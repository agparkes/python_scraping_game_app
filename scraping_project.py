# http://quotes.toscrape.com
import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
# from csv import writer

all_quotes   = []
base_url     = "http://quotes.toscrape.com"
url          = "/page/1"

while url:
    res      = requests.get(f"{base_url}{url}")
    print(f"Now Scraping {base_url}{url}...")
    soup     = BeautifulSoup(res.text, "html.parser")
    quotes   = soup.find_all(class_= "quote")

    # with open("blog_data.csv", "w") as csv_file:
    #     csv_writer = writer(csv_file)
    #     csv_writer.writerow(["title", "link", "date"])

    for quote in quotes:
        all_quotes.append({
            "text": quote.find(class_   ="text").get_text(),
            "author" : quote.find(class_="author").get_text(),
            "bio-link" : quote.find("a")["href"]
        })
    next_btn  = soup.find(class_="next")
    url       = next_btn.find("a")["href"] if next_btn else None
    sleep(3)

quote = choice(all_quotes)
remaining_guesses = 4
print("Here's a quote: ")
print(quote["text"])
print(quote["author"])
guess = ""
while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
    guess = input(f"Who is the author of this quote? You have {remaining_guesses} guesses remaining: ")
    if guess.lower() == quote["author"].lower():
        print("YEAH, YOU GOT IS RIGHT!!!") 
        break
    remaining_guesses -= 1
    if remaining_guesses == 3:
        res = requests.get(f"{base_url}{quote['bio-link']}")
        soup = BeautifulSoup(res.text, "html.parser")
        birth_date  = soup.find(class_= "author-born-date").get_text()
        birth_location = soup.find(class_= "author-born-location").get_text()
        print(f"Here's a hint: The author was born on {birth_date}, {birth_location}")
    elif remaining_guesses == 2:
        print(f"Here's another hint: The author's first name starts with {quote['author'][0]}: ")
    elif remaining_guesses == 1:
        author_lastname_initial = quote["author"].split(" ")[1][0] 
        print(f"Here's the final hint: The author's last name starts with {author_lastname_initial}: ")
    else:
        print(f"Sorry, you ran out of guesses. The answer is: {quote['author']}") 

print("Thanks for playing!")