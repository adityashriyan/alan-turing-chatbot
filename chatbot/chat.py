"""
Orchestration for a single-turn response:
- converts Gradio's messages format into LangChain messages
- calls the chain
"""

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

from .types import Chain


class AlanTuringChat:
    """
    A thin adapter between UI chat history and a LangChain-like pipeline.

    The adapter:
      1) converts UI history (list of dicts) → LC messages
      2) calls `chain.invoke` with {"input": <user_text>, "history": <lc_messages>}
    """

    def __init__(self, chain: Chain) -> None:
        """
        Args:
            chain: Any object satisfying the `Chain` protocol (has `.invoke(dict) -> str`).
        """
        self.chain = chain

    @staticmethod
    def _gradio_to_lc(history: list[dict[str, str]]) -> list[BaseMessage]:
        """
        Convert Gradio's `type='messages'` history into LC message objects.

        Args:
            history: Messages like [{"role":"user","content":"Hi"}, {"role":"assistant","content":"Hello"}]

        Returns:
            LC messages with preserved order and roles.
        """
        lc_msgs: list[BaseMessage] = []
        for msg in history:
            role = msg.get("role")
            content = msg.get("content", "")
            if role == "user":
                lc_msgs.append(HumanMessage(content=content))
            elif role == "assistant":
                lc_msgs.append(AIMessage(content=content))
        return lc_msgs

    def respond(self, user_text: str, history: list[dict[str, str]]) -> str:
        """
        Run one conversational turn against the chain.

        Args:
            user_text: The latest user message.
            history: Full prior chat as Gradio-style messages.

        Returns:
            The assistant's reply as a string.
        """
        lc_history = self._gradio_to_lc(history)
        reply: str = self.chain.invoke({"input": user_text, "history": lc_history})
        return reply
