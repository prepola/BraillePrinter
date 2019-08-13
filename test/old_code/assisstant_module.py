# google-oauthlib-tool --scope https://www.googleapis.com/auth/assistant-sdk-prototype --scope https://www.googleapis.com/auth/gcm   --save --headless --client-secrets client_secret_454163905606-tjq3ajui0a62bcfnl48p4igueobueai4.apps.googleusercontent.com.json
# googlesamples-assistant-pushtotalk --device-id brailleprinter-f4c63 --device-model-id brailleprinter-f4c63-raspberry-us2ld5 --lang ko-KR

from googlesamples.assistant.grpc import pushtotalk
import subprocess

api_endpoint = 'embeddedassistant.googleapis.com'
project_id = 'brailleprinter-f4c63'
device_model_id = 'brailleprinter-f4c63-raspberry-us2ld5'
lang = 'ko-KR'
credentials = 'client_secret_454163905606-tjq3ajui0a62bcfnl48p4igueobueai4.apps.googleusercontent.com.json'

result = subprocess.check_output("googlesamples-assistant-pushtotalk --device-id brailleprinter-f4c63 --device-model-id brailleprinter-f4c63-raspberry-us2ld5 --lang ko-KR")
print(result)

#assistant.SampleAssistant('ko-KR','brailleprinter-f4c63-raspberry-us2ld5', 'brailleprinter-f4c63', None, None, None, None, None)
    
