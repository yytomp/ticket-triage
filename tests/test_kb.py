from kb import best_guide, words


def test_words_drops_filler_and_short_words():
    assert words("The printer is OFFLINE and I can't print") == {"printer", "offline", "print"}


def test_best_guide_picks_the_closest_match():
    guides = {
        "printer-offline": "Printer shows as offline. Remove the printer and add it again.",
        "password-reset": "Forgot your password? Use the self-service reset page.",
    }
    name, text = best_guide("My printer says offline", guides)
    assert name == "printer-offline"
    assert "Remove the printer" in text


def test_best_guide_returns_none_when_nothing_matches():
    assert best_guide("zzz qqq", {"printer-offline": "printer offline"}) == (None, "")