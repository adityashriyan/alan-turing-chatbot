from chatbot.prompts import system_prompt


def test_system_prompt_has_key_traits():
    assert isinstance(system_prompt, str)
    assert "Alan Turing" in system_prompt
    # sanity checks to enforce style constraints exist
    for phrase in ["concise", "well-reasoned", "plain English"]:
        assert phrase.lower() in system_prompt.lower()
