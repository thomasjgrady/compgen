import json
from typing import Any, Dict, List, Optional, Type
from pydantic import BaseModel


class TokenConfig(BaseModel, extra="forbid"):
    regex: str
    data_callback: Optional[str] = None

class LexerConfig(BaseModel, extra="forbid"):
    tokens: Dict[str, TokenConfig]

class Rule(BaseModel, extra="forbid"):
    target: str
    args: List[str]

class ParserConfig(BaseModel, extra="forbid"):
    rules: List[Rule]

class GrammarV1(BaseModel, extra="forbid"):
    lexer: LexerConfig
    parser: ParserConfig

Grammar = GrammarV1

GRAMMAR_VERSION = "1"
GRAMMAR_VERSION_MAP: Dict[str, Type[Grammar]] = {
    "1": GrammarV1
}

def read_grammar_file(file_path: str) -> Grammar:

    with open(file_path, "r") as f:
        data: Dict[str, Any] = json.load(f)

    version = data.pop("version", GRAMMAR_VERSION)
    if version in GRAMMAR_VERSION_MAP:
        cls = GRAMMAR_VERSION_MAP[version]
        return cls(**data)
    else:
        raise ValueError(f"Invalid grammar file version: {version}")