import re

def sentence_split(text: str):
    """
    Split text into clean sentences.
    """
    text = text.strip().replace("\n", " ")
    parts = re.split(r'(?<=[\.\?\!])\s+(?=[A-Z0-9"])', text)
    return [p.strip() for p in parts if len(p.strip()) > 10]
