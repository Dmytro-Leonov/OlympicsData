from bs4 import BeautifulSoup as bs
import requests
import json

BASE_URL = "https://en.wikipedia.org"


def get_wiki_page(page=""):
    # return soup object on a given wikipedia page
    return bs(requests.get(f"{BASE_URL}{page}").content, features="html.parser")


def get_every_olympiad(soup: bs):
    # return links to all olympiads
    return [a['href'] for a in soup.find(class_="infobox-full-data").find_all('a', href=True)]


def scrape_every_olympiad(all_olympiads: list, file_name: str, skip_last=1):
    all_olympiads_info = []
    # loop through every olympiad link besides the last ones (they are broken)
    for olympiad_href in all_olympiads[:len(all_olympiads) - skip_last]:
        olympiad = get_wiki_page(page=olympiad_href)
        # remove 'sup' tags
        for sup in olympiad.find_all("sup"):
            sup.decompose()
        # get year and kind
        title = olympiad.find(id="firstHeading").get_text().split(" ")
        print(title)  # to see progress
        year = int(title[0])
        kind = title[1]
        olympiad_info = {"Year": year, "Kind": kind, }
        # get all tr tags from infobox
        info_box = olympiad.find(class_="infobox").findAll('tr')
        # for every tr with info get header and info
        for field in info_box[1:len(info_box) - 1]:
            olympiad_info[field.find("th").get_text()] = field.find("td").get_text()
        # append to dictionary using year as a key
        all_olympiads_info.append(olympiad_info)
        # write to json file
    with open(file_name, 'w') as f:
        json.dump(all_olympiads_info, f, indent=4)


def main():
    # Scrape Summer Olympics
    soup = get_wiki_page(page="/wiki/Summer_Olympic_Games")
    all_olympiads = get_every_olympiad(soup)
    scrape_every_olympiad(all_olympiads, "summer_olympics_data.json")
    print("Scraped Summer Olympics")

    # Scrape Winter Olympics
    soup = get_wiki_page(page="/wiki/Winter_Olympic_Games")
    all_olympiads = get_every_olympiad(soup)
    scrape_every_olympiad(all_olympiads, "winter_olympics_data.json")
    print("Scraped Winter Olympics")

    # Scrape Summer Paralympics
    soup = get_wiki_page(page="/wiki/Summer_Paralympic_Games")
    all_olympiads = get_every_olympiad(soup)
    scrape_every_olympiad(all_olympiads, "summer_paralympics_data.json")
    print("Scraped Summer Paralympics")

    # Scrape Winter Paralympics
    soup = get_wiki_page(page="/wiki/Winter_Paralympic_Games")
    all_olympiads = get_every_olympiad(soup)
    scrape_every_olympiad(all_olympiads, "winter_paralympics_data.json", skip_last=2)
    print("Scraped Winter Paralympics")


if __name__ == "__main__":
    main()
