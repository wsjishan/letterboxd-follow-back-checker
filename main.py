from bs4 import BeautifulSoup
import requests


def fetch_url(session):
    while True:
        user_name = input("Please enter your Letterboxd username: ")
        user_url = f"https://letterboxd.com/{user_name}/"
        response = session.get(user_url)
        if response.status_code == 200:
            return user_url
        else:
            print("Invalid username. Please try again.")


def get_users(session, user_url, relation_type):
    page_number = 1
    users_list = []
    while True:
        response = session.get(f"{user_url}{relation_type}/page/{page_number}")
        soup = BeautifulSoup(response.text, "html.parser")

        elements = soup.find_all("a", class_="name")
        if not elements:
            break

        for element in elements:
            user_link = element.get("href")
            full_user_url = f"https://letterboxd.com{user_link}"
            users_list.append(full_user_url)

        page_number += 1

    return users_list


def main():
    session = requests.Session()
    user_url = fetch_url(session)

    followers_list = get_users(session, user_url, "followers")
    following_list = get_users(session, user_url, "following")

    not_following_back = [user for user in following_list if user not in followers_list]

    with open("not_following_back.txt", "w") as file:
        file.write(f"Users not following back: {len(not_following_back)}\n\n")
        for index, user in enumerate(not_following_back, start=1):
            file.write(f"{index}. {user}\n\n")

    print("Output written to not_following_back.txt")


if __name__ == "__main__":
    main()
