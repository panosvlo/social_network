from bs4 import BeautifulSoup
import requests, lxml

headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

html = requests.get('https://news.duckduckgo.com/?q=greece+news&va=f&t=hj&df=w&iar=news&ia=news', headers=headers)
print(html.text)
soup = BeautifulSoup(html.text, 'lxml')

for result in soup.select('.card-with-cluster'):
    # title = result.select_one('.title').text
    # link = result.select_one('.title')['href']
    # snippet = result.select_one('.snippet').text
    # source = result.select_one('.source a').text
    # date_posted = result.select_one('#algocore span+ span').text
    # print(f'{title}\n{link}\n{source}\n{date_posted}\n{snippet}\n')
    print(result)

print(len(soup.select('.card-with-cluster')))
