import nltk
import random

AGREE_FILE = 'data/agree.txt'
DISAGREE_FILE = 'data/disagree.txt'


def _read_data(file):
    return [line.strip() for line in open(file, 'r')]


def _prepare_data(data, intention_key):
    result_data = []
    for phrase in data:
        result_data.append(({'text': _pre_process_text(phrase)}, intention_key))

    return result_data


def _pre_process_text(text):
    # remove punctuation
    words = ''.join([word for word in text if word not in """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""])

    # split by words
    words = nltk.wordpunct_tokenize(words)

    # remove stop words
    words = [word for word in words if word not in nltk.corpus.stopwords.words('english')]

    # stem
    s = nltk.stem.SnowballStemmer('english')
    result = [s.stem(word) for word in words]

    return ' '.join(result).lower()


def train(train_data):
    return nltk.NaiveBayesClassifier.train(train_data)


def classify_prob(classifier, data, prob_intention):
    return classifier.prob_classify({'text': _pre_process_text(data)}).prob(prob_intention)


def classify(classifier, data):
    return classifier.classify({'text': _pre_process_text(data)})


def teach():
    agree_data = _read_data(AGREE_FILE)
    disagree_data = _read_data(DISAGREE_FILE)

    agree_data = _prepare_data(agree_data, 'AGREE')
    disagree_data = _prepare_data(disagree_data, 'DISAGREE')

    d = (agree_data + disagree_data) * 100
    random.shuffle(d)

    return train(d)


classifier = teach()
res = classify_prob(classifier, 'Yes', 'AGREE')
print(res)
res = classify(classifier, 'Yes')
print(res)
