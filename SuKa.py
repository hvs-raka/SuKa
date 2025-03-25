from ast import arg
# from the scratch

import os
from dotenv import load_dotenv, dotenv_values
import argparse # help to use the flag in input such ass '--help'
import requests # sends http requests online
# from google.colab import userdata # importing keys and secrets consist of APIs ( no need now it's in vscode)

# APIs and other credentials
#API_KEY = userdata.get('customSearchAPI')
#SEARCH_ENGINE_ID = userdata.get('customSearchCX')

load_dotenv()

# Google Search function
def google_dork(query):
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


# using parse on input
def parse_input(query):
    # spliting query into list of arguments
    args_list = query.split()
    # creating an argument parser object
    parser = argparse.ArgumentParser(description="Process some inputs.")

    # adding arrguments
    parser.add_argument("-q", "-query", type=str, dest='query',nargs="+", action = 'append', help="Your Query") # nargs is there to make sure that multile words and multiple querries can come action = append ensures that it calls -q everytime the querry got it
    parser.add_argument("-s", "-site", type=str, dest='site', help="Specific Site", default=None)
    parser.add_argument("-fl", "-file-type", type=str, dest='file_type', help="File Type", default=None)
    parser.add_argument("-iu", "-inurl", type=str, dest='inurl', help="URL part", default=None)

    try:
        # parse the arggument from the user input
        args = parser.parse_args(args_list)
        return args
    except SystemExit:
        # handle invalid input gracefully
        print("Invalid input. Please try again.")
        return None



# constructing querry
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

