from transformers import pipeline

# Initialize a text-generation pipeline with GPT-2
generator = pipeline('text-generation', model='gpt2')


def generate_comment(article):
    # Use the first part of the article as a prompt for GPT-2
    prompt = article[:500] + "\nMy comment is:"

    # Generate a text response
    output = generator(prompt, max_length=200, do_sample=True)

    # Extract the generated text and remove the original article text and prompt
    comment = output[0]['generated_text']
    comment = comment.replace(prompt, "").strip()

    # Cut the comment at the last full stop (or any other punctuation you want)
    last_full_stop = comment.rfind(".")
    if last_full_stop != -1:
        comment = comment[:last_full_stop + 1]

    return comment


# Assume we have an article stored in the variable 'article'
article = """
In recent years, artificial intelligence has been a subject of intense media hype. Machine learning, deep learning, 
and AI come up in countless articles, often outside of technology-minded publications. We're promised a future of 
intelligent chatbots, self-driving cars, and virtual assistants—a future sometimes painted in a grim light and other 
times as utopian, where human jobs will become obsolete and AI will take over. As always, the truth is somewhere in the 
middle. AI, machine learning, and deep learning are complex subjects and while they're making headlines, they're still 
misunderstood.
"""

print(generate_comment(article))
