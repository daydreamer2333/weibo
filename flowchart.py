#情感分析
import nltk
import nltk.sentiment.sentiment_analyzer
def wordBasedSentiment():
    positive_words = ['love','hope','joy']
    text = 'rainfall this year brings lots of joy and hope for farmers'.split()
    analysis = nltk.sentiment.util.extract_unigram_feats(text,positive_words)
    print('--single word sentiment--')
    print(analysis)
def multiWordBasedSentiment():
    word_sets = [('heavy','rains'),('flood','bengaluru')]
    text = 'heavy rains cause flash flooding in bengaluru'.split()
    analysis =  nltk.sentiment.util.extract_bigram_feats(text,word_sets)
    print('--multi word sentiment--')
    print(analysis)
def markNegativity():
    text = 'rainfall this year brings lots of joy and hope for farmers'.split()
    negation = nltk.sentiment.util.mark_negation(text)
    print('--negativity--')
    print(negation)
if __name__ == '__main__':
    wordBasedSentiment()
    multiWordBasedSentiment()
    markNegativity()