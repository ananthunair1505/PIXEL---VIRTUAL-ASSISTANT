import re
from message.util.parse import normalize
from message_bus_client.message import dig_for_message
import message_bus_client
class Message(message_bus_client.Message):
    def utterance_remainder(self):
        utt = normalize(self.data.get(" ", ""))
        if utt and "__tags__" in self.data:
            for token in self.data["__tags__"]:
                utt = re.sub(r'\b' + token.get("key", "") + r"\b", "", utt)
        return normalize(utt)