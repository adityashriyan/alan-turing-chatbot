def test_public_contracts():
    import chatbot

    assert hasattr(chatbot, "__all__")
    exported = set(chatbot.__all__)
    # We expect these modules to remain part of the public API
    for name in {"prompts", "llm", "chat"}:
        assert name in exported
