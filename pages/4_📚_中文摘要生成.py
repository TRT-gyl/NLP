import mammoth
import streamlit as st
import time
from transformers import (AutoTokenizer,
                          BartForConditionalGeneration)


def processing():
    st.sidebar.header("中文摘要生成")
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    for i in range(1, 101):

        status_text.text("中文摘要生成进度：%i%%" % i)
        progress_bar.progress(i)
        time.sleep(0.01)

    # progress_bar.empty()


st.set_page_config(page_title="中文摘要生成", page_icon="📚", layout="wide")
st.title("中文摘要生成")
st.write("Tips:  利用Bart预训练模型编写一个中文摘要生成的程序")
tokenizer = AutoTokenizer.from_pretrained("./huggingface/bart-base-chinese")
text = []
model = BartForConditionalGeneration.from_pretrained("./huggingface/best")
st.write("中文摘要训练模型加载完毕---模型位置./huggingface/best")
print("中文摘要训练模型加载完毕")
st.markdown("""**选择需要中文文本摘要生成的文件上传：**""")
uploader = st.file_uploader('选择需要中文文本摘要生成的文件上传：', type=['txt', 'docx'], label_visibility="collapsed")
if uploader is not None:
    if uploader.name.split('.')[-1] == 'docx':
        text = mammoth.convert_to_markdown(uploader).value
    elif uploader.name.split('.')[-1] == 'txt':
        text = uploader.read().decode("utf-8")
test_examples = text
if test_examples:
    st.subheader("上传的中文文章：")
    st.text_area(label='上传的中文文章', value=test_examples, height=300, label_visibility="collapsed")
    inputs = tokenizer(
        test_examples,
        padding="max_length",
        truncation=True,
        max_length=1024,
        return_tensors="pt",
    )
    input_ids = inputs.input_ids.to(model.device)
    attention_mask = inputs.attention_mask.to(model.device)
    # 生成
    outputs = model.generate(input_ids, attention_mask=attention_mask, max_length=128)
    # 将token转换为文字
    output_str = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    output_str = [s.replace(" ", "") for s in output_str]
    print(output_str)
    print("中文摘要生成完毕")
    st.divider()
    processing()
    st.subheader("自动生成的中文摘要：")
    st.text_area(label='自动生成的中文摘要', value=output_str[0], height=200, label_visibility="collapsed")


