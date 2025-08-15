from langdetect import detect, LangDetectException
from typing import Dict

def route_by_language(text: str) -> Dict[str, str]:
    """
    detects the language of a given text and provides a routing suggestion.

    Args:
        text: The input string to analyze.

    Returns:
        dictionary containing the detected language and a routing action.
    """
    try:
        lang_code = detect(text)
        if lang_code == "ar":
            return {"language": "Arabic", "route_to": "arabic_support_queue"}
        else:
            return {"language": "English", "route_to": "english_support_queue"}
    except LangDetectException:
        # If language cannot be detected, default to English
        return {"language": "Unknown", "route_to": "english_support_queue"}