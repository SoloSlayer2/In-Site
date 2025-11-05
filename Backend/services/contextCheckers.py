class NameEntityRecognition:
    THRESHOLD: int = 0.85

    def __init__(self, question: str):
        self.question = question

    def nerPipeline_and_Check(self):
        from transformers import pipeline

        ner = pipeline(
            task="ner",
            model="dslim/bert-base-NER",
            aggregation_strategy="simple",
        )

        raw_entities = ner(self.question)
        filtered_entities = [
            ent
            for ent in raw_entities
            if ent["score"] > NameEntityRecognition.THRESHOLD
        ]

        return self._merge_word_pieces(filtered_entities)

    def _merge_word_pieces(self, entities):
        words = []
        current = ""
        for ent in entities:
            word = ent["word"]
            if word.startswith("##"):
                current += word[2:]
            else:
                if current:
                    words.append(current)
                current = word
        if current:
            words.append(current)
        return list(set(words))  # return unique names


class KeyWordExtractor:
    import spacy
    from keybert import KeyBERT

    nlp = spacy.load("en_core_web_sm")

    def __init__(self, question):
        self.question = question
        self.kw_model = KeyWordExtractor.KeyBERT()

    def keywordExtractor(self):
        keywords = self.kw_model.extract_keywords(self.question, stop_words="english")
        filtered_keywords = []
        for word, score in keywords:
            doc = KeyWordExtractor.nlp(word)
            if not doc[0].pos_ == "VERB":  # exclude verbs
                filtered_keywords.append((word, score))
        return filtered_keywords
