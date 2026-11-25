from llm import build_prompt, parse_response


def test_parse_clean_json():
    result = parse_response('{"category": "printing", "urgency": "low", "reply": "Try this."}')
    assert result == {"category": "printing", "urgency": "low", "reply": "Try this."}


def test_parse_json_with_extra_text_around_it():
    text = 'Sure! Here you go:\n{"category": "network", "urgency": "high", "reply": "On it."}\nHope that helps.'
    assert parse_response(text)["category"] == "network"


def test_unknown_values_fall_back():
    result = parse_response('{"category": "coffee machine", "urgency": "panic", "reply": "Hi"}')
    assert result["category"] == "other"
    assert result["urgency"] == "medium"


def test_garbage_falls_back():
    assert parse_response("I don't know")["category"] == "other"
    assert parse_response("[1, 2, 3]")["category"] == "other"


def test_prompt_contains_the_ticket_and_guide():
    prompt = build_prompt("Locked out", "Too many attempts", "Wait 15 minutes")
    assert "Locked out" in prompt
    assert "Wait 15 minutes" in prompt
    assert "account_access" in prompt