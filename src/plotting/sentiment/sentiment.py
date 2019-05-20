from polyglot.text import Text

blob1 = ("Barack Obama gave a fantastic speech last night. "
        "Reports indicate he will move next to New Hampshire.")

blob2 = ("what the fuck is this shit? is it working anyway?")

blob3 = ("My bike is blue. Yours is white.")

blob4 = ("źle to idzie. Nie uda się. chuj")

# text = Text(blob)

# first_sentence = text.sentences[0]
# print(first_sentence)

# first_entity = first_sentence.entities[0]
# print(first_entity)

# first_entity.positive_sentiment


# first_entity.negative_sentiment



# print("{:<16}{}".format("Word", "Polarity")+"\n"+"-"*30)
# for w in text.words:
#     print("{:<16}{:>2}".format(w, w.polarity))

# print(text.polarity)

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()

ss = sid.polarity_scores(blob2)
for k in sorted(ss):
    print("{0}:{1},".format(k, ss[k], end='/n '))
    print