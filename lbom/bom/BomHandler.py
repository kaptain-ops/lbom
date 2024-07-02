from abc import ABC, abstractmethod
from typing import List

from lbom.clearly_defined.ClearlyDefinedDetail import ClearlyDefinedResponse

class BomHandler(ABC):

    @abstractmethod
    def get_cd_uris(self, ignore_with_str: str | None = None) -> List[str]:
        pass

    @abstractmethod
    def update_bom_with_licenses(self, licenses: ClearlyDefinedResponse) -> dict:
        pass
