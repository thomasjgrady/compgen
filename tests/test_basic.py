from tempfile import NamedTemporaryFile
import json

import pytest

from compgen.grammar import GrammarV1, read_grammar_file


def test_grammar_file_version() -> None:

    with NamedTemporaryFile(mode="w", suffix=".gmr") as f:
        s = json.dumps({
            "version": "1",
            "lexer": {
                "tokens": {}
            },
            "parser": {
                "rules": []
            }
        })
        f.write(s)
        f.flush()
        g = read_grammar_file(f.name)
        assert isinstance(g, GrammarV1)

    with NamedTemporaryFile(mode="w", suffix=".gmr") as f:
        s = json.dumps({
            "version": "-1",
            "lexer": {
                "tokens": {}
            },
            "parser": {
                "rules": []
            }
        })
        f.write(s)
        f.flush()
        with pytest.raises(ValueError):
            g = read_grammar_file(f.name)