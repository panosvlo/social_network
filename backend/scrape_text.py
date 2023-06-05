from bs4 import BeautifulSoup
import requests
import re


def extract_article(soup):
    text = [p.text for p in soup.find_all('p')]
    return '\n'.join(text)


url = "https://www.tornosnews.gr/en/greek-news/politics/48941-a-total-of-44-parties-submit-applications-for-june-25-elections-in-greece.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

article_text = extract_article(soup)

# Split the text into lines, remove short lines, and then recombine
lines = article_text.split('\n')
filtered_lines = [line for line in lines if len(line) > 150]  # Dont include recommendations, advertisements etc
filtered_text = '\n'.join(filtered_lines)

print(filtered_text)
