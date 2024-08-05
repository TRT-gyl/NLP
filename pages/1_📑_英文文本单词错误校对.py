import mammoth
import time
import streamlit as st
import CorrectDocx


def processing():
    st.sidebar.header("英文文本单词错误校对")
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    for i in range(1, 101):
        status_text.text("错误单词校对进度%i%%" % i)
        progress_bar.progress(i)
        time.sleep(0.01)
    # progress_bar.empty()


st.set_page_config(page_title="英文文本单词错误校对", page_icon="📑", layout="wide")
st.title("英文文本单词错误校对")
st.write("Tips:  编写一个英文文本单词错误校对的软件，能够对英文文本中的错误进行发现，并予以更正")
st.markdown("""**选择错误校对文件上传：**""")
uploader = st.file_uploader('选择错误校对文件上传', type=['txt', 'docx'], label_visibility="collapsed")
if uploader is not None:
    if uploader.name.split('.')[-1] == 'docx':
        text = mammoth.convert_to_markdown(uploader).value
    elif uploader.name.split('.')[-1] == 'txt':
        text = uploader.read().decode("utf-8")
    show_text = text
    st.subheader('校对原文：')
    text_area = st.text_area(label='校对原文：', value=show_text, height=260, label_visibility="collapsed")
    if text_area is not None:
        button = st.button("开始错误校对")
        # 在按钮被点击时执行的操作
        if button:
            st.divider()
            docx_file = uploader.name
            CorrectDocx.write_correct_paragraph(docx_file)
            processing()
            sum0 = CorrectDocx.get_count_correct()
            st.subheader("错误单词校对数："+str(sum0)+"个")
            readword_address = CorrectDocx.readword()
            texts = mammoth.convert_to_markdown(readword_address).value
            if texts is not None:
                st.subheader('英文文本单词错误校对---保存路径：' + CorrectDocx.readword())
            col1, col2 = st.columns([1, 1])
            with col1:
                st.subheader("校对原文：")
                st.text_area(label='校对原文', value=text, height=300, key='text', label_visibility="collapsed")
            with col2:
                st.subheader("校对结果：")
                st.text_area(label='校对结果', value=texts, height=300, key='texts', label_visibility="collapsed")
