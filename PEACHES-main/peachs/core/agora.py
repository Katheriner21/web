# agora_token.py
import time
from agora_token_builder import RtcTokenBuilder

# Reemplaza con tus credenciales de Ágora
APP_ID = "2cf9aef4e0f145398ee2aa61fd034931"
APP_CERTIFICATE = "51cc404902fb4d168a1a6bfcb650316e"

def get_rtc_token(channelName, uid=0, role="host"):
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    token = RtcTokenBuilder.buildTokenWithUid(APP_ID, APP_CERTIFICATE, channelName, uid, role, privilegeExpiredTs)
    return token
