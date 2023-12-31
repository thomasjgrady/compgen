from typing import Any, Callable, List, Optional, Tuple
from .grammar import Grammar, GrammarV1
from pydantic import BaseModel
import re


class TokenData(BaseModel, extra="forbid"):
    name: str
    value: Optional[Any] = None

class TokenMeta(BaseModel, extra="forbid"):
    span: Tuple[int, int]

class Token(BaseModel, extra="forbid"):
    data: TokenData
    meta: TokenMeta

Lexer = Callable[[str], List[Token]]

def make_lexer_v1(grammar: GrammarV1) -> Lexer:
    def lexer(s: str) -> List[Token]:

        i = 0
        tokens = []

        while i < len(s):
            if s[i].isspace():
                i += 1
                continue
            found = False
            for token_name, token_config in grammar.lexer.tokens.items():
                m = re.match(token_config.regex, s[i:])
                if m is not None:
                    span = m.span()
                    if span[0] == 0:

                        start = span[0] + i
                        stop = span[1] + i
                        value = None

                        if token_config.data_callback is not None:
                            f = eval(token_config.data_callback)
                            match_str = s[start:stop]
                            value = f(match_str)

                        token_data = TokenData(
                            name=token_name,
                            value=value
                        )

                        token_meta = TokenMeta(
                            span=(start, stop)
                        )

                        tokens.append(Token(data=token_data, meta=token_meta))

                        found = True
                        i = stop

                if found:
                    break
            
            if not found:
                raise ValueError("Unknown symbol")
        
        return tokens
    
    return lexer

def make_lexer(grammar: Grammar) -> Lexer:
    
    if isinstance(grammar, GrammarV1):
        return make_lexer_v1(grammar)           
    else:
        raise ValueError(f"Unsupported grammar type: {type(grammar)}")