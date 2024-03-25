from string import punctuation

import nltk
import pymorphy3

from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

nltk.download("punkt")
nltk.download("stopwords")


morph = pymorphy3.MorphAnalyzer()
punctuations = list(punctuation)
stopwords = nltk.corpus.stopwords.words("russian")


def preprocessing(text: str) -> list:
    """
    Функция обработки текста. Возвращает список "очищенных" слов
    """
    tokens = word_tokenize(text)                                        # Токенизация текста
    tokens_without_punct = [i for i in tokens if i not in punctuations] # Удаление знаков пунктуации
    low_tokens = [i.lower() for i in tokens_without_punct]              # Перевод текста в нижний регистр
    words_without_stop = [i for i in low_tokens if i not in stopwords]  # Удаление стоп-слов
    lemms = [morph.parse(i)[0].normal_form for i in words_without_stop] # Лемматизация
    final_without_empty_strings = [i for i in lemms if i != ""]

    return final_without_empty_strings


def calc_tf(data: list, length: int) -> list:
    """
    Рассчитывает общий показатель TF для каждого слова
    """
    ans = [0] * length

    for x in range(len(data[0])):
        for y in range(length):
            ans[x] += data[y][x]

    return ans


def tf_idf_calculation(preprocessed_data: list) -> tuple[list]:
    count_vectorizer = CountVectorizer()
    count_vectorizer.fit_transform(preprocessed_data)

    word_dict = count_vectorizer.vocabulary_ # {word: index}

    freq_term_matrix = count_vectorizer.transform(preprocessed_data)

    array = freq_term_matrix.toarray() # [index: tf]
    array_tf = calc_tf(array, len(word_dict))

    tfidf = TfidfTransformer()
    tfidf.fit(freq_term_matrix)

    array_idf = list(tfidf.idf_) # [index: idf]

    return sorted(word_dict), array_tf, array_idf


def present_results(word_dict: list, tf: list, idf: list) -> list[tuple]:
    """
    Возвращает 50 слов с наибольшим показателем IDF
    """
    ans = [(word, tf_score, idf_score) for word, tf_score, idf_score in sorted(zip(word_dict, tf, idf), key=lambda x: x[2], reverse=True)][:50]

    return ans
