# Copyright (C) 2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import base64
import json
import os
import urllib.request
import uuid

import requests

# https://gist.github.com/novwhisky/8a1a0168b94f3b6abfaa
# test_audio_base64_str = "UklGRigAAABXQVZFZm10IBIAAAABAAEARKwAAIhYAQACABAAAABkYXRhAgAAAAEA"

uid = str(uuid.uuid4())
file_name = uid + ".wav"

urllib.request.urlretrieve(
    "https://github.com/Spycsh/assets/raw/refs/heads/main/prompt.wav",
    file_name,
)

with open(file_name, "rb") as f:
    test_audio_base64_str = base64.b64encode(f.read()).decode("utf-8")
os.remove(file_name)

endpoint = "http://localhost:3008/v1/audioqna"
inputs = {"audio": test_audio_base64_str, "max_tokens":64, "tts_text_language":"zh"}
response = requests.post(url=endpoint, data=json.dumps(inputs), proxies={"http": None})

def base64_to_wav(base64_string, output_file="out.wav"):
    # Decode the base64 string into binary data
    audio_data = base64.b64decode(base64_string)
    
    # Write the binary data to a .wav file
    with open(output_file, 'wb') as file:
        file.write(audio_data)

base64_to_wav(response.text)