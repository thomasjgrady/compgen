from compgen.grammar import GrammarV1, LexerConfig, ParserConfig, Rule, TokenConfig
from compgen.lexer import make_lexer


grammar = GrammarV1(
    lexer=LexerConfig(
        tokens={
            "INT": TokenConfig(regex=r"[0-9]+", data_callback=f"lambda x: int(x)"),
            "ADD": TokenConfig(regex=r"\+"),
            "MUL": TokenConfig(regex=r"\*")
        }
    ),
    parser=ParserConfig(
        rules=[
            Rule(target="EXPR", args=[
                "EXPR <ADD> EXPR",
                "EXPR <MUL> EXPR",
                "<INT>"
            ])
        ]
    )
)

def test_arithmetic_grammar_lexer():

    lexer = make_lexer(grammar)

    tokens = lexer("5 + 6 * 9012 + 10")
    token_names = [t.data.name for t in tokens]
    assert token_names == [
        "INT",
        "ADD",
        "INT",
        "MUL",
        "INT",
        "ADD",
        "INT"
    ]

    token_values = [t.data.value for t in tokens]
    assert token_values == [
        5,
        None,
        6,
        None,
        9012,
        None,
        10
    ]