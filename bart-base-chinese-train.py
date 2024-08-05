import torch
import datasets
import lawrouge
import numpy as np

from typing import List, Dict
from datasets import load_dataset
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence
from transformers import (AutoTokenizer,
                          AutoModelForSeq2SeqLM,
                          DataCollatorForSeq2Seq,
                          Seq2SeqTrainingArguments,
                          Seq2SeqTrainer,
                          BartForConditionalGeneration)


batch_size = 32
epochs = 5
# 最大输入长度
max_input_length = 512
# 最大输出长度
max_target_length = 128
learning_rate = 1e-04
# 读取数据

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
train_dataset, valid_dataset = dataset.train_test_split(test_size=0.1,shuffle=True,seed=42).values()
train_dataset, test_dataset = train_dataset.train_test_split(test_size=0.1, shuffle=True, seed=42).values()
datasets = datasets.DatasetDict({"train":train_dataset,"validation": valid_dataset,"test":test_dataset})
print(datasets["train"][2])
print(datasets["validation"][2])
print(datasets["test"][2])
print("数据转换完毕")
def preprocess_function(examples):
    """
    document作为输入，summary作为标签
    """
    inputs = [doc for doc in examples["document"]]
    model_inputs = tokenizer(inputs, max_length=max_input_length, truncation=True)

    with tokenizer.as_target_tokenizer():
        labels = tokenizer(examples["summary"], max_length=max_target_length, truncation=True)

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_datasets = datasets
tokenized_datasets = tokenized_datasets.map(preprocess_function, batched=True, remove_columns=["document", "summary", "id"])
# print(tokenized_datasets["train"][2].keys())
# print(tokenized_datasets["train"][2])

def collate_fn(features: Dict):
    batch_input_ids = [torch.LongTensor(feature["input_ids"]) for feature in features]
    batch_attention_mask = [torch.LongTensor(feature["attention_mask"]) for feature in features]
    batch_labels = [torch.LongTensor(feature["labels"]) for feature in features]

    # padding
    batch_input_ids = pad_sequence(batch_input_ids, batch_first=True, padding_value=0)
    batch_attention_mask = pad_sequence(batch_attention_mask, batch_first=True, padding_value=0)
    batch_labels = pad_sequence(batch_labels, batch_first=True, padding_value=-100)
    return {
        "input_ids": batch_input_ids,
        "attention_mask": batch_attention_mask,
        "labels": batch_labels
    }

# 构建DataLoader来验证collate_fn
dataloader = DataLoader(tokenized_datasets["test"], shuffle=False, batch_size=4, collate_fn=collate_fn)
batch = next(iter(dataloader))
# print(batch)

print("开始模型训练")

model = AutoModelForSeq2SeqLM.from_pretrained("./huggingface/bart-base-chinese")
# output = model(**batch) # 验证前向传播
# print(output)
print("加载预训练模型")

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    # 将id解码为文字
    decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
    # 替换标签中的-100
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    # 去掉解码后的空格
    decoded_preds = ["".join(pred.replace(" ", "")) for pred in decoded_preds]
    decoded_labels = ["".join(label.replace(" ", "")) for label in decoded_labels]
    # 分词计算rouge
    # decoded_preds = [" ".join(jieba.cut(pred.replace(" ", ""))) for pred in decoded_preds]
    # decoded_labels = [" ".join(jieba.cut(label.replace(" ", ""))) for label in decoded_labels]
    # 计算rouge
    rouge = lawrouge.Rouge()
    result = rouge.get_scores(decoded_preds, decoded_labels,avg=True)
    result = {'rouge-1': result['rouge-1']['f'], 'rouge-2': result['rouge-2']['f'], 'rouge-l': result['rouge-l']['f']}
    result = {key: value * 100 for key, value in result.items()}
    return result

# 设置训练参数
args = Seq2SeqTrainingArguments(
    output_dir="results", # 模型保存路径
    num_train_epochs=epochs,
    do_train=True,
    do_eval=True,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    learning_rate=learning_rate,
    warmup_steps=500,
    weight_decay=0.001,
    predict_with_generate=True,
    logging_dir="logs",
    logging_steps=500,
    eval_strategy="steps",
    save_total_limit=3,
    generation_max_length=128, # 生成的最大长度
    generation_num_beams=1, # beam search
    load_best_model_at_end=True,
    metric_for_best_model="rouge-1"
)
trainer = Seq2SeqTrainer(
    model,
    args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    data_collator=collate_fn,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)
train_result = trainer.train()
# 打印验证集上的结果
print(trainer.evaluate(tokenized_datasets["validation"]))
# 打印测试集上的结果
print(trainer.evaluate(tokenized_datasets["test"]))
# 保存最优模型
trainer.save_model("results/best")

# # 加载训练好的模型
# model = BartForConditionalGeneration.from_pretrained("./huggingface/best")
# # model = model.to("cuda")
# # 从测试集中挑选4个样本
# test_examples = test_dataset["document"][:5]
# print(test_examples)
# inputs = tokenizer(
#         test_examples,
#         padding="max_length",
#         truncation=True,
#         max_length=max_input_length,
#         return_tensors="pt",
#     )
# input_ids = inputs.input_ids.to(model.device)
# attention_mask = inputs.attention_mask.to(model.device)
# # 生成
# outputs = model.generate(input_ids, attention_mask=attention_mask, max_length=128)
# # 将token转换为文字
# output_str = tokenizer.batch_decode(outputs, skip_special_tokens=True)
# output_str = [s.replace(" ","") for s in output_str]
# print(output_str)
