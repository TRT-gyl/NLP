import jieba
import mammoth
import numpy as np
import streamlit as st
import jieba.posseg as pseg
import save
import train
import Summary
import time
import CorrectDocx
from LAC import LAC
from pysbd import Segmenter
from docx import Document
import webbrowser

# --server.enableXsrfProtection=false


def remove_duplicates(lst):
    return list(dict.fromkeys(lst))


def processing():
    word0 = st.empty()
    bar = st.progress(0)
    for i in range(100):
        word0.subheader('人名标注进度: ' + str(i + 1) + '%')
        bar.progress(i + 1)
        time.sleep(0.01)


def processing1():
    word0 = st.empty()
    bar = st.progress(0)
    for i in range(100):
        word0.subheader('单词错位校对进度: ' + str(i + 1) + '%')
        bar.progress(i + 1)
        time.sleep(0.01)


def processing2():
    word0 = st.empty()
    bar = st.progress(0)
    for i in range(100):
        word0.subheader('训练专有LAC分词&词法分析模型进度: ' + str(i + 1) + '%')
        bar.progress(i + 1)
        time.sleep(0.01)

# "🦈" ":dolphin:" ":rocket:"


def main():
    global text, text_area, llac, llac1
    st.set_page_config(page_title="SummerTask",  page_icon=":dolphin:", layout="wide", initial_sidebar_state="expanded",
                       menu_items={'Get Help': 'https://docs.streamlit.io/',
                                   'About': "# 暑期任务"})
    st.sidebar.title('暑期任务')
    page = st.sidebar.radio("选择一个任务", ["英文文本单词错误校对", "中文人名识别-标注", "中文人名识别-模型训练识别", "中文摘要生成", "test"])

    if page == "英文文本单词错误校对":
        # webbrowser.open("http://localhost:8502", new=0)
        st.title("英文文本单词错误校对：")
        st.write("Tips:  编写一个英文文本单词错误校对的软件，能够对英文文本中的错误进行发现，并予以更正")

        uploader = st.file_uploader('选择错误校对文件上传', type=['txt', 'docx'])
        if uploader is not None:
            if uploader.name.split('.')[-1] == 'docx':
                text = mammoth.convert_to_markdown(uploader).value
            elif uploader.name.split('.')[-1] == 'txt':
                text = uploader.read().decode("utf-8")
            # st.subheader("原文：")
            show_text = text
            text_area = st.text_area(label='校对原文：', value=show_text, height=260)
            if text_area is not None:
                button = st.button("开始错误校对")
                # 在按钮被点击时执行的操作
                if button:
                    docx_file = uploader.name
                    CorrectDocx.write_correct_paragraph(docx_file)
                    processing1()
                    sum0 = CorrectDocx.get_count_correct()
                    st.subheader("错误单词校对数："+str(sum0)+"个")
                    readword_address = CorrectDocx.readword()
                    texts = mammoth.convert_to_markdown(readword_address).value
                    if texts is not None:
                        st.subheader('英文文本单词错误校对---保存路径：' + CorrectDocx.readword())
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.subheader("校对原文：")
                        st.text_area(label='', value=text, height=300, key='text')
                    with col2:
                        st.subheader("校对结果：")
                        st.text_area(label='', value=texts, height=300, key='texts')

    elif page == "中文人名识别-标注":
        st.title("中文人名识别")
        st.write("Tips:  编写一个中文人名识别软件，将一篇中文文本中的人名识别出来并标红")
        lac = LAC(mode='seg')
        lac1 = LAC(mode='lac')
        uploaded = st.file_uploader("请上传需处理的DOCX或者TXT文件", type=['docx', 'txt'])
        if uploaded is not None:
            if uploaded.name.split('.')[-1] == 'docx':
                text = mammoth.convert_to_markdown(uploaded).value
            elif uploaded.name.split('.')[-1] == 'txt':
                text = uploaded.read().decode("utf-8")
            docx_file = uploaded.name
            st.header("原文：")
            # with st.container():

            st.text_area(label='', value=text, height=300)
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

            choice = st.selectbox(label='请选择分类分词结果完成中文人名标注', options=('jieba规则人名识别结果', 'LAC模型人名识别结果', 'jieba&LAC模型综合识别', ''), index=3, format_func=str, help='如果不选择默认使用效果最好的一个识别结果')
            if choice == 'jieba规则人名识别结果':
                save.main(unique_lists, docx_file)
                processing()
                st.subheader('标注人名文件---保存路径：' + save.readword())
            elif choice == 'LAC模型人名识别结果':
                save.main(namesss, docx_file)
                processing()
                st.subheader('标注人名文件---保存路径：' + save.readword())
            elif choice == 'jieba&LAC模型综合识别':
                save.main(namesss, docx_file)
                processing()
                st.subheader('标注人名文件---保存路径：' + save.readword())

    elif page == "中文人名识别-模型训练识别":
        st.title("中文人名识别-模型训练识别")

        st.subheader('step1、训练专有LAC分词&词法分析模型')
        button = st.button("训练专有LAC模型")
        llac = train.seg_train()
        llac1 = train.lac_train()
        if button:
            processing2()
        st.subheader('step2、上传识别文档')
        uploaded = st.file_uploader("", type=['docx'])
        if uploaded is not None:
            docx_file = uploaded.name
            text = mammoth.convert_to_markdown(uploaded).value
            st.subheader("原文：")
            st.text_area(label='', value=text, height=300)
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
                save.main(namesss, docx_file)
                processing()
                st.subheader('标注人名文件---保存路径：' + save.readword())

    elif page == "中文摘要生成":
        st.title("中文摘要生成")
        st.write("Tips:  利用Bart预训练模型编写一个中文摘要生成的程序")
        Summary.output_abstracts()

    elif page == "test":

        st.markdown("# 绘图演示")
        st.sidebar.header("绘图演示")
        st.write(
            """这个演示展示了 Streamlit 的绘图和动画组合。我们在一个循环中生成一些随机数大约5秒钟。希望你喜欢！"""
        )

        progress_bar = st.sidebar.progress(0)
        status_text = st.sidebar.empty()
        last_rows = np.random.randn(1, 1)
        chart = st.line_chart(last_rows)

        for i in range(1, 101):
            new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
            status_text.text("完成%i%%" % i)
            chart.add_rows(new_rows)
            progress_bar.progress(i)
            last_rows = new_rows
            time.sleep(0.05)

        progress_bar.empty()

        # Streamlit 的部件会自动按顺序运行脚本。由于此按钮与任何其他逻辑都没有连接，因此它只会引起简单的重新运行。
        st.button("重新运行")

if __name__ == "__main__":
    main()