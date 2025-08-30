import pytest

# We’ll test the public API of chatbot.llm without making real API calls.


def test_build_model_requires_api_key(monkeypatch):
    import chatbot.llm as llm

    # Ensure no key is visible
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    # …and make load_dotenv() a no-op so it can't repopulate from .env
    monkeypatch.setattr(llm, "load_dotenv", lambda *a, **k: False)

    with pytest.raises(RuntimeError):
        llm.build_model()


def test_build_model_with_key(monkeypatch):
    import chatbot.llm as llm

    # Fake a Google key
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    # Stub the real model class so we don't import/network anything heavy
    class FakeModel:
        def __init__(self, model: str, api_key: str, temperature: float):
            self.model = model
            self.api_key = api_key
            self.temperature = temperature

    monkeypatch.setattr(llm, "ChatGoogleGenerativeAI", FakeModel)

    mdl = llm.build_model(model="gemini-1.5-pro", temperature=0.5)
    assert isinstance(mdl, FakeModel)
    assert mdl.api_key == "test-key"
    assert mdl.temperature == 0.5


def test_build_chain_returns_invokable_chain(monkeypatch):
    import chatbot.llm as llm

    # Provide a minimal pipeline that supports the `|` composition and `.invoke(...)`
    class FakeSeq:
        def __or__(self, _other):
            return self

        def invoke(self, _inputs):
            return "ok"

    class FakePrompt:
        def __or__(self, _other):
            return FakeSeq()

    class FakePromptTemplate:
        @staticmethod
        def from_messages(_msgs):
            return FakePrompt()

    class FakeParser:
        pass

    class FakeModel:
        pass

    monkeypatch.setattr(llm, "ChatPromptTemplate", FakePromptTemplate)
    monkeypatch.setattr(llm, "StrOutputParser", lambda: FakeParser())

    chain = llm.build_chain(model=FakeModel())
    assert hasattr(chain, "invoke")
    assert chain.invoke({"input": "hi", "history": []}) == "ok"
