from transformers import GPT2LMHeadModel, GPT2Tokenizer
import random

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2',
                                        pad_token_id=tokenizer.eos_token_id)

text = """
Here is an article I read:
Nigeria is often referred to as the "giant of Africa", given its huge population and economic potential, but it has some gigantic problems too - and these will confront Bola Tinubu as he takes over as president on Monday.
The 71-year-old is unlikely to be fazed by the challenges. As a two-time governor of Lagos, he revitalised Nigeria's commercial hub - no easy task - and is well aware of the issues.
But Nigerians, even those who did not vote for him, will want to see early results from Mr Tinubu. Here are some of the major hurdles he faces and how he may tackle them. 
Despite its oil riches, Nigeria is unable to refine enough crude to meet local demands so it imports petroleum products, which are then sold at a government-set price. As this is usually lower than the import price, the government pays the difference.
But this subsidy is taking a huge toll on dwindling public finances. Last year it guzzled 4.3trn naira ($9.3bn; Â£7.5bn) and for the first half of this year, 3.36trn naira was budgeted. 
These payments come at the expense of development goals such as building schools or hospitals, but removing the subsidy will not be easy as it will lead to an increase in prices.
Many struggling Nigerians, used to seeing politicians mismanaging the country's oil wealth, believe cheap petrol is their share of what has been described as the "national cake".
"He has a capacity to listen and to consult widely before making tough decisions," Housing Minister Babatunde Fashola, a close colleague who succeeded Mr Tinubu as Lagos governor in 2007, told the BBC.
One area he may explore to lessen the impact is to subsidise and improve public transport - something he has experience in after implementing a massive public transport scheme in Lagos that put in place fast bus links.
The outgoing government has also managed to secure an $800m World Bank loan, intended to beef up its welfare scheme for vulnerable Nigerians who will be most affected by the loss of the subsidy. However, lawmakers still have to approve the package - so it is not a done deal.
He won a tightly contested election that was not only rancorous, but exposed ethnic and religious divisions that have lingered even in Nigeria's most cosmopolitan cities.
As governor of Lagos, Mr Tinubu probably had the most ethnically diverse cabinet in Nigeria, appointing non-Lagosians into key positions, which is still a rarity.
But politicians, often with common interests, may be easier to placate than the millions of young Nigerians who did not vote for him - especially those who supported Peter Obi of the Labour Party.
"You will see a government that will embrace new ideas and technology and by extension, you will see a lot of young people around him," Mr Fashola explained.
This may be hyperbole, but Mr Tinubu's use of technology to improve tax collection in Lagos was remarkable, increasing revenue by more than 400% in eight years.
He has spoken several times of his ambition to widen the tax net, but this might be harder to replicate at a national level given high inflation, rising poverty and widespread insecurity that often stops people from working.
Mr Tinubu also favours a more private-sector led approach, in contrast to his predecessor, Muhammadu Buhari, who aimed to bolster national welfare safety nets.
This keeps the naira artificially high - the official exchange rate is 460 naira: $1, available to different categories of people who have to apply and wait till it is available.
Everyone else who wants forex must use the parallel rate - currently 760 naira: $1, meaning there is a widening gap between the official and black market.
The two have a fractious relationship following the central bank's move to redesign the local currency - leading to huge cash shortages - just before the election. This was seen by some as a ploy to scupper the ruling party's chances of winning the vote - allegations Mr Emefiele denies.
Mr Tinubu will want to get a grip on this quickly, given the scale of problem. His administration will be confronting armed criminals on motorcycles in the north-west, countrywide kidnapping and a violent secessionist group in the south-east. Deadly clashes between farmers and herders also continue in the central states.
During the election campaign, Mr Tinubu's deputy, incoming Vice-President Kashim Shettima, said this would be his remit - touting his experience as governor of north-eastern Borno state, home to many Islamist militant groups and the Boko Haram insurgency.
But Nigeria's security challenges have evolved since he left office in 2019 and President Buhari, a former army general, failed dismally to find an answer during his eight years in power - instead insecurity has escalated nationwide.
More importantly, they have proposed freeing police personnel from VIP security and guard duties, which could see more officers on the streets fighting crime.
Since the election, he has travelled abroad twice, raising questions about his health. In 2021 he spent months in London being treated for an undisclosed illness.
He has brushed off the criticism, saying the job does not require the fitness of an Olympic athlete and his associates are quick to remind everyone that US President Joe Biden is older, at 80. 
But Nigerians are weary of seeing presidents spend considerable time in hospitals abroad, leading to government in-fighting for control. This happened under both Mr Buhari and Umaru Yar'Adua, who died in office in 2010.
Since his victory, it has been revealed that he was once issued with a Guinean diplomatic passport - which is not illegal but was not previously disclosed. While a Bloomberg investigation said his son owns an Â£11m mansion in London. Neither Mr Tinubu, his son, nor his allies have commented on the report, and it has not been confirmed that Mr Tinubu was involved in the purchase.
My comment on the article is:
"""
while True:
    sentences = text.split('. ')
    if len(tokenizer.encode(text, truncation=False)) <= 1024:
        break
    else:
        # Delete random sentence
        del sentences[random.randint(0, len(sentences) - 1)]
        text = '. '.join(sentences)

input_ids = tokenizer.encode(text, return_tensors='pt')

output = model.generate(input_ids,
                        max_length=10000,
                        num_beams=5,
                        no_repeat_ngram_size=2,
                        early_stopping=True)

print(tokenizer.decode(output[0], skip_special_tokens=True))
