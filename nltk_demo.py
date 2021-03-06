import nltk

def gender_features(word):
    return {'last_letter': word[-1]}


gender_features('Shrek')
# {'last_letter': 'k'}


from nltk.corpus import names

labeled_names = (
    [(name, 'male') for name in names.words('male.txt')] +
    [(name, 'female') for name in names.words('female.txt')]
)
import random

random.shuffle(labeled_names)

featuresets = [
    (gender_features(n), gender) for (n, gender) in labeled_names
    ]
train_set, test_set = featuresets[500:], featuresets[:500]

classifier = nltk.NaiveBayesClassifier.train(train_set)

print(classifier.classify(gender_features('Neo')))
# 'male'
print(classifier.classify(gender_features('Trinity')))
# 'female'
