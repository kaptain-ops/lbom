
import sys
from typing import List

from lbom.clearly_defined.ClearlyDefinedProviders import ClearlyDefinedProviders
from lbom.bom.BomHandler import BomHandler
from lbom.clearly_defined.ClearlyDefinedDetail import ClearlyDefinedResponse

class BomHandlerCyclonedx(BomHandler):
    supported_version: List[str] = ["1.4", "1.5"]

    def __init__(
        self, bom_json: dict, clearlydefinedproviders: ClearlyDefinedProviders
    ) -> None:
        self.providers = clearlydefinedproviders

        version = bom_json.get("specVersion", None)
        if version not in self.supported_version:
            print("Supported cyclonedx versions " + ",".join(self.supported_version))
        self.bom_json = bom_json

    def get_cd_uris(self, ignore_with_str: str | None = None) -> List[str]:
        components: List[dict] = self.bom_json.get("components", [])

        purls = []
        for dependency in components:
            purl_str: str = dependency.get("purl", None)
            if not purl_str:
                print(f"No purl found for package {dependency}", file=sys.stderr)
                continue
            purls.append(purl_str)

        return self.providers.get_cd_uris(purls, ignore_with_str)

    def update_bom_with_licenses(self, licenses: ClearlyDefinedResponse) -> dict:
        components: List[dict] = self.bom_json.get("components", [])
        for key, value in licenses.items():
            for index, dependency in enumerate(components):
                purl: str = dependency.get("purl", "")
                if not purl:
                    continue
                if self.providers.get_cd_uri(purl) == key:
                    dependency["licenses"] = [
                        {"license": {"id": value.licensed.declared}}
                    ]
                    components[index] = dependency
        self.bom_json["components"] = components
        return self.bom_json
