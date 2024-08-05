import time
import webbrowser
import mammoth
import streamlit as st
import datasets
from datasets import load_dataset
from transformers import (AutoTokenizer,
                          AutoModelForSeq2SeqLM,
                          DataCollatorForSeq2Seq,
                          Seq2SeqTrainingArguments,
                          Seq2SeqTrainer,
                          BartForConditionalGeneration)


def processing():
    word0 = st.empty()
    bar = st.progress(0)
    for i in range(100):
        word0.subheader('生成并输出中文摘要进行中......: ' + str(i + 1) + '%')
        bar.progress(i + 1)
        time.sleep(0.01)


def output_abstract():
    print("加载训练好的模型")
    model = BartForConditionalGeneration.from_pretrained("./huggingface/best")
    # model = model.to("cuda")
    test_examples = test_dataset["document"][:10]
    # print(test_examples)
    st.subheader("中文摘要测试集：")
    # st.text_area(label='', value=test_examples, height=300)
    st.write(test_examples)
    inputs = tokenizer(
            test_examples,
            padding="max_length",
            truncation=True,
            max_length=512,
            return_tensors="pt",
        )
    input_ids = inputs.input_ids.to(model.device)
    attention_mask = inputs.attention_mask.to(model.device)
    # 生成
    outputs = model.generate(input_ids, attention_mask=attention_mask, max_length=128)
    # 将token转换为文字
    output_str = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    output_str = [s.replace(" ","") for s in output_str]
    # print(output_str)
    st.subheader("生成并输出中文摘要：")
    # st.text_area(label='', value=output_str, height=260)
    st.write(output_str)
    print("中文摘要输出完成...")


def output_abstracts():
    tokenizer = AutoTokenizer.from_pretrained("./huggingface/bart-base-chinese")
    text = []
    st.write("已加载训练好的模型./huggingface/best")
    print("加载完毕训练模型")
    model = BartForConditionalGeneration.from_pretrained("./huggingface/best")
    st.subheader("选择需要中文文本摘要生成的文件上传：")
    uploader = st.file_uploader('', type=['txt', 'docx'])
    if uploader is not None:
        if uploader.name.split('.')[-1] == 'docx':
            text = mammoth.convert_to_markdown(uploader).value
        elif uploader.name.split('.')[-1] == 'txt':
            text = uploader.read().decode("utf-8")
    test_examples = text
    if test_examples:
        st.subheader("上传的中文文章：")
        st.text_area(label='', value=test_examples, height=300)
        inputs = tokenizer(
                test_examples,
                padding="max_length",
                truncation=True,
                max_length=512,
                return_tensors="pt",
            )
        input_ids = inputs.input_ids.to(model.device)
        attention_mask = inputs.attention_mask.to(model.device)
        # 生成
        outputs = model.generate(input_ids, attention_mask=attention_mask, max_length=256)
        # 将token转换为文字
        output_str = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        output_str = [s.replace(" ","") for s in output_str]
        print(output_str)
        print("中文摘要生成完毕")
        processing()
        st.text_area(label='', value=output_str[0], height=200)


def main():
    st.set_page_config(page_title="SummerTask",  page_icon="🦈", layout="wide", initial_sidebar_state="expanded",
                       menu_items={'Get Help': 'https://www.extremelycoolapp.com/help',
                                   'About': "# 暑期任务"})
    st.sidebar.title('暑期任务')
    page = st.sidebar.selectbox("选择一个任务", ["文本中文摘要生成", "中文摘要生成训练查看", "英文文本单词错误校对", "中文人名识别-标注"])

    if page == "文本中文摘要生成":
        st.title("文本中文摘要生成")
        st.write("Tips:  利用Bart预训练模型完成文本文件（docx、txt）一个中文摘要生成的程序")
        output_abstracts()
    elif page == "中文摘要生成训练查看":
        st.title("中文摘要生成训练查看")
        st.write("Tips:  利用Bart预训练模型编写一个中文摘要生成的程序")
        # st.text_area(label='训练集：', value=datasets["train"][2], height=260)
        output_abstract()
    elif page == "英文文本单词错误校对":
        webbrowser.open("http://localhost:8501", new=0)
    elif page == "中文人名识别-标注":
        webbrowser.open("http://localhost:8501", new=0)

if __name__ == "__main__":
    dataset = load_dataset('json', data_files='./huggingface/nlpcc2017_clean.json', field='data')
    # 加载tokenizer,中文bart使用bert的tokenizer
    tokenizer = AutoTokenizer.from_pretrained("./huggingface/bart-base-chinese")
    # 调整数据格式
    def flatten(example):
        return {
            "document": example["content"],
            "summary": example["title"],
            "id": "0"
        }

    # 将原始数据中的content和title转换为document和summary
    dataset = dataset["train"].map(flatten, remove_columns=["title", "content"])
    print(dataset)
    # 划分数据集
    train_dataset, valid_dataset = dataset.train_test_split(test_size=0.1, shuffle=True, seed=42).values()
    train_dataset, test_dataset = train_dataset.train_test_split(test_size=0.1, shuffle=True, seed=42).values()
    datasets = datasets.DatasetDict({"train": train_dataset, "validation": valid_dataset, "test": test_dataset})
    print("数据转换完毕")
    main()