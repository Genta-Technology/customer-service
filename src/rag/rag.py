"""
This is the file in which the process of langchain and prompt system is defined.
"""

def rag_main(chat_history: list, system: str):
    """
    Run the main function of the langchain, the only function that can be called outside
    """

    copy_chat_history = chat_history.copy()

    copy_chat_history.insert(0, {"role":"system", "content":system})

    return copy_chat_history
