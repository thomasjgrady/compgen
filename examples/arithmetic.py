from compgen.grammar import (
    GrammarV1,
    LexerConfig,
    ParserConfig,
    Rule,
    TokenConfig
)
from compgen.lexer import make_lexer
from compgen.parser import make_parser


grammar = GrammarV1(
    lexer=LexerConfig(tokens={
        "INT": TokenConfig(regex=r"[0-9]+", data_callback="lambda x: int(x)"),
        "ADD": TokenConfig(regex=r"\+"),
        "MUL": TokenConfig(regex=r"\*")
    }),
    parser=ParserConfig(
        rules=[
            Rule(
                target="EXPR",
                args=[
                    "EXPR <ADD> EXPR",
                    "EXPR <MUL> EXPR",
                    "<INT>"
                ]
            )
        ]
    )
)

def main():
    lexer = make_lexer(grammar)
    parser = make_parser(grammar)
    while True:
        s = input("> ")
        tokens = lexer(s)
        ast = parser(tokens)
        print(ast.model_dump_json(indent=2))

if __name__ == "__main__":
    import fire
    fire.Fire(main)