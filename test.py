# import streamlit as st
# import webbrowser
# st.sidebar.title("Navigation")
# selection = st.sidebar.radio("Go to", ["Home", "Page 1", "Page 2"])
#
# if st.button("跳转到Demo"):
#     webbrowser.open("http://localhost:8501",new=2)

# import pkuseg
#
# # 示例中文文本
# text = "这是一个示例句子。这是另一个！这个怎么样？让我们试试看。"
#
# # 配置pkuseg
# seg = pkuseg.pkuseg()
#
# # 将文本切分为句子
# sentences = seg.cut(text)
#
# # 输出切分后的句子
# for i, sentence in enumerate(sentences):
#     print(f"句子 {i + 1}: {sentence}")

#pip install spacy
#python -m spacy download en_core_web_sm


import string

def strip_punctuation(text):
    return ''.join([c for c in text if c not in string.punctuation])
#
# text = "Hello, world!"
# result = strip_punctuation(text)
# print(result) # 输出: Hello world
#

# 利用nltk库来实现分词和分单词
import nltk.data
data = 'This is the first sentence. This is the second sentence. And this is the third sentence. This is the first sentence, This is the second sentence! This is the first sentence. This is the second sentence? And this is the third sentence. And this is the third sentence.'

tokenizer = nltk.data.load('./task1_data/english.pickle')
list_ret = list()
word_list = list()
for row in tokenizer.tokenize(data):
    list_ret.append(row)
    # print(row)
print(list_ret)


for i in range(len(list_ret)):
    sentence = strip_punctuation(list_ret[i])
    word_list.append(sentence.split())
    # wordss = [word for word in list_ret[i].split()]
print(word_list)
    # print(wordss)