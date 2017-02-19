#!/usr/bin/python

"""

This is the script that, for each Wikipedia URL in input file,
extracts company website URL from appropriate Wikipedia page
and exports results to wikipedia_answers.csv.

"""

import sys
import csv
import re
import requests
from bs4 import BeautifulSoup


def read_csv_file(file):
    """Reading an input csv file.

    The file must be in the same directory as the script.py

    :param file: An input file name
    :return: A list of wikipedia URLs

    """
    try:
        with open(file, 'r') as file:
            wiki_links = []
            for line in csv.reader(file):
                wiki_links.append(line[0])
            print("\tThe input file has been successfully read.")
            return wiki_links

    except FileNotFoundError:
        print("File '{}' not found!".format(file))
        return None


def extract_websites(wiki_urls):
    """Extracting urls of companies.

    For each input Wikipedia URL,
    it extracts company website URL from Wikipedia page.

    :param wiki_urls: List of Wikipedia URLs
    :return: List of company website URLs

    """
    companies_websites = []
    company_num = 1
    for wiki_url in wiki_urls:
        company_title = re.findall(r'[^/]+$', wiki_url)
        try:
            r = requests.get(wiki_url)
            soup = BeautifulSoup(r.text, "html.parser")
            # Finding a company’s url in HTML code.
            website = soup.find('th', string="Website").findNext('td').a['href']
        except:
            print("\tCompany {0} - {1}: ERROR".format(company_num, company_title[0]))
            companies_websites.append('')
            company_num += 1
            continue

        companies_websites.append(website)
        print("\tCompany {0} - {1}: OK".format(company_num, company_title[0]))
        company_num += 1
    return companies_websites


def create_output_csv(wiki_pages, websites):
    """Creating an output .csv file.

    Creating a .csv file from two lists:
    wiki_pages and websites.
    Format of the file is following: "wikipedia_page","website"

    :param wiki_pages: List of wikipedia pages
    :param websites: List of websites
    :return: nothing

    """
    try:
        with open('wikipedia_answers.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_ALL)
            writer.writerow(["wikipedia_page", "website"])
            writer.writerows(zip(wiki_pages, websites))
        print("\tThe output file has been successfully created.")
    except PermissionError:
        print("Permission error to file!")


def main():
    """Main entry point for the script."""
    try:
        input_file = sys.argv[1]
    except IndexError:
        print("Please, specify an input file!")
        sys.exit()

    # Creating a list of companies Wikipedia pages URLs.
    wiki_urls = read_csv_file(input_file)

    if wiki_urls is not None:
        # Creating a list of companies websites URLs.
        companies_websites = extract_websites(wiki_urls)
        # Creating an output .csv file from the lists above.
        create_output_csv(wiki_urls, companies_websites)


if __name__ == '__main__':
    sys.exit(main())
