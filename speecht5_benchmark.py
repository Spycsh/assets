import base64
import json
import os
import urllib.request
import uuid
import requests
from time import time
import numpy as np

DATASET_PATH = "./LibriSpeech/test-clean"
EXP_NAME = "speecht5_gaudi_librispeech_benchmark"

ENDPOINT = "http://localhost:7055/v1/tts"

class SpeechT5BM:
    def __init__(self, endpoint, dataset_name, dataset_path):
        self.endpoint = endpoint
        self.dataset_name = dataset_name
        self.dataset_path = dataset_path
        self.compute_times = dict()
        if self.dataset_name == 'librispeech':
            self.run_bm = self.ls_bm
        elif self.dataset_name == 'single':
            self.run_bm = self.single_bm

    def prepare_text_list(self, path_to_file):
        with open(path_to_file, 'r') as file:
            lines = file.readlines()

        for line in lines:
            parts = line.split(maxsplit=1)  # maxsplit=1 ensures only the first whitespace is considered
            if len(parts) > 1:  # Ensure there's text after the ID
                yield parts[1].strip().lower()  # Add the text part, stripping any trailing spaces, lowercase


    def single_bm(self):
        #WIP
        pass

    def ls_bm(self, num_requests=100):
        req_idx = 0
        for i in os.listdir(self.dataset_path):
            for j in os.listdir(os.path.join(self.dataset_path, i)):
                for k in os.listdir(os.path.join(self.dataset_path, i, j)):

                    if k.endswith('.trans.txt'):
                        for text in self.prepare_text_list(os.path.join(self.dataset_path, i, j, k)):
                            print(text)

                            while req_idx == num_requests:
                                p50 = np.percentile(list(self.compute_times.values()),50)
                                p99 = np.percentile(list(self.compute_times.values()),99)
                                print(f">>>> {num_requests} requests processed! P50: {p50}, P99: {p99}")
                                return
                            start = time()
                            # do the req/reply
                            response = requests.post(self.endpoint, headers={"Content-Type": "application/json"}, json={"text":text}, proxies={"http": None})
                            assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
                            end = time()
                            self.compute_times[req_idx] = end - start
                            print(req_idx, self.compute_times[req_idx])
                            req_idx += 1


def main():
    benchmark = SpeechT5BM(ENDPOINT,
                          'librispeech',
                          DATASET_PATH)
    benchmark.run_bm(num_requests=100)


if __name__ == "__main__":
    main()
