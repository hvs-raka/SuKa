#from ast import arg

import os
#import subprocess
from dotenv import load_dotenv, dotenv_values
import argparse # help to use the flag in input such ass '--help'
import requests # sends http requests online
from serpapi import GoogleSearch
# from google.colab import userdata # importing keys and secrets consist of APIs ( no need now it's in vscode)

# APIs and other credentials
#API_KEY = userdata.get('customSearchAPI')
#SEARCH_ENGINE_ID = userdata.get('customSearchCX')

load_dotenv()

# Google Search function
def google_dork(query):
    print("[+] Results from Google Search API")
    url = f"https://www.googleapis.com/customsearch/v1" # this url gets hit for api search query
    params = {
        "key": os.getenv("customSearchAPI"),
        "cx": os.getenv("customSearchCX"),
        "q": query
    }

    response = requests.get(url, params=params) # storing results in response using request to ping the url with params

    if response.status_code == 200: # if response comes with result
        result = response.json()
        for index, item in enumerate(result.get("items", []),start=1):
            print(f"\n[{index}] {item['title']}")
            print(f"URL: {item['link']}")
            print(f"Snippet: {item['snippet']}\n")
    else:
        print("Error Fetching search results: ", response.json())


def find_social(username):
    print("\n[+] Searching social media for: ", username)
    social_sites = {
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}",
        "GitHub": f"https://github.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Pinterest": f"https://www.pinterest.com/{username}",
        "YouTube": f"https://www.youtube.com/@{username}",
        "Facebook": f"https://www.facebook.com/{username}",
        "Snapchat": f"https://www.snapchat.com/add/{username}",
        "Medium": f"https://medium.com/@{username}",
        "Dev.to": f"https://dev.to/{username}",
        "About.me": f"https://about.me/{username}",
        "ProductHunt": f"https://www.producthunt.com/@{username}",
        "500px": f"https://500px.com/{username}",
        "SoundCloud": f"https://soundcloud.com/{username}",
        "Vimeo": f"https://vimeo.com/{username}",
        "Twitch": f"https://www.twitch.tv/{username}",
        "Flickr": f"https://www.flickr.com/people/{username}",
        "Replit": f"https://replit.com/@{username}",
        "Kaggle": f"https://www.kaggle.com/{username}",
        "Steam": f"https://steamcommunity.com/id/{username}",
        "GitLab": f"https://gitlab.com/{username}",
        "BuyMeACoffee": f"https://www.buymeacoffee.com/{username}",
        "CodePen": f"https://codepen.io/{username}"
    } # creating dictionary with sites and their links

    for site, url in social_sites.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"[-] Found username on {site}: {url}")
            else:
                print(f"[-] User not found on {site}")
        
        except requests.exceptions.RequestException:
            print(f"[-] Could not check {site}")


# yandex image search 
def yandex_image_search(image_url):
    print("\n[+] Performing Yandex image search..")
    params = {
        "engine" : "yandex_image",
        "url": image_url,
        "api_key": os.getenv("serpAPI")
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()

        if "images_results" in results:
            print("[+] Found Similar Images: \n")
            for i, image in enumerate(results["images_results"],1):
                print(f"{i}. Title: {image.get('title')}")
                print(f"    Image URL: {image.get('original')}")
                print(f"    Source: {image.get('link')}\n")
        else:
            print("[-] No similar image found or something went wrong")

    except Exception as e:
        print(f"[-] Error during image Search: {e}")


# using parse on input
def parse_input(query):
    # spliting query into list of arguments
    args_list = query.split()
    # creating an argument parser object
    parser = argparse.ArgumentParser(description="Process some inputs.")

    # adding arguments
    parser.add_argument("-q", "-query", type=str, dest='query',nargs="+", action = 'append', help="Your Query") # nargs is there to make sure that multile words and multiple querries can come action = append ensures that it calls -q everytime the querry got it
    parser.add_argument("-s", "-site", type=str, dest='site', help="Specific Site", default=None)
    parser.add_argument("-fl", "-file-type", type=str, dest='file_type', help="File Type", default=None)
    parser.add_argument("-iu", "-inurl", type=str, dest='inurl', help="URL part", default=None)
    parser.add_argument("-u", "-username", type=str, dest='username', help="Username", default= None)
    parser.add_argument("-img", "-image", type=str, dest = 'image', help="Public image URL to perform reverse image search via Yandex (SerpAPI)")

    try:
        # parse the argument from the user input
        args = parser.parse_args(args_list)
        return args
    except SystemExit:
        # handle invalid input gracefully
        print("Invalid input. Please try again.")
        return None



# constructing query
def construct_query(args):
    ConQuery = []
    if args is not None:
        if args.query:
            for query_group in args.query:
                ConQuery.append("+" + "+".join(query_group))
        if args.site:
            ConQuery.append(f"site:{args.site}")
        if args.file_type:
            ConQuery.append(f"filetype:{args.file_type}")
        if args.inurl:
            ConQuery.append(f"inurl:{args.inurl}")
        if ConQuery:
            return " ".join(ConQuery)





# main function
def main():
    print("Welcome to SuKa it's the information gathering tool.")
    print("currently works on Google Custom Search API")
    print("--> how to use it")
    print("Here 'argparse' works in the input once code is started not like bash terminal")
    print("-> example query { -q your_query_here -s site_to_search_on.com }")
    print("> '-q' or '-query' = The main query / use multiple times to call must include queries")
    print("> '-s' or '-site' = The site to search in works same as (site: site.com)")
    print("> '-fl' or '-file-type' = This specifies the file type such as pdf")
    print("> '-iu' or '-inurl' = Must contain in url")
    print("> '-all' = this performs all saerch functions")

    while True:
    # getting user input
        OgQuery = input("Enter your Query: ")
        args = parse_input(OgQuery)
        newQuery = construct_query(args)

        if args.username:
            find_social(args.username)
        elif args.image:
            yandex_image_search(args.image)
        
        results = google_dork(newQuery)

        if results:
            print(f"[+] Found {len(results)} results:")
            for i, result in enumerate(results, 1):
                print(f"{i}. Title: {result['title']}")
                print(f"   Link: {result['link']}\n")
        else:
            print("[-] No results found.")



        # for exiting the program
        if OgQuery.lower() in ["exit","quit"]:
            print("Exiting program, Goodbye!")
            break


if __name__ == "__main__":
    main()

