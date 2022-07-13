import time
from microsoft.util.signal import check_for_signal
def is_speaking():
    return check_for_signal("isSpeaking", -1)
def wait_while_speaking():
    time.sleep(0.3)
    while is_speaking():
        time.sleep(0.1)
def stop_speaking():
    if is_speaking():
        from microsoft.messagebus.send import send
        send('audio.speech.stop')
        while check_for_signal("isSpeaking", -1):
            time.sleep(0.25)