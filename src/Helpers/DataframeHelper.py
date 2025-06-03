import re

import pandas as pd
import unicodedata


class DataframeHelper:

    @staticmethod
    def remove_accents_and_capitalize(text: str) -> str:
        nfkd = unicodedata.normalize('NFKD', text)
        text = ''.join(c for c in nfkd if not unicodedata.combining(c))
        text = re.sub(r"[^A-Za-z0-9\s-]", "", text)
        text = re.sub(r'[-\s]+', ' ', text)  # Substitui múltiplos espaços e hífens por um único espaço
        return text.upper()

    @staticmethod
    def remove_accents_and_lowercase(text: str) -> str:
        nfkd = unicodedata.normalize('NFKD', text)
        text = ''.join(c for c in nfkd if not unicodedata.combining(c))
        text = re.sub(r"[^A-Za-z0-9\s-]", "", text)
        text = re.sub(r'[-\s]+', ' ', text)  # Substitui múltiplos espaços e hífens por um único espaço
        return text.lower()


    @staticmethod
    def remove_accents_and_capitalize(text: str) -> str:
        nfkd = unicodedata.normalize('NFKD', text)
        text = ''.join(c for c in nfkd if not unicodedata.combining(c))
        text = re.sub(r"[^A-Za-z0-9\s-]", "", text)
        text = re.sub(r'[-\s]+', ' ', text)  # Substitui múltiplos espaços e hífens por um único espaço
        return text.upper()