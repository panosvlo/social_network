from transformers import GPT2LMHeadModel, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2',
                                        pad_token_id=tokenizer.eos_token_id)

tokenizer.decode(tokenizer.eos_token_id)
text = """
Here is an article I read:
For about 30 years, Steve Richards taught outdoor activities including archery and axe-throwing. But being made redundant and bearing an uncanny resemblance to U2 guitarist The Edge has sent his life in an unexpected direction. 
"I work outside so winter time I've always got a beanie-type hat on," said Mr Richards, explaining how he came to be regularly compared to the lead guitarist of one of the world's most successful rock bands. 
"I was in a bit of a state, thinking 'oh my God what am I going to do now?' So over Christmas I had that kind of panic and worry but at the beginning of January I had a change of mindset.
He said "literally two or three days later" while at home painting a skirting board, he got a call from the agent about some filming with the actual U2. 
"He said 'I've got something you might be interested in - I've just been on the phone to U2's production company and are you free for a week next week?" he recalled. 
Mr Sfera, an experienced musician from California, has his own tribute band and had been a stand-in double for Bono on occasions during a 30-year career. 
Ahead of the show they walked around together and were asked by a busker to sing a song. The Camden New Journal reported crowds believed "U2 had come to Camden Town".
Mr Richards' first performance was in front of a growing entourage "thinking it was the real thing", with guitar chords on a piece of paper in his pocket. They then did some impromptu gigs in cafes and shops. 
His nerves hit again during the sound check in front of a capacity crowd at Dublin Castle, as he prepared to play songs including One and With or Without You. 
"He commands a crowd so well. So I was kind of lucky that way because I just have to sit in the background - like The Edge does - and just play the music," he said. 
The new duo are hoping for more work together, with Mr Sfera putting his friend in touch with tutors who can help him learn more about the electric guitar and The Edge's sound effects. 
My comment on the article is:
"""
input_ids = tokenizer.encode(text, return_tensors='pt')

output = model.generate(input_ids,
                        max_length=10000,
                        num_beams=5,
                        no_repeat_ngram_size=2,
                        early_stopping=True)

print(tokenizer.decode(output[0], skip_special_tokens=True))
