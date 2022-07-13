import sys
import os
import stat
from lib import ServerCommunication, ConnectionWatchdog, Receiver
from lib import SMTPAlert
from lib import RaspberryPiGPIOAlert, AlertEventHandler
from lib import GlobalData
import logging
import time
import random
import signal
import RPi.GPIO as GPIO
import xml.etree.ElementTree

def signal_handler(signum, frame):
    log_tag = os.path.basename(__file__)
    logging.info("[%s] Resetting GPIOs." % log_tag)
    GPIO.cleanup()
    logging.info("[%s] Exiting client." % log_tag)
    sys.exit(0)


def make_path(input_location: str) -> str:
   
    if input_location[0] == "/":
        return input_location
    
    elif input_location[0] == "~":
        pos = -1
        for i in range(1, len(input_location)):
            if input_location[i] == "/":
                continue
            pos = i
            break
        if pos == -1:
            return os.environ["HOME"]
        return os.path.join(os.environ["HOME"], input_location[pos:])
   
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), input_location)


if __name__ == '__main__':

    globalData = GlobalData()

    log_tag = os.path.basename(__file__)
    try:
        configRoot = xml.etree.ElementTree.parse(globalData.configFile).getroot()

        logfile = make_path(str(configRoot.find("general").find("log").attrib["file"]))
        tempLoglevel = str(configRoot.find("general").find("log").attrib["level"])
        tempLoglevel = tempLoglevel.upper()
        if tempLoglevel == "DEBUG":
            loglevel = logging.DEBUG
        elif tempLoglevel == "INFO":
            loglevel = logging.INFO
        elif tempLoglevel == "WARNING":
            loglevel = logging.WARNING
        elif tempLoglevel == "ERROR":
            loglevel = logging.ERROR
        elif tempLoglevel == "CRITICAL":
            loglevel = logging.CRITICAL
        else:
            raise ValueError("No valid log level in config file.")
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %H:%M:%S',
                            filename=logfile,
                            level=loglevel)

    except Exception as e:
        print("Config could not be parsed.")
        print(e)
        sys.exit(1)
    try:
        config_stat = os.stat(globalData.configFile)
        if (config_stat.st_mode & stat.S_IROTH
                or config_stat.st_mode & stat.S_IWOTH
                or config_stat.st_mode & stat.S_IXOTH):
            raise ValueError("Config file is accessible by others. Please remove file permissions for others.")
        version = float(configRoot.attrib["version"])
        if version != globalData.version:
            raise ValueError("Config version '%.3f' not "
                             % version
                             + "compatible with client version '%.3f'."
                             % globalData.version)

        server = str(configRoot.find("general").find("server").attrib["host"])
        serverPort = int(configRoot.find("general").find("server").attrib["port"])

        ssl_enabled = (str(configRoot.find("general").find("ssl").attrib["enabled"]).upper() == "TRUE")
        server_ca_file = None
        client_cert_file = None
        client_key_file = None
        if ssl_enabled:
            server_ca_file = os.path.abspath(make_path(str(configRoot.find("general").find("ssl").find("server").attrib[
                                                             "caFile"])))
            if os.path.exists(server_ca_file) is False:
                raise ValueError("Server CA does not exist.")

            certificate_required = (str(configRoot.find("general").find("ssl").find("client").attrib[
                                           "certificateRequired"]).upper() == "TRUE")

            if certificate_required is True:
                client_cert_file = os.path.abspath(
                                 make_path(str(configRoot.find("general").find("ssl").find("client").attrib["certFile"])))
                client_key_file = os.path.abspath(
                                make_path(str(configRoot.find("general").find("ssl").find("client").attrib["keyFile"])))
                if (os.path.exists(client_cert_file) is False
                        or os.path.exists(client_key_file) is False):
                    raise ValueError("Client certificate or key does not exist.")

                key_stat = os.stat(client_key_file)
                if (key_stat.st_mode & stat.S_IROTH
                        or key_stat.st_mode & stat.S_IWOTH
                        or key_stat.st_mode & stat.S_IXOTH):
                    raise ValueError("Client key is accessible by others. Please remove file permissions for others.")

        else:
            logging.warning("[%s] TLS/SSL is disabled. Do NOT use this setting in a production environment."
                            % log_tag)

        username = str(configRoot.find("general").find("credentials").attrib["username"])
        password = str(configRoot.find("general").find("credentials").attrib["password"])
        temp = (str(configRoot.find("general").find("connection").attrib["persistent"]).upper() == "TRUE")
        if temp:
            globalData.persistent = 1
        else:
            globalData.persistent = 0
        smtpActivated = (str(configRoot.find("smtp").find("general").attrib["activated"]).upper() == "TRUE")
        smtpServer = ""
        smtpPort = -1
        smtpFromAddr = ""
        smtpToAddr = ""
        if smtpActivated is True:
            smtpServer = str(configRoot.find("smtp").find("server").attrib["host"])
            smtpPort = int(configRoot.find("smtp").find("server").attrib["port"])
            smtpFromAddr = str(configRoot.find("smtp").find("general").attrib["fromAddr"])
            smtpToAddr = str(configRoot.find("smtp").find("general").attrib["toAddr"])
        for item in configRoot.find("alerts").iterfind("alert"):

            alert = RaspberryPiGPIOAlert()
            alert.gpio_pin = int(item.find("gpio").attrib["gpioPin"])
            if int(item.find("gpio").attrib["gpioPinStateNormal"]) == 1:
                alert.gpio_pin_state_normal = GPIO.HIGH

            else:
                alert.gpio_pin_state_normal = GPIO.LOW

            if int(item.find("gpio").attrib["gpioPinStateTriggered"]) == 1:
                alert.gpio_pin_state_triggered = GPIO.HIGH

            else:
                alert.gpio_pin_state_triggered = GPIO.LOW

            recv_triggered_activated = str(item.find("gpio").find("triggered").attrib["activated"]).upper() == "TRUE"
            alert.recv_triggered_activated = recv_triggered_activated
            if recv_triggered_activated:
                alert.recv_triggered_state = int(item.find("gpio").find("triggered").attrib["state"])

            recv_normal_activated = str(item.find("gpio").find("normal").attrib["activated"]).upper() == "TRUE"
            alert.recv_normal_activated = recv_normal_activated
            if recv_normal_activated:
                alert.recv_normal_state = int(item.find("gpio").find("normal").attrib["state"])

            recv_profile_change_activated = str(
                item.find("gpio").find("profilechange").attrib["activated"]).upper() == "TRUE"
            alert.recv_profile_change_activated = recv_profile_change_activated
            if recv_profile_change_activated:
                for profile in item.find("gpio").find("profilechange").iterfind("profile"):
                    alert.recv_profile_change_target_profiles.add(int(profile.text))

            gpio_reset_activated = str(item.find("gpio").find("reset").attrib["activated"]).upper() == "TRUE"
            alert.gpio_reset_activated = gpio_reset_activated
            if gpio_reset_activated:
                alert.gpio_reset_state_time = int(item.find("gpio").find("reset").attrib["time"])
            alert.id = int(item.find("general").attrib["id"])
            alert.description = str(item.find("general").attrib["description"])

            if alert.gpio_reset_activated and alert.gpio_reset_state_time <= 0:
                raise ValueError("time for reset of Alert %d has to be greater to 0." % alert.id)

            if recv_triggered_activated and alert.recv_triggered_state != 0 and alert.recv_triggered_state != 1:
                raise ValueError("state for 'triggered' sensor alert of Alert %d has to be 0 or 1." % alert.id)

            if recv_normal_activated and alert.recv_normal_state != 0 and alert.recv_normal_state != 1:
                raise ValueError("state for 'normal' sensor alert of Alert %d has to be 0 or 1." % alert.id)

            if recv_profile_change_activated and not alert.recv_profile_change_target_profiles:
                raise ValueError("No profiles set for profilechange of alert %d."
                                 % alert.id)

            alert.alertLevels = list()
            for alertLevelXml in item.iterfind("alertLevel"):
                alert.alertLevels.append(int(alertLevelXml.text))
            if len(alert.description) == 0:
                raise ValueError("Description of alert %d is empty."
                                 % alert.id)
            for registeredAlert in globalData.alerts:
                if registeredAlert.id == alert.id:
                    raise ValueError("Id of alert %d is already taken."
                                     % alert.id)

            globalData.alerts.append(alert)

    except Exception as e:
        logging.exception("[%s] Could not parse config." % log_tag)
        sys.exit(1)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    random.seed()
    if smtpActivated is True:
        globalData.smtpAlert = SMTPAlert(smtpServer, smtpPort, smtpFromAddr, smtpToAddr)
    else:
        globalData.smtpAlert = None
    globalData.serverComm = ServerCommunication(server,
                                                serverPort,
                                                server_ca_file,
                                                username,
                                                password,
                                                client_cert_file,
                                                client_key_file,
                                                AlertEventHandler(globalData),
                                                globalData)
    connectionRetries = 1
    logging.info("[%s] Connecting to server." % log_tag)
    while True:
        if (globalData.smtpAlert is not None
                and (connectionRetries % 5) == 0):
            globalData.smtpAlert.sendCommunicationAlert(connectionRetries)

        if globalData.serverComm.initialize() is True:
            if globalData.smtpAlert is not None:
                globalData.smtpAlert.sendCommunicationAlertClear()

            connectionRetries = 1
            break

        connectionRetries += 1

        logging.critical("[%s] Connecting to server failed. Try again in 5 seconds." % log_tag)
        time.sleep(5)
    logging.info("[%s] Starting watchdog thread." % log_tag)
    watchdog = ConnectionWatchdog(globalData.serverComm,
                                  globalData.pingInterval,
                                  globalData.smtpAlert)
    watchdog.daemon = True
    watchdog.start()
    logging.info("[%s] Initializing alerts." % log_tag)
    for alert in globalData.alerts:
        alert.initialize()

    logging.info("[%s] Client started." % log_tag)
    receiver = Receiver(globalData.serverComm)
    receiver.run()