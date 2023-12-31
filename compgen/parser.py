from typing import Any, Callable, List, Optional, Tuple
from pydantic import BaseModel
from .grammar import Grammar, GrammarV1
from .lexer import Token
from .utils import find_sublist_range, find_contiguous_ranges


class Expression(BaseModel, extra="forbid"):
    data: Optional[Any]
    args: Optional[List["Expression"]]

Parser = Callable[[List[Token]], Expression]

def make_parser_v1(grammar: GrammarV1) -> Parser:

    token_names = set(grammar.lexer.tokens.keys())
    expr_names = set(rule.target for rule in grammar.parser.rules)
    
    def parse_token_name(s: str) -> Optional[str]:
        if s.startswith("<") and s.endswith(">") and s[1:-1] in token_names:
            return s[1:-1]

    def parser(tokens: List[Token], target: Optional[str] = None) -> Expression:
        
        if target is not None:
            assert target in expr_names

        for rule in grammar.parser.rules:
            
            if target is not None and rule.target != target:
                continue

            for arg in rule.args:
                
                arg_def = arg.split()

                rule_token_ranges = find_contiguous_ranges(
                    arg_def,
                    lambda s: parse_token_name(s) is not None
                )

                token_names = [token.data.name for token in tokens]
                patterns = [[parse_token_name(x) for x in arg_def[a:b]] for (a, b) in rule_token_ranges]
                
                token_ranges = []
                match = True
                i = 0

                for p in patterns:
                    r = find_sublist_range(token_names[i:], p) # type: ignore
                    if r is None:
                        match = False
                        break
                    token_ranges.append((r[0]+i, r[1]+i))

                if match:

                    expr_ranges = []
                    if len(token_ranges) == 0:
                        # should be fine because we enforce that there are no
                        # two consecutive expressions in grammar def
                        expr_ranges.append((0, len(tokens)))

                    else:

                        if token_ranges[0][0] > 0:
                            expr_ranges.append((0, token_ranges[0][0]))
                            
                        for r0, r1 in zip(token_ranges[::2], token_ranges[1::2]):
                            expr_ranges.append((r0[1], r1[0]))

                        if token_ranges[-1][1] < len(tokens):
                            expr_ranges.append((token_ranges[-1][1], len(tokens)))

                    # No subexpressions, this is a leaf node
                    expr_tokens = [tokens[a:b] for a, b in token_ranges]
                    if len(expr_ranges) == 0:
                        return Expression(
                            data={ "tokens": expr_tokens },
                            args=None
                        )
                    
                    # Recursively parse
                    else:
                        arg_exprs = [e for e in arg_def if e in expr_names]
                        assert len(arg_exprs) == len(expr_ranges)
                        subargs = []
                        for target, (a, b) in zip(arg_exprs, expr_ranges):
                            subargs.append(parser(tokens[a:b], target=target))

                        return Expression(
                            data={ "tokens": expr_tokens },
                            args=subargs
                        )

        raise ValueError(f"Tokens {tokens} did not match any rule")

    return parser

def make_parser(grammar: Grammar) -> Parser:
    if isinstance(grammar, GrammarV1):
        return make_parser_v1(grammar)
    else:
        raise ValueError(f"Unsupported grammar type: {type(grammar)}")