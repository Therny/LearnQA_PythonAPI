import pytest

class TestCheckLenPhrase:
    def test_check_len_phrase(self):
        phrase = input("Set a phrase: ")
        len_phrase = len(phrase)
        assert len_phrase < 15, f"Phrase have {len_phrase} symbols, it more than 15"


