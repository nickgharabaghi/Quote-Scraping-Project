import requests
from bs4 import BeautifulSoup
from random import choice
from time import sleep


def scraping(url):
    all_information = requests.get(url)
    soup = BeautifulSoup(all_information.text, "html.parser")
    page = 1
    all_quotes = []
    while soup.find(class_="next"):
        all_information = requests.get(f"{url}/page/{page}")
        soup = BeautifulSoup(all_information.text, "html.parser")
        quotes = soup.find_all(class_="quote")
        for quote in quotes:
            all_quotes.append({
                "text": quote.find(class_="text").get_text(),
                "author": quote.find(class_="author").get_text(),
                "href": quote.find("a").attrs["href"]
            })
        page += 1
        sleep(1)
    return all_quotes


def select_quote(list_of_quotes):
    selected_quote = choice(list_of_quotes)
    return(selected_quote)


def author_info(base_url, href_tag):
    author_bio_page = requests.get(base_url + href_tag)
    soup2 = BeautifulSoup(author_bio_page.text, "html.parser")
    birth_date = soup2.find(class_="author-born-date").get_text()
    birthplace = soup2.find(class_="author-born-location").get_text()
    return birth_date, birthplace


url = "http://quotes.toscrape.com"
all_quotes = scraping(url)

while True:
    selected_quote = select_quote(all_quotes)
    print(selected_quote["text"])

    successfully_guessed = False
    times_guessed = 0
    while successfully_guessed == False:
        print(f"{4-times_guessed} guesses remaining")
        guess = input("Who said that quote? ")
        if guess.upper() == selected_quote["author"].upper():
            print("Congratulations, you guessed correctly!")
            successfully_guessed = True
        else:
            print("Sorry, that wasn't right.")
            times_guessed += 1
            if times_guessed == 1:
                birth_date, birthplace = author_info(
                    url, selected_quote["href"])
                print(f"The person was born on {birth_date} {birthplace}")
            elif times_guessed == 2:
                print(
                    f"Here's a hint: the first letter of the person's first name is: {selected_quote['author'][0]}")
            elif times_guessed == 3:
                last_name = selected_quote["author"].split(" ")[-1]
                print(
                    f"Here's another hint: the first letter of the person's last name is: {last_name[0]}")
            else:
                print(f"The correct answer was {selected_quote['author']}")
                break
    again = input("Do you want to continue playing? ").lower()
    if again in ("no", "n", "nah"):
        break
