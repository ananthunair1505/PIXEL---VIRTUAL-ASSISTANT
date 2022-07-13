import importlib
import sys
import time
from os import listdir
from os.path import abspath, dirname, basename, isdir, join
from threading import Lock
from microsoft.configuration import Configuration
from microsoft.messagebus.message import Message
from microsoft.util.log import LOG
from microsoft.util.monotonic_event import MonotonicEvent
from microsoft.util.plugins import find_plugins
from .services import RemoteAudioBackend
MINUTES = 60
MAINMODULE = '__init__'
sys.path.append(abspath(dirname(__file__)))
def create_service_spec(service_folder):
    module_name = 'audioservice_' + basename(service_folder)
    path = join(service_folder, MAINMODULE + '.py')
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    info = {'spec': spec, 'mod': mod, 'module_name': module_name}
    return {"name": basename(service_folder), "info": info}
def get_services(services_folder):
    LOG.info("Loading services from " + services_folder)
    services = []
    possible_services = listdir(services_folder)
    for i in possible_services:
        location = join(services_folder, i)
        if (isdir(location) and
                not MAINMODULE + ".py" in listdir(location)):
            for j in listdir(location):
                name = join(location, j)
                if (not isdir(name) or
                        not MAINMODULE + ".py" in listdir(name)):
                    continue
                try:
                    services.append(create_service_spec(name))
                except Exception:
                    LOG.error('Failed to create service from ' + name,
                              exc_info=True)
        if (not isdir(location) or
                not MAINMODULE + ".py" in listdir(location)):
            continue
        try:
            services.append(create_service_spec(location))
        except Exception:
            LOG.error('Failed to create service from ' + location,
                      exc_info=True)
    return sorted(services, key=lambda p: p.get('name'))
def setup_service(service_module, config, bus):
    if (hasattr(service_module, 'autodetect') and
            callable(service_module.autodetect)):
        try:
            return service_module.autodetect(config, bus)
        except Exception as e:
            LOG.error('Failed to autodetect. ' + repr(e))
    elif hasattr(service_module, 'load_service'):
        try:
            return service_module.load_service(config, bus)
        except Exception as e:
            LOG.error('Failed to load service. ' + repr(e))
    else:
        LOG.error('Failed to load service. loading function not found')
        return None
def load_internal_services(config, bus, path=None):
    if path is None:
        path = dirname(abspath(__file__)) + '/services/'
    service_directories = get_services(path)
    service = []
    for descriptor in service_directories:
        LOG.info('Loading ' + descriptor['name'])
        try:
            service_module = descriptor['info']['mod']
            spec = descriptor['info']['spec']
            module_name = descriptor['info']['module_name']
            sys.modules[module_name] = service_module
            spec.loader.exec_module(service_module)
        except Exception as e:
            LOG.error('Failed to import module ' + descriptor['name'] + '\n' +
                      repr(e))
        else:
            s = setup_service(service_module, config, bus)
            if s:
                service += s
    return service
def load_plugins(config, bus):
    plugin_services = []
    found_plugins = find_plugins('microsoft.plugin.audioservice')
    for plugin_name, plugin_module in found_plugins.items():
        LOG.info(f'Loading audio service plugin: {plugin_name}')
        service = setup_service(plugin_module, config, bus)
        if service:
            plugin_services += service
    return plugin_services
def load_services(config, bus, path=None):
    return (load_internal_services(config, bus, path) +
            load_plugins(config, bus))
class AudioService:
    def __init__(self, bus):
        self.bus = bus
        self.config = Configuration.get().get("Audio")
        self.service_lock = Lock()
        self.default = None
        self.service = []
        self.current = None
        self.play_start_time = 0
        self.volume_is_low = False
        self._loaded = MonotonicEvent()
        self.load_services()
    def load_services(self):
        services = load_services(self.config, self.bus)
        local = [s for s in services if not isinstance(s, RemoteAudioBackend)]
        remote = [s for s in services if isinstance(s, RemoteAudioBackend)]
        self.service = local + remote
        for s in self.service:
            s.set_track_start_callback(self.track_start)
        default_name = self.config.get('default-backend', '')
        LOG.info('Finding default backend...')
        for s in self.service:
            if s.name == default_name:
                self.default = s
                LOG.info('Found ' + self.default.name)
                break
        else:
            self.default = None
            LOG.info('no default found')
        self.bus.on('microsoft.audio.service.play', self._play)
        self.bus.on('microsoft.audio.service.queue', self._queue)
        self.bus.on('microsoft.audio.service.pause', self._pause)
        self.bus.on('microsoft.audio.service.resume', self._resume)
        self.bus.on('microsoft.audio.service.stop', self._stop)
        self.bus.on('microsoft.audio.service.next', self._next)
        self.bus.on('microsoft.audio.service.prev', self._prev)
        self.bus.on('microsoft.audio.service.track_info', self._track_info)
        self.bus.on('microsoft.audio.service.list_backends', self._list_backends)
        self.bus.on('microsoft.audio.service.seek_forward', self._seek_forward)
        self.bus.on('microsoft.audio.service.seek_backward', self._seek_backward)
        self.bus.on('recognizer_loop:audio_output_start', self._lower_volume)
        self.bus.on('recognizer_loop:record_begin', self._lower_volume)
        self.bus.on('recognizer_loop:audio_output_end', self._restore_volume)
        self.bus.on('recognizer_loop:record_end',
                    self._restore_volume_after_record)
        self._loaded.set()
    def wait_for_load(self, timeout=3 * MINUTES):
        return self._loaded.wait(timeout)

    def track_start(self, track):
        if track:
            LOG.debug('New track coming up!')
            self.bus.emit(Message('microsoft.audio.playing_track',
                                  data={'track': track}))
        else:
            LOG.debug('End of playlist!')
            self.bus.emit(Message('microsoft.audio.queue_end'))

    def _pause(self, message=None):
        if self.current:
            self.current.pause()

    def _resume(self, message=None):
        if self.current:
            self.current.resume()

    def _next(self, message=None):
        if self.current:
            self.current.next()

    def _prev(self, message=None):
        if self.current:
            self.current.previous()

    def _perform_stop(self):
        if self.current:
            name = self.current.name
            if self.current.stop():
                self.bus.emit(Message("microsoft.stop.handled",
                                      {"by": "audio:" + name}))
        self.current = None
    def _stop(self, message=None):
        if time.monotonic() - self.play_start_time > 1:
            LOG.debug('stopping all playing services')
            with self.service_lock:
                self._perform_stop()
        LOG.info('END Stop')

    def _lower_volume(self, message=None):
        if self.current:
            LOG.debug('lowering volume')
            self.current.lower_volume()
            self.volume_is_low = True

    def _restore_volume(self, _=None):
        current = self.current
        if current:
            LOG.debug('restoring volume')
            self.volume_is_low = False
            current.restore_volume()

    def _restore_volume_after_record(self, message=None):
        def restore_volume():
            LOG.debug('restoring volume')
            self.current.restore_volume()
        if self.current:
            self.bus.on('recognizer_loop:speech.recognition.unknown',
                        restore_volume)
            speak_msg_detected = self.bus.wait_for_message('speak',
                                                           timeout=8.0)
            if not speak_msg_detected:
                restore_volume()
            self.bus.remove('recognizer_loop:speech.recognition.unknown',
                            restore_volume)
        else:
            LOG.debug("No audio service to restore volume of")
    def play(self, tracks, prefered_service, repeat=False):
        self._perform_stop()
        if isinstance(tracks[0], str):
            uri_type = tracks[0].split(':')[0]
        else:
            uri_type = tracks[0][0].split(':')[0]
        if prefered_service and uri_type in prefered_service.supported_uris():
            selected_service = prefered_service
        elif self.default and uri_type in self.default.supported_uris():
            LOG.debug("Using default backend ({})".format(self.default.name))
            selected_service = self.default
        else:
            LOG.debug("Searching the services")
            for s in self.service:
                if uri_type in s.supported_uris():
                    LOG.debug("Service {} supports URI {}".format(s, uri_type))
                    selected_service = s
                    break
            else:
                LOG.info('No service found for uri_type: ' + uri_type)
                return
        if not selected_service.supports_mime_hints:
            tracks = [t[0] if isinstance(t, list) else t for t in tracks]
        selected_service.clear_list()
        selected_service.add_list(tracks)
        selected_service.play(repeat)
        self.current = selected_service
        self.play_start_time = time.monotonic()
    def _queue(self, message):
        if self.current:
            with self.service_lock:
                tracks = message.data['tracks']
                self.current.add_list(tracks)
        else:
            self._play(message)
    def _play(self, message):
        with self.service_lock:
            tracks = message.data['tracks']
            repeat = message.data.get('repeat', False)
            for s in self.service:
                if ('utterance' in message.data and
                        s.name in message.data['utterance']):
                    prefered_service = s
                    LOG.debug(s.name + ' would be prefered')
                    break
            else:
                prefered_service = None
            self.play(tracks, prefered_service, repeat)
            time.sleep(0.5)
    def _track_info(self, message):
        if self.current:
            track_info = self.current.track_info()
        else:
            track_info = {}
        self.bus.emit(Message('microsoft.audio.service.track_info_reply',
                              data=track_info))
    def _list_backends(self, message):
        data = {}
        for s in self.service:
            info = {
                'supported_uris': s.supported_uris(),
                'default': s == self.default,
                'remote': isinstance(s, RemoteAudioBackend)
            }
            data[s.name] = info
        self.bus.emit(message.response(data))
    def _seek_forward(self, message):
        seconds = message.data.get("seconds", 1)
        if self.current:
            self.current.seek_forward(seconds)

    def _seek_backward(self, message):
        seconds = message.data.get("seconds", 1)
        if self.current:
            self.current.seek_backward(seconds)
    def shutdown(self):
        for s in self.service:
            try:
                LOG.info('shutting down ' + s.name)
                s.shutdown()
            except Exception as e:
                LOG.error('shutdown of ' + s.name + ' failed: ' + repr(e))
        self.bus.remove('microsoft.audio.service.play', self._play)
        self.bus.remove('microsoft.audio.service.queue', self._queue)
        self.bus.remove('microsoft.audio.service.pause', self._pause)
        self.bus.remove('microsoft.audio.service.resume', self._resume)
        self.bus.remove('microsoft.audio.service.stop', self._stop)
        self.bus.remove('microsoft.audio.service.next', self._next)
        self.bus.remove('microsoft.audio.service.prev', self._prev)
        self.bus.remove('microsoft.audio.service.track_info', self._track_info)
        self.bus.remove('microsoft.audio.service.seek_forward',
                        self._seek_forward)
        self.bus.remove('microsoft.audio.service.seek_backward',
                        self._seek_backward)
        self.bus.remove('recognizer_loop:audio_output_start',
                        self._lower_volume)
        self.bus.remove('recognizer_loop:record_begin', self._lower_volume)
        self.bus.remove('recognizer_loop:audio_output_end',
                        self._restore_volume)
        self.bus.remove('recognizer_loop:record_end',
                        self._restore_volume_after_record)