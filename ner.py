import stanza

stanza.download('ru')
nlp = stanza.Pipeline('ru')

def extract_addresses(text):
    addresses = []
    doc = nlp(text)
    for sentence in doc.sentences:
        for entity in sentence.entities:
            if entity.type == 'LOC':
                addresses.append(entity.text)
    return set(addresses)
