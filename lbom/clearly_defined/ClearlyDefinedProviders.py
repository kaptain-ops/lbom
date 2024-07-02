from packageurl import PackageURL
from typing import List
import sys


class ClearlyDefinedProviders:

    PROVIDERS: dict[str, str] = {
        "npm": "npmjs",
        "maven": "mavencentral",
        "git": "github",
        "nuget": "nuget",
        "pypi": "pypi",
        "gem": "rubygems",
        "pod": "cocoapods",
        "crate": "cratesio",
        "debsrc": "debian",
        "deb": "debian",
        "composer": "packagist",
        "go": "golang",
    }

    def get_provider(self, package_type: str) -> str:
        return self.PROVIDERS.get(package_type, "")

    def get_cd_uri(self, purl_str: str) -> str:
        purl: dict = PackageURL.from_string(purl_str).to_dict()
        package_type: str = purl.get("type", "")
        namespace: str = purl.get("namespace", "-")
        name: str = purl.get("name", "")
        version: str = purl.get("version", "")
        provider: str = self.get_provider(package_type)

        if not provider:
            print(f"Missing provider for type {package_type}", file=sys.stderr)
            return ""

        if namespace is None:
            namespace = "-"
        namespace = namespace.replace("/", "%2F")
        return f"{package_type}/{provider}/{namespace}/{name}/{version}"

    def get_cd_uris(
        self, purls: List[str], ignore_with_str: str | None = None
    ) -> List[str]:
        cd_artifacts: List[str] = []

        for purl in purls:
            ignore: bool = False
            cd_uri: str = self.get_cd_uri(purl)
            if ignore_with_str:
                ignore_words: List[str] = ignore_with_str.split(",")
                if any(word in cd_uri for word in ignore_words):
                    ignore = True
                    print(f"Ignoring library {cd_uri}", file=sys.stderr)

            if not ignore:
                cd_artifacts.append(cd_uri)

        return cd_artifacts
