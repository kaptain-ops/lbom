# ClearlyDefinedClient.py

import requests
from typing import List
from lbom.utils.Utils import Utils
import sys

from lbom.clearly_defined.ClearlyDefinedDetail import ClearlyDefinedResponse


class ClearlyDefinedClient:
    API_BASE_URL = "https://api.clearlydefined.io"

    def __init__(self, batch_size=50):
        self.batch_size = batch_size
        pass

    def fetch_notices(self, cd_uris: List[str]) -> str:
        notices = ""
        cd_chunks: List[List[str]] = Utils.divide_chunks(cd_uris, self.batch_size)

        for cd_uris in cd_chunks:
            notices += self.__fetch_notices(cd_uris)
        return notices

    def __fetch_notices(self, cd_uris: List[str]) -> str:
        try:
            response = requests.post(
                f"{self.API_BASE_URL}/notices",
                json={"coordinates": cd_uris, "options": {}},
            )
            return response.json().get("content", "")
        except requests.exceptions.RequestException as e:
            print(f"Could not fetch notices: {e}", file=sys.stderr)
            return ""

    def fetch_licenses(self, cd_uris: List[str]) -> ClearlyDefinedResponse:
        cd_chunks: List[List[str]] = Utils.divide_chunks(cd_uris, self.batch_size)
        licenses: ClearlyDefinedResponse | None = None
        for chunk in cd_chunks:
            license_chunk = self.__fetch_licenses(chunk)
            if licenses is None:
                licenses = license_chunk
            else:
                licenses.update(license_chunk)
        return licenses  # This always contains license

    def __fetch_licenses(self, cd_uris: List[str]) -> ClearlyDefinedResponse:
        try:
            response = requests.post(f"{self.API_BASE_URL}/definitions", json=cd_uris)
            if response.status_code != 200:
                print(
                    f"Request failed: {response.status_code}, {response.text}",
                    file=sys.stderr,
                )
                exit(-1)

            json_response = response.json()
            return ClearlyDefinedResponse.from_dict(json_response)

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}", file=sys.stderr)
            exit(-1)

    def harvest_packages(self, cd_uris: List[str]):
        try:
            requests.post(
                f"{self.API_BASE_URL}/harvest",
                json=[{"tool": "package", "coordinates": cd_uris}],
            )
        except requests.exceptions.RequestException as e:
            print(f"Could not harvest packages: {e}", file=sys.stderr)
