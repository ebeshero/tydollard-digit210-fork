import spacy
# Need line 8 the first time: Then comment it out after the first time you run it:
#nlp = spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')
avatarSpeeches = open('avatarSpeeches copy.txt', 'r', encoding='utf8')
words = avatarSpeeches.read()
wordstrings = str(words)
print(wordstrings)
# count=0
# for w in words:
#     count += 1
#     print(count, ": ", w)
# start playing with spaCy and nlp:
avatarWords = nlp(wordstrings)
for token in avatarWords:
    # if token.pos_ == "VERB":
    print(token.text, "---->", token.pos_, ":::::", token.lemma_)




