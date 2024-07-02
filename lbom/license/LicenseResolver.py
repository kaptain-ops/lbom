from lbom.bom.BomHandler import BomHandler
from lbom.clearly_defined.ClearlyDefinedClient import ClearlyDefinedClient
from typing import List
import sys


class LicenseResolver:
    def __init__(self, bom_handler: BomHandler):
        self.bom_handler: BomHandler = bom_handler
        self.clearly_defined_client: ClearlyDefinedClient = ClearlyDefinedClient()

    def download_notices(self, ignore_with_str: str | None = None) -> str:
        cd_uris: List[str] = self.bom_handler.get_cd_uris(ignore_with_str)
        return self.clearly_defined_client.fetch_notices(cd_uris)

    def download_licenses(
        self,
        ignore_with_str: str | None = None,
        harvest_missing: bool = False,
    ) -> dict:

        cd_uris: List[str] = self.bom_handler.get_cd_uris(ignore_with_str)
        licenses = self.clearly_defined_client.fetch_licenses(cd_uris)
        missing_licenses: List[str] = []
        for cd_uri, license_details in list(licenses.items()):
            license_obj = license_details.licensed
            tool_score = license_obj.toolScore.declared
            if license_obj.declared is None and tool_score == 0:
                print(f"Missing definition {cd_uri}", file=sys.stderr)
                missing_licenses.append(cd_uri)
                del licenses[cd_uri]

        if harvest_missing:
            self.clearly_defined_client.harvest_packages(missing_licenses)

        return self.bom_handler.update_bom_with_licenses(licenses)
