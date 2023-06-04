from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2',
                                        pad_token_id=tokenizer.eos_token_id)

model.to(device)

content = """
What is your opinion on Donald Trump?"""

text = f"""A user in Facebook made the below post.\n{content}\nAnother user commented on that post:"""

print(text)

tokens = tokenizer.encode(text, truncation=False)
print(len(tokens))
if len(tokens) <= 1024:
    input_ids = tokenizer.encode(text, return_tensors='pt')

    output = model.generate(input_ids.to(device),
                            max_length=10000,
                            num_beams=1,
                            no_repeat_ngram_size=2,
                            early_stopping=True,
                            num_return_sequences=1)

    print(tokenizer.decode(output[0], skip_special_tokens=True))
else:
    print("Text is too big.")
