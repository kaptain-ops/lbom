from dataclasses import dataclass
from typing import Dict

@dataclass
class ToolScore:
    total: int
    declared: int
    discovered: int
    consistency: int
    spdx: int
    texts: int

    def __init__(
        self,
        total: int,
        declared: int,
        discovered: int,
        consistency: int,
        spdx: int,
        texts: int,
    ) -> None:
        self.total = total
        self.declared = declared
        self.discovered = discovered
        self.consistency = consistency
        self.spdx = spdx
        self.texts = texts
        pass


@dataclass
class Licensed:
    declared: str
    toolScore: ToolScore

    def __init__(self, declared: str, toolScore: ToolScore) -> None:
        self.declared = declared
        self.toolScore = toolScore


@dataclass
class ClearlyDefinedDetail:
    licensed: Licensed

    def __init__(self, licensed: Licensed):
        self.licensed = licensed


class ClearlyDefinedResponse(Dict[str, ClearlyDefinedDetail]):
    pass

    @staticmethod
    def from_dict(dict_param: Dict):
        cd_response = ClearlyDefinedResponse()
        for cd_uri, cd_detail in dict_param.items():
            licended_dict = cd_detail.get("licensed")
            tool_score_dict = licended_dict.get("toolScore")

            tool_score = ToolScore(
                tool_score_dict.get("total"),
                tool_score_dict.get("declared"),
                tool_score_dict.get("discovered"),
                tool_score_dict.get("consistency"),
                tool_score_dict.get("spdx"),
                tool_score_dict.get("texts"),
            )
            licensed = Licensed(licended_dict.get("declared"), tool_score)
            detail = ClearlyDefinedDetail(licensed)
            cd_response[cd_uri] = detail
        return cd_response
