This is the script that, for each Wikipedia URL in input file, extracts company website
URL from appropriate Wikipedia page and exports results to wikipedia_answers.csv.

Script input format:
A list of companies Wikipedia pages URLs in wikipedia_links.csv

Script output format:
wikipedia_answers.csv containing list of tuples (columns): wikipedia_page_url, website_url.