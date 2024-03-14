import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

def scrape_books(page_url, collection):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    books = soup.find_all('article', class_='product_pod')
    for book in books:
        title = book.find('h3').find('a')['title']
        price = book.find('p', class_='price_color').get_text()
        availability = book.find('p', class_='instock availability').get_text().strip()
        rating = get_rating(book)  # Get the rating
        # Insert the scraped data into MongoDB collection
        collection.insert_one({
            "title": title,
            "price": price,
            "availability": availability,
            "rating": rating  # Include the rating in the document
        })


# Function to extract rating from the book element
def get_rating(book):
    rating_tag = book.find('p', class_='star-rating')
    rating_classes = rating_tag.get('class')
    rating = rating_classes[1] if rating_classes else 'No rating'
    return rating