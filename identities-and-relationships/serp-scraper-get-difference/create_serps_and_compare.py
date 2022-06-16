import serp_scraper
import comparing_serps
import os
import sys

def main(date1, date2, filename):
    #date1 = '6-8-22'
    #date2 = '6-9-22'
    #f = 'Ace.html'

    query = filename.split('.')[0]

    os.system(f'python serp_scraper.py {date1} {filename}')
    os.system(f'python serp_scraper.py {date2} {filename}')

    path_to_serps = 'for_comparing_serps'
    f1 = f'{path_to_serps}/{date1}_{filename.split(".")[0]}.json'
    f2 = f'{path_to_serps}/{date2}_{filename.split(".")[0]}.json'

    os.system(f'python comparing_serps.py {f1} {f2} {query} {date1} {date2}')

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
