import mammoth
import streamlit as st
import save
import train
import time


def processing():
    st.sidebar.header("中文人名识别进度")
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    for i in range(1, 101):
        status_text.text("人名标注进度：%i%%" % i)
        progress_bar.progress(i)
        time.sleep(0.01)
    # progress_bar.empty()


def processing1():
    st.sidebar.header("LAC模型训练进度")
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    for i in range(1, 101):
        status_text.text("训练专有LAC分词&词法分析模型进度：%i%%" % i)
        progress_bar.progress(i)
        time.sleep(0.01)
    # progress_bar.empty()


def show_detail(detail_text, list):
    for i in range(len(list)):
        position = detail_text.find("鲁迅")
        colored_text = f"<span style='color:red'>{list[i]}</span>"
        detail_text = detail_text.replace(list[i], colored_text)
    st.markdown(detail_text, unsafe_allow_html=True)
    return detail_text


def remove_duplicates(lst):
    return list(dict.fromkeys(lst))


st.set_page_config(page_title="中文人名识别-模型训练识别", page_icon="📊", layout="wide")
st.title("中文人名识别-模型训练识别")
st.subheader('step1、训练专有LAC分词&词法分析模型')
button = st.button("训练专有LAC模型")
llac = train.seg_train()
llac1 = train.lac_train()
llac.load_customization('./task2_data/dict.txt')
llac1.load_customization('./task2_data/dict.txt')
if button:
    processing1()
st.subheader('step2、上传识别文档')
st.markdown("""**上传识别文档：**""")
uploaded = st.file_uploader("上传识别文档", type=['docx'], label_visibility="collapsed")
if uploaded is not None:
    docx_file = uploaded.name
    text = mammoth.convert_to_markdown(uploaded).value
    st.subheader("原文：")
    st.text_area(label='原文', value=text, height=300, label_visibility="collapsed")
    seg_result = llac.run(text)
    names = []
    namesss = []
    ls = []
    ls1 = []
    lac_result = llac1.run(seg_result)
    for i in range(len(lac_result)):
        ls.append(lac_result[i])
        ls1.append(sum(ls[i], []))
    for i in range(len(ls1)):
        if "PER" in ls1[i]:
            names.append(ls1[i])
    column = [row[0] for row in names]
    unique_list = remove_duplicates(column)
    min_length = 1
    longest_string = ""
    for s in unique_list:
        if len(s) > min_length:
            longest_string = s
            namesss.append(longest_string)
    col1, col2, col3 = st.columns([1, 1, 1.2])
    with col1:
        st.subheader("LAC分词结果：")
        st.write(seg_result)
    with col2:
        st.subheader("LAC标注词性结果：")
        st.write(ls1)
    with col3:
        st.subheader("LAC模型中文名字识别结果：")
        st.write(namesss)
    button = st.button("标注人名文件")
    if button:
        st.divider()
        st.subheader('标注结果显示：')
        show_detail(text, namesss)
        save.main(namesss, docx_file)
        processing()
        st.subheader('标注人名文件---保存路径：' + save.readword())


