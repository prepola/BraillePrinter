# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Text-To-Speech API sample application .
Example usage:
    python quickstart.py
"""
import os
from google.cloud import texttospeech
import pyaudio
import wave
import threading
import io

chunk = 1024

class run_voice(threading.Thread):
    def __init__(self, text, name=''):
        # [START tts_quickstart]
        """Synthesizes speech from the input string of text or ssml.
        Note: ssml must be well-formed according to:
            https://www.w3.org/TR/speech-synthesis/
        """
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\hanium project-3d7b2a095e96.json'
        # Instantiates a client
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.types.SynthesisInput(text=text)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.types.VoiceSelectionParams(
            language_code='ko-KR',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

        # Select the type of audio file you want returned
        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16,
            speaking_rate=0.8)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(synthesis_input, voice, audio_config)

        # open the file for reading.
        # with open('.\\output.wav', 'wb') as out:
        # # Write the response to the output file.
        #     out.write(response.audio_content)
        self.audio_data = io.BytesIO(response.audio_content)

        threading.Thread.__init__(self,name=name)
        self.stop_event = threading.Event()

    def run (self):
        # wf = wave.open('.\\output.wav', 'rb')
        wf = wave.open(self.audio_data, 'rb')

        # create an audio object
        p = pyaudio.PyAudio()

        # open stream based on the wave object which has been input.
        stream = p.open(format =
                        p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output = True)

        # read data (based on the chunk size)
        data = wf.readframes(chunk)
        while len(data) > 1:
            # writing to the stream is what *actually* plays the sound.
            stream.write(data)
            data = wf.readframes(chunk)
            if self.stop_event.is_set():
                break
        stream.close()    
        p.terminate()

    def stop(self): 
        self.stop_event.set()
        # self.join()

if __name__ == '__main__':
    run_voice('테스트 음성입니다.').start()