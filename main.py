import argparse
import json

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"


def get_category_url(category_name):
    """Fetch the URL for a given book category."""
    base_url = f"{BASE_URL}index.html"
    response = requests.get(base_url, timeout=10)
    if response.status_code != 200:
        print("Error accessing the website.")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    category_links = soup.select(".side_categories ul li a")

    for link in category_links:
        if category_name.lower() in link.text.strip().lower():
            return BASE_URL + link["href"]

    print("Category not found.")
    return None


def get_book_details(book_url):
    """Extract book details from its product page."""
    response = requests.get(book_url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    upc = soup.find("th", text="UPC").find_next_sibling("td").text
    title = soup.find("h1").text
    price = soup.find("p", class_="price_color").text
    image_url = soup.find("img")["src"].replace("../..", BASE_URL)

    return {"upc": upc, "title": title, "price": price, "image_url": image_url}


def scrape_books_by_category(category_name: str):
    """Scrape all books from the given category and return as a JSON list."""
    category_url = get_category_url(category_name)
    if not category_url:
        return []

    books = []

    while category_url:
        response = requests.get(category_url, timeout=10)
        if response.status_code != 200:
            print("Error accessing category page.")
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        for book in soup.select("h3 a"):
            book_url = f"{BASE_URL}catalogue" + book["href"].replace(
                "../", "/"
            )
            books.append(get_book_details(book_url))

        next_page = soup.find("li", class_="next")
        if next_page:
            category_url = (
                f"{BASE_URL}catalogue/category/books/"
                + next_page.a["href"]
            )
        else:
            category_url = None

    print(json.dumps(books, indent=4, ensure_ascii=False))
    return books


def main():
    """Scrape Book Website for list of books"""
    parser = argparse.ArgumentParser(
        description="Scrape book details from a given category."
    )
    parser.add_argument(
        "--category",
        help="Enter the category name to scrape books from.",
        default="humor",
    )
    args = parser.parse_args()
    scrape_books_by_category(args.category)


if __name__ == "__main__":
    main()
