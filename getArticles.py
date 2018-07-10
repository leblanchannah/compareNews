#https://holwech.github.io/blog/Automatic-news-scraper/
#http://newspaper.readthedocs.io/en/latest/
#https://scrapy.org/

import json
import newspaper
from newspaper import news_pool

def saveFile(outFile, content):
    #save articles and info to json files
    with open(outFile, 'w') as fp:
        json.dump(content, fp)

def downloadAndParse(source):
    #return list of article dictionaries
    data = []
    for article in source.articles:
        article.download()
        article.parse()
        temp = {"title":article.title,
                "text":article.text,
                "authors":article.authors,
                "url":article.url
                #"published":article.publish_date
                }
        data.append(temp)
    return data


def main():

    # Build a news souce
    # use memoize_articles flag to turn off article caching 
    fox = newspaper.build("http://www.foxnews.com", memoize_articles=False)
    print(fox.size())
    msnbc= newspaper.build("http://www.msnbc.com", memoize_articles=False)
    print(msnbc.size())
    bbc= newspaper.build("http://www.bbc.com", memoize_articles=False)
    print(bbc.size())

    papers = [fox, msnbc, bbc]


    news_pool.set(papers, threads_per_source=2) #6 total
    news_pool.join()

    # extract and save articles
    saveFile("fox.json", downloadAndParse(fox))
    saveFile("msnbc.json", downloadAndParse(msnbc))
    saveFile("bbc.json", downloadAndParse(bbc))




main()