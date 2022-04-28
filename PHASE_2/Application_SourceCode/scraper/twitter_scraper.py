import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools

def scraper_with_location(location):
    df_city = pd.DataFrame(itertools.islice(sntwitter.TwitterSearchScraper(
        '{} near:"{}" within:10km'.format("covid",location)).get_items(), 50))[['url', 'date','user','content', 'likeCount', 'quoteCount', 'retweetCount', 'replyCount']]
    
    print(df_city.to_json(orient='index',indent = 2))


if __name__ == "__main__":
    scraper_with_location("Australia")