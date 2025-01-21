import base64
import json
import os
import urllib.request
import uuid
import requests
from time import time
import numpy as np

DATASET_PATH = "./LibriSpeech/test-clean"
EXP_NAME = "whisper_gaudi_librispeech_benchmark"
######## Note: using /v1/asr or /v1/audio/transcriptions has little perf gap and can be ignored.
"""
ENDPOINT = "http://localhost:7066/v1/asr"
"""
ENDPOINT = "http://localhost:7066/v1/audio/transcriptions"

class WhisperBM:
    def __init__(self, endpoint, dataset_name, dataset_path):
        self.endpoint = endpoint
        self.dataset_name = dataset_name
        self.dataset_path = dataset_path
        self.compute_times = dict()
        if self.dataset_name == 'librispeech':
            self.run_bm = self.ls_bm
        elif self.dataset_name == 'single':
            self.run_bm = self.single_bm

    def single_bm(self):
        #WIP
        pass

    def ls_bm(self, num_requests=100):
        req_idx = 0
        for i in os.listdir(self.dataset_path):
            for j in os.listdir(os.path.join(self.dataset_path, i)):
                for k in os.listdir(os.path.join(self.dataset_path, i, j)):

                    if k.endswith('.flac'):
                        while req_idx == num_requests:
                            p50 = np.percentile(list(self.compute_times.values()),50)
                            p99 = np.percentile(list(self.compute_times.values()),99)
                            print(f">>>> {num_requests} requests processed! P50: {p50}, P99: {p99}")
                            return
                        fname = os.path.join(self.dataset_path, i, j, k)
                        """
                        with open(fname, "rb") as f:
                            test_audio_base64_str = base64.b64encode(f.read()).decode("utf-8")


                        inputs = {"audio": test_audio_base64_str}

                        start = time()
                        response = requests.post(url=self.endpoint, data=json.dumps(inputs), proxies={"http": None})
                        end = time()
                        """
                        start = time()
                        with open(fname, "rb") as audio_file:
                            files = {"file": (fname, audio_file)}
                            response = requests.post(self.endpoint, files=files, data={"model": "openai/whisper-small","language": "english"}, proxies={"http": None})
                        end = time()
                        self.compute_times[fname] = end - start
                        print(k, self.compute_times[fname])
                        req_idx += 1

    def save_results(self, exp_name):
        # Save the dictionary to a file
        output_fname = f"{exp_name}_0"
        while os.path.exists(f'{output_fname}.json'):
            output_fname = output_fname[:-1] + str(int(output_fname[-1]) + 1)

        with open(f"{output_fname}.json", "w") as f:
            json.dump(self.compute_times, f)


def main():
    benchmark = WhisperBM(ENDPOINT,
                          'librispeech',
                          DATASET_PATH)
    benchmark.run_bm(num_requests=100)
    benchmark.save_results(EXP_NAME)


if __name__ == "__main__":
    main()
