from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2',
                                        pad_token_id=tokenizer.eos_token_id)

model.to(device)

article_text = """
TROTWOOD, Ohio â Four years after the Memorial Day tornadoes swept across the Dayton region, homes have been rebuilt, parks restored and businesses brought back. For most people who lived through the worst of it, it feels like time to move on, but reminders remain all too present.
In Trotwood, one of the hardest hit areas, the city managerâs office said more than 90% of the destroyed and damaged housing has been recovered or removed, yet one of the largest projects, the Woodland Hills apartments, stand as a reminder thereâs still plenty of work left to do.
For Stephanie Kellum, dealing with the loss of housing in Trotwood was one of the top priorities after the 2019 storm. In Trotwood alone, the Miami Valley Regional Planning Commission found several hundred damaged or destroyed units in their assessment. 
âMontgomery County already had a housing deficiency,â Kellum said. âSo to lose housing when you already had a housing deficiency lets you know that people are happy to return home.â
The two biggest blows to the housing stock were the two multi-family complexes hit hard in the storms, accounting for nearly 800 units of housing by themselves. Coming right before the 2020 census, Kellum said this significantly deflated the population numbers reported in Trotwood, affecting the cityâs cut of federal funding and services. 
âOur city manager and our mayor wrote letters to Fannie Mae advocating on behalf of the citizens and the property owner to give the owners the dollars they needed to rebuild here,â she said.
Roughly nine months after the tornado, the complex reopened, allowing families to return and refill its 312 units and now, four years later, Kellum says most of its surrounding neighborhood has rebuilt.
Not all the homes have returned, however. Kellum said a handful in the past year were demolished with help from the Montgomery County Land Bank after negotiating with property owners, insurers and other interested parties. Rather than remediate, some decided not to move back and rebuild.
At the same time, neighbors are growing frustrated that the largest eyesore remains standing. The city of Trotwood filed a lawsuit against the owners of the Woodland Hills apartment complex in 2022, hoping to get the complex demolished or started on a remediation plan.
In the four years since the tornado, itâs been the site of multiple break-ins and fire calls. One neighbor, whose yard borders the property, showed Spectrum News, a hole in her fence that she said squatters used to go through her yard to get into the building. Every time the hole is blocked or repaired, she said a new one forms.
The city has asked the court to declare the complex a public nuisance prompting demolition. Meanwhile, Kellum said sheâs hoping to finally see those 430 units replaced.
In other heavily affected neighborhoods, Trotwood is growing. In the Moses Creek neighborhood, the impact of the tornadoes is barely visible outside of the memorial plaque along the main street. Homes are rebuilt, people are moving in and construction is underway.
Kellum said thatâs what sheâd like to see on every empty lot the tornado left behind. Once all of Trotwoodâs housing is restored, then she said the city can finally move on.
"""

article_title = "Four years after tornadoes, Trotwood rebuild faces obstacles"

text = f"""
I just read the below article.\nTitle of the article: {article_title}\nThe content of the article: {article_text}What I would like to comment on the article is that
"""

print(text)

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
