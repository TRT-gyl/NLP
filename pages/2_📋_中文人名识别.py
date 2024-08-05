import jieba
import mammoth
import save
import time
import streamlit as st
import jieba.posseg as pseg
from LAC import LAC


def remove_duplicates(lst):
    return list(dict.fromkeys(lst))


def processing():
    st.sidebar.header("中文人名识别进度")
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    for i in range(1, 101):
        status_text.text("人名标注进度%i%%" % i)
        progress_bar.progress(i)
        time.sleep(0.01)
    # progress_bar.empty()


def show_detail(detail_text, list):
    # 使用Markdown语法设置字体颜色
    for i in range(len(list)):
        colored_text = f"<span style='color:red'>{list[i]}</span>"
        detail_text = detail_text.replace(list[i], colored_text)
    st.markdown(detail_text, unsafe_allow_html=True)
    return detail_text


st.set_page_config(page_title="中文人名识别", page_icon="📋", layout="wide")

st.title("中文人名识别")
st.write("Tips:  编写一个中文人名识别软件，将一篇中文文本中的人名识别出来并标红")
lac = LAC(mode='seg')
lac1 = LAC(mode='lac')
lac.load_customization('./task2_data/dict.txt')
lac1.load_customization('./task2_data/dict.txt')
st.markdown("""**请上传需处理的DOCX或者TXT文件：**""")
uploaded = st.file_uploader("请上传需处理的DOCX或者TXT文件", type=['docx', 'txt'], label_visibility="collapsed")
if uploaded is not None:
    if uploaded.name.split('.')[-1] == 'docx':
        text = mammoth.convert_to_markdown(uploaded).value
    elif uploaded.name.split('.')[-1] == 'txt':
        text = uploaded.read().decode("utf-8")
    docx_file = uploaded.name
    st.header("原文：")
    st.text_area(label='原文', value=text, height=300, label_visibility="collapsed")
    content = jieba.lcut(text, use_paddle=True)
    seg_result = lac.run(text)
    names = []
    namess = []
    namesss = []
    ls = []
    ls1 = []

    lac_result = lac1.run(seg_result)
    for i in range(len(lac_result)):
        ls.append(lac_result[i])
        ls1.append(sum(ls[i], []))
    for i in range(len(ls1)):
        if "PER" in ls1[i]:
            names.append(ls1[i])
    words = pseg.lcut(text, HMM=True, use_paddle=True)
    column = [row[0] for row in names]
    col1, col2, col3, col4 = st.columns([1, 1.1, 1, 1.1])
    with col1:
        st.subheader("jieba分词结果：")
        st.write(content)
    with col2:
        st.subheader("jieba标注词性结果：")
        st.write(words)
    with col3:
        st.subheader("LAC分词结果：")
        st.write(seg_result)
    with col4:
        st.subheader("LAC标注词性结果：")
        st.write(ls1)
    unique_list = remove_duplicates(column)
    min_length = 1
    longest_string = ""
    for s in unique_list:
        if len(s) > min_length:
            longest_string = s
            namesss.append(longest_string)
    for word, flag in words:
        if flag == 'nr':  # 人名
            if len(word) > min_length:
                namess.append(word)
    unique_lists = remove_duplicates(namess)
    col4, col5 = st.columns([1, 1])
    with col4:
        st.subheader("jieba规则人名识别结果：")
        st.write(unique_lists)
    with col5:
        st.subheader("LAC模型人名识别结果：")
        st.write(namesss)
    st.markdown("""**请选择分类分词结果完成中文人名标注：**""")
    choice = st.selectbox(label='请选择分类分词结果完成中文人名标注', options=('jieba规则人名识别结果', 'LAC模型人名识别结果', ''),
                          index=2, format_func=str, help='如果不选择默认使用效果最好的一个识别结果', label_visibility="collapsed")
    if choice == 'jieba规则人名识别结果':
        st.divider()
        st.subheader('标注结果显示：')
        show_detail(text, unique_lists)
        save.main(unique_lists, docx_file)
        processing()
        st.subheader('标注人名文件---保存路径：' + save.readword())
    elif choice == 'LAC模型人名识别结果':
        st.divider()
        st.subheader('标注结果显示：')
        show_detail(text, namesss)
        save.main(namesss, docx_file)
        processing()
        st.subheader('标注人名文件---保存路径：' + save.readword())

