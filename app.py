
import os

import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

nltk.data.path.append(os.path.abspath("nltk_data"))



ps = PorterStemmer()


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


cv = pickle.load(open('countVectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))
st.title("Movie Review Sentiment Analysis")
txt = st.text_area(
    "Text to analyze",

    )

st.write(f'You wrote {len(txt)} characters.')



if st.button('Submit', type="primary"):

    # 1. preprocess
    transformed_sms = transform_text(txt)

    # 2. vectorize
    vector_input = cv.transform([transformed_sms])
    # 3. predict
    result = model.predict(vector_input)[0]
    # 4. Display
    if result == 1:
        st.header("Positive Review")
    else:
        st.header("Negative Review")