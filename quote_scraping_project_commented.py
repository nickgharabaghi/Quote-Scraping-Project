import requests
from bs4 import BeautifulSoup
from random import choice
from time import sleep


def scraping(url):
    """Scrapes the website and returns a list of quotes"""
    all_information = requests.get(
        url)  # Uses the requests module to obtain information from the url
    # Turns the HTML into text that we can work with
    soup = BeautifulSoup(all_information.text, "html.parser")
    page = 1
    all_quotes = []
    # While the next button is on the page (i.e. while you are not on the last
    # page) :
    while soup.find(class_="next"):
        # Makes a request on the current page
        all_information = requests.get(f"{url}/page/{page}")
        soup = BeautifulSoup(all_information.text, "html.parser")
        quotes = soup.find_all(class_="quote")  # Finds all quotes on the page
        for quote in quotes:    # For each quote, appends a dictionary containing the text, author, and href url extension to a list
            all_quotes.append({
                "text": quote.find(class_="text").get_text(),
                "author": quote.find(class_="author").get_text(),
                "href": quote.find("a").attrs["href"]
            })
        page += 1
        sleep(1)    # delays requests to avoid overloading the website's servers
    return all_quotes   # returns the list of all the quotes' text, author, and href extension


def select_quote(list_of_quotes):
    """Selects one quote from the list"""
    selected_quote = choice(list_of_quotes)
    return(selected_quote)


def author_info(base_url, href_tag):
    """Scrapes the author's bio page and returns their date and place of birth"""
    author_bio_page = requests.get(base_url + href_tag)
    soup2 = BeautifulSoup(author_bio_page.text, "html.parser")
    birth_date = soup2.find(class_="author-born-date").get_text()
    birthplace = soup2.find(class_="author-born-location").get_text()
    return birth_date, birthplace


url = "http://quotes.toscrape.com"
all_quotes = scraping(url)

while True:  # While the user wants to continue playing
    selected_quote = select_quote(all_quotes)
    print(selected_quote["text"])   # Prints the selected quote

    successfully_guessed = False
    times_guessed = 0
    # While the user has not successfully guessed the author:
    while successfully_guessed == False:
        print(f"{4-times_guessed} guesses remaining")
        guess = input("Who said that quote? ")
        if guess.upper() == selected_quote["author"].upper():
            print("Congratulations, you guessed correctly!")
            successfully_guessed = True
        else:
            print("Sorry, that wasn't right.")
            times_guessed += 1
            if times_guessed == 1:  # On the first hint, the user is given the author's date and place of birth
                birth_date, birthplace = author_info(
                    url, selected_quote["href"])
                print(f"The person was born on {birth_date} {birthplace}")
            elif times_guessed == 2:    # On the second hint, the user gets the first letter of the author's first name
                print(
                    f"Here's a hint: the first letter of the person's first name is: {selected_quote['author'][0]}")
            elif times_guessed == 3:    # On the third hint, the user gets the firs letter of the author's last name
                last_name = selected_quote["author"].split(" ")[-1]
                print(
                    f"Here's another hint: the first letter of the person's last name is: {last_name[0]}")
            else:
                print(f"The correct answer was {selected_quote['author']}")
                break
    again = input("Do you want to continue playing? ").lower()
    if again in ("no", "n", "nah"):
        break