import stanza
from spell_and_summarization import spell_txt

stanza.download('ru')
nlp = stanza.Pipeline('ru')


def extract_addresses(text):
    addresses = []
    doc = nlp(text)
    for sentence in doc.sentences:
        for entity in sentence.entities:
            if entity.type == 'LOC':
                addresses.append(entity.text)
    addr = ' '.join(list(set(addresses)))
    addr = spell_txt(addr)
    return addr
