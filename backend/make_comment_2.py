from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2',
                                        pad_token_id=tokenizer.eos_token_id)

model.to(device)

article_text = """
Among others paying tribute were Health Secretary Steve Barclay, who tweeted: "Her exemplary reporting throughout the Covid pandemic was a vital public service - helping to keep people safe."
"""

article_title = "ITV News journalist Emily Morgan dies, aged 45"

text = f"""
I read the below article.
Title: {article_title}
The text: {article_text}
My comment on the article is:
"""

tokens = tokenizer.encode(text, truncation=False)
print(len(tokens))
if len(tokens) <= 1024:
    input_ids = tokenizer.encode(text, return_tensors='pt')

    output = model.generate(input_ids.to(device),
                            max_length=10000,
                            num_beams=5,
                            no_repeat_ngram_size=2,
                            early_stopping=True)

    print(tokenizer.decode(output[0], skip_special_tokens=True))
else:
    print("Text is too big.")
