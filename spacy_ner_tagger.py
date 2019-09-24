"""
This is a minimal example to return Named Entities with the help of Spacy.
It makes use of a cached model (for frequent function use, this allows concise and clean function parameters,
while still not having to re-load the model each time.
"""

from functools import lru_cache
import spacy


def get_ner(text, lang="de"):
    """
    Expects an input string and will return the recognised named entities.
    :param text: string. Can be either a single sentence or multiple passages at once, spacy doesn't care
    :return: List of tuples. Each tuple contains (string (of NE), start_pos (character), end_pos, type)
    """

    nlp = load_spacy(lang=lang)

    doc = nlp(text)
    results = []
    for ent in doc.ents:
        results.append((ent.text, ent.start_char, ent.end_char, ent.label_))

    return results


@lru_cache(maxsize=5)
def load_spacy(lang="de"):
    """
    Also adds the sentencizer for better splitting
    :param lang: string. Either "en" for English or "de" for German
    :return:
    """
    nlp = None
    if lang == "en":
        nlp = spacy.load("en_core_web_sm")
    elif lang == "de":
        nlp = spacy.load("de_core_news_sm")
    else:
        raise ValueError("Invalid language specified")

    nlp.add_pipe(nlp.create_pipe("sentencizer"), first=True)

    return nlp
