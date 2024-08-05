# facebook/huggingface-large-cnn
# 可以实现英文文章摘要

from transformers import BartTokenizer, BartForConditionalGeneration

model = BartForConditionalGeneration.from_pretrained('./huggingface/bart-base')
tokenizer = BartTokenizer.from_pretrained("./huggingface/bart-base")
text = '''
        Find the spelling mistakes in this text
        I started my schooling as the majority did in my area, at the local primary school. I then went to the local secondary school and received grades in English, Maths, Physics, Biology, Geography, Art, Graphical Communication and Philosophy of Religion. I 'll not bore you with the' A' levels and above.
        Notice the ambiguous English qualification above. It was, in truth, a course dedicated to reading “ Lord of the flies ” and other gems, and a weak attempt at getting us to comprehend them. Luckily my middle-class upbringing gave me a head start as I was already acquainted with that sort of language these books used( and not just the Peter and Jane books) and had read similar books before. I will never be able to put that particular course down as much as I desire to because, for all its faults, it introduced me to Steinbeck, Malkovich and the wonders of Penny, mice and pockets.
        My education never included one iota of grammar. Lynn Truss points out in “ Eats, shoots and leaves ” that many people were excused from the rigors of learning English grammar during their schooling over the last 30 or so years because the majority or decision-makers decided one day that it might hinder imagination and expression( so what, I ask, happened to all those expressive and imaginative people before the ruling?).
'''
inputs = tokenizer([text], max_length=1024, return_tensors='pt')
summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=200, early_stopping=True)
summary = ([tokenizer.decode(i, skip_special_tokens=True, clean_up_tokenization_spaces=False) for i in summary_ids])
print(summary)