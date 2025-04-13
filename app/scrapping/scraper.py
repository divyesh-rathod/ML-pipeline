import requests
from bs4 import BeautifulSoup
import csv
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.article import Article

def fetch_rss_feed(url):
    """
    Fetches the RSS feed from the given URL and returns a Beautiful Soup object
    using the lxml parser.
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "lxml-xml")
        return soup
    else:
        raise Exception(f"Failed to fetch RSS feed: {response.status_code} for URL: {url}")


def parse_rss_items(soup):
    """
    Extracts the <item> elements from the RSS feed and returns a list of dictionaries
    containing key information: title, link, publication date, and description.
    """
    items = soup.find_all("item")
    articles = []
    
    for item in items:
        title = item.find("title").text if item.find("title") else "No Title"
        link = item.find("link").text if item.find("link") else "No Link"
        pub_date = item.find("pubDate").text if item.find("pubDate") else "No Publication Date"
        description = item.find("description").text if item.find("description") else "No Description"
        categories = [cat.text.strip() for cat in item.find_all("category")]
        
        articles.append({
            "title": title,
            "link": link,
            "pub_date": pub_date,
            "description": description,
            "categories": categories  # Now includes a list of category strings
        })
    
    return articles


def store_articles_in_db(articles):
    db = SessionLocal()
    c=0;
    try:
        # 1) Fetch all existing links from the DB into a set
        existing_links = set(r[0] for r in db.query(Article.link).all())

        for article in articles:
            link = article["link"]
            # 2) Skip if link already seen (in DB or already in this batch)
            if link in existing_links:
                c=c+1
                continue

            # 3) Create & add new Article
            new_article = Article(
                title=article["title"],
                link=link,
                pub_date=article["pub_date"],
                description=article["description"],
                categories=article.get("categories", []),
            )
            db.add(new_article)

            # 4) Add the link to the set so no subsequent item in this batch inserts it
            existing_links.add(link)

        db.commit()
        print("Articles successfully stored in the database. ")
        print(c);

    except Exception as e:
        db.rollback()
        print(f"Error storing articles: {e}")
    finally:
        db.close()


def write_articles_to_csv(articles, csv_filename="all_articles.csv"):
    """
    Writes the list of article dictionaries to a CSV file.
    """
    fieldnames = ["title", "link", "pub_date", "description","categories"]
    
    # Open the CSV file for writing using newline='' to prevent extra blank lines.
    with open(csv_filename, mode="w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # Write the header row
        
        for article in articles:
            writer.writerow(article)
    
    print(f"Data successfully written to {csv_filename}")


def main():
 endPoints = ["international", "football", "politics", "global-development",
             "world/ukraine", "world/asia", "us-news", "australia-news",
             "technology", "business","sport/tennis","sport/formulaone","uk/lifeandstyle","fashion","food","tone/recipes","lifeandstyle/relationships","lifeandstyle/health-and-wellbeing","lifeandstyle/women","lifeandstyle/men","uk/travel","travel/usa","travel/europe","science","books","uk/film","games","music/classical-music-and-opera","sport/cricket","uk/environment","environment/climate-crisis","environment/wildlife","environment/energy","environment/pollution","global-development","tone/obituaries","uk/business","business/economics","business/banking","uk/money","money/savings","money/property","money/work-and-careers","money/debt","business/stock-markets","business/series/project-syndicate-economists","uk/business-to-business","business/retail"]
    


 all_articles = []  # To store articles across all feeds.

 for endpoint in endPoints:
        rss_url = f"https://www.theguardian.com/{endpoint}/rss"
        try:
            soup = fetch_rss_feed(rss_url)
        except Exception as e:
            print(f"Error fetching feed from {rss_url}: {e}")
            continue  # Skip to the next site if there's an error
        
        articles = parse_rss_items(soup)
        all_articles.extend(articles)
    
    
    
#     # Now write all articles into a single CSV file.
#  write_articles_to_csv(all_articles, csv_filename="all_articles.csv")

 store_articles_in_db(all_articles)

if __name__ == "__main__":
    main()
