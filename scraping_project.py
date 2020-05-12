def start_game(quotes):
    quote = choice(quotes)
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
            res = requests.get(f"{BASE_URL}{quote['bio-link']}")
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

    again = ""
    while again.lower() not in ("y", "yes", "yeah", "n", "no", "nop"):
        again = input(f"Would you like to continue playing (y/n)?: ")
    if again.lower() in ("y", "yes", "yeah"):
        return start_game(quotes)
    else:
        print("Thanks for playing!!!")
quotes = scrape_quotes()
start_game(quotes)