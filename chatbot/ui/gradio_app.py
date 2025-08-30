"""
Gradio Blocks UI for the Alan Turing Chatbot.
"""

import gradio as gr
from dotenv import load_dotenv

from ..chat import AlanTuringChat
from ..llm import build_chain


def launch(share: bool = False) -> None:
    """
    Launch the Gradio UI.

    Args:
        share: If True, Gradio shares a public link (use with caution).
    """
    load_dotenv()
    chain = build_chain()
    bot = AlanTuringChat(chain)

    def chat_fn(msg: str, history: list[dict[str, str]]) -> tuple[str, list[dict[str, str]]]:
        """
        Gradio callback to process a user message and update the chat.
        """
        reply = bot.respond(msg, history)
        new_history = history + [
            {"role": "user", "content": msg},
            {"role": "assistant", "content": reply},
        ]
        return "", new_history

    def clear_fn() -> tuple[str, list[dict[str, str]]]:
        """
        Clear the textbox and chat history.
        """
        return "", []

    with gr.Blocks(title="Chat with Alan Turing", theme=gr.themes.Soft()) as page:
        gr.Markdown(
            """
            # Alan Turing Chatbot
            Welcome to your personal conversation with Alan Turing!
            """
        )
        chatbot = gr.Chatbot(
            type="messages", avatar_images=(None, "assets/AlanTuring.jpg"), show_label=False
        )

        msg = gr.Textbox(show_label=False, placeholder="Ask Alan anything...")

        msg.submit(chat_fn, [msg, chatbot], [msg, chatbot])

        clear = gr.Button("Clear Chat", variant="secondary")
        clear.click(clear_fn, outputs=[msg, chatbot])

    page.launch(share=share)
