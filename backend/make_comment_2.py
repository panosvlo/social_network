from transformers import GPT2LMHeadModel, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2',
                                        pad_token_id=tokenizer.eos_token_id)

article_text = """
"I will miss absolutely miss this place with a passion," he said, reflecting on an end of an era - not just for the Irish News, but also for the small surrounding area which used to be known as Belfast's Fleet Street.
Throughout much of the 20th century, Northern Ireland's top newspapers were based in Donegall Street or nearby - now, with the Irish News's departure for modern office space on College Street, they have all left. 
"It was a great interaction because the Belfast Telegraph ran from early morning to late at night and all the time during the day and night the reporters and editors were bumping into each other, swapping stories, swapping ideas, and it was non-stop for most of the 24 hours in the day," he said. 
Mary Kelly, a journalist who worked at various outlets, including the BBC and Irish News, added: "The Front Page was the bar across the road and it was handy for all the offices, but it was also handy when you were covering the crown court on the Crumlin Road. 
"We sat down quite recently and there were four or five photographers who'd worked over that period of time and it was only when we got talking to each other we realised what we had been through.
"Most of the times there would be somebody killed overnight and your job the next day was to go an interview the family and ask if there was a photo that could be used in the paper," she explained. 
"""

article_title = "Irish News move marks the end of Belfast's Fleet Street"

text = f"""
A facebook user posted the below article in his feed.
Title: {article_title} The text: {article_text}Another Facebook user commented on the post:
"""

print(text)

tokens = tokenizer.encode(text, truncation=False)
print(len(tokens))
if len(tokens) <= 1024:
    input_ids = tokenizer.encode(text, return_tensors='pt')

    output = model.generate(input_ids,
                            max_length=10000,
                            num_beams=5,
                            no_repeat_ngram_size=2,
                            early_stopping=True)

    print(tokenizer.decode(output[0], skip_special_tokens=True))
else:
    print("Text is too big.")
