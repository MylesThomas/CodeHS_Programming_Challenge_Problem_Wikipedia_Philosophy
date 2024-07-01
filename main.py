import requests
from bs4 import BeautifulSoup
import sys

BASE_URL = 'https://en.wikipedia.org'
PHILOSOPHY_URL = f'{BASE_URL}/wiki/Philosophy'

def fetch_url(url: str) -> BeautifulSoup:
    """
    Fetches the content of a URL and returns the BeautifulSoup object.

    Args:
        url (str): The URL to fetch.

    Returns:
        BeautifulSoup: Parsed HTML content of the URL.
    """
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def extract_first_link(soup: BeautifulSoup) -> str:
    """
    Extracts and returns the first valid link from the Wikipedia page content.

    Args:
        soup (BeautifulSoup): Parsed HTML content of the Wikipedia page.

    Returns:
        str: The first valid link found, or None if no link is found.
    """
    content = soup.find(id='mw-content-text').find(class_='mw-parser-output')
    for paragraph in content.find_all('p', recursive=False):
        if paragraph.find('a', recursive=False):
            link = paragraph.find('a', recursive=False).get('href')
            if link:
                return f'{BASE_URL}{link}'
    return None

def get_first_link(url: str) -> str:
    """
    Gets the first link from a given Wikipedia page URL.

    Args:
        url (str): The Wikipedia page URL.

    Returns:
        str: The first link found on the page, or None if no link is found.
    """
    soup = fetch_url(url)
    return extract_first_link(soup)

def navigate_to_philosophy(start_url: str, max_hops: int = 100) -> None:
    """
    Navigates through Wikipedia links starting from start_url to the Philosophy page.

    Args:
        start_url (str): The starting Wikipedia page URL.
        max_hops (int): The maximum number of hops_count_int to perform. Defaults to 100.

    Returns:
        None
    """
    visited_set = set()
    hops_count_int = 0

    current_url = start_url
    while current_url != PHILOSOPHY_URL and hops_count_int < max_hops:
        print(current_url)
        if current_url in visited_set:
            print("Loop detected. Exiting.")
            break
        visited_set.add(current_url)
        current_url = get_first_link(current_url)
        if not current_url:
            print("No further links found. Exiting.")
            break
        hops_count_int += 1

    if current_url == PHILOSOPHY_URL:
        print(current_url)
        print(f"Reached Philosophy in {hops_count_int} hops.")
    else:
        print(f"Did not reach Philosophy within {max_hops} hops.")

def main():
    """
    This is the main entry point of the program.
    
    It initializes necessary components and starts the execution.
    """
    if len(sys.argv) != 2:
        print("Usage: python getting_to_philosophy.py STARTING_LINK")
        return

    starting_link = sys.argv[1]
    navigate_to_philosophy(starting_link)

if __name__ == "__main__":
    main()
