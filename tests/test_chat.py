from chatbot.chat import AlanTuringChat


class FakeChain:
    """Mimics a LangChain chain with an invoke() method returning a string."""

    def __init__(self, reply_prefix="Turing:"):
        self.reply_prefix = reply_prefix

    def invoke(self, inputs):
        # inputs expected to be {'input': <str>, 'history': <list>}
        user = inputs.get("input", "")
        return f"{self.reply_prefix} {user[::-1]}"  # playful: reverse user text


def test_chat_respond_basic():
    chain = FakeChain()
    bot = AlanTuringChat(chain)

    history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi, how can I help?"},
    ]
    reply = bot.respond("Test", history)
    assert isinstance(reply, str)
    assert "gnitseT" not in reply  # ensure we didn't accidentally include wrong input casing
    assert reply.startswith("Turing:")


def test_chat_preserves_role_order():
    chain = FakeChain("Answer:")
    bot = AlanTuringChat(chain)

    history = [
        {"role": "user", "content": "Who are you?"},
        {"role": "assistant", "content": "I'm Alan Turing."},
        {"role": "user", "content": "Prove it."},
    ]
    reply = bot.respond("What is computation?", history)
    assert reply.startswith("Answer:")
