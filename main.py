import requests
import xmltodict
from bs4 import BeautifulSoup
from fastapi import FastAPI
import uvicorn
# Create 'app' object 
app = FastAPI()


def genIdea(stream):
    url = f"https://www.tradingview.com/feed/?stream={stream}&recent=sort"
    res = requests.get(url)
    xml = res.text
    dct = xmltodict.parse(xml)

    items = dct["rss"]["channel"]["item"]

    ideas = []

    for item in items:
        content = item["content:encoded"]
        soup = BeautifulSoup(content,'lxml')
        author = soup.find('div',class_='chart-author').find('a').text
        img = soup.find_all('img')
        len_img = 1 if len(img) == 2 else 0 
        chart = img[len_img].get('src')
        title = item["title"]
        description = item["description"]
        pubDate = item["pubDate"]
        ideas.append({
            "title":title,
            "description":description,
            "pubDate":pubDate,
            "author":author,
            "chart":chart
        })

    return ideas

@app.get('/{stream}')
def return_idea(stream:str):
    vaild_streams = ['bitcoin', 'commodities', 'crypto', 'currencies', 'indices', 'stocks']
    if stream not in vaild_streams:
        return "unexpected value; permitted: 'bitcoin', 'commodities', 'crypto', 'currencies', 'indices', 'stocks'"
    return genIdea(stream)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)