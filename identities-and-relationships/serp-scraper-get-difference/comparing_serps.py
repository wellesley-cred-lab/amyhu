import json
import os
import sys

def findChange(query, d1, d2):
    current_query = query
    contrast = {}
    for d in d1:
        print(d)
        comp = d[0]
        if comp['query'] == current_query:
            contrast[1] = d
    for d in d2:
        comp = d[0]
        if comp['query'] == current_query:
            contrast[2] = d
    return contrast

def findOrganicChange(contrast):
    organicResult = {}
    for comp1 in contrast[1]:
        if comp1['type'] == 'organic':
            title1 = comp1['title']
            position1 = comp1['org-position']
            domain1 = comp1['domain']
            found = False
            for comp2 in contrast[2]:
                if comp2['type'] == 'organic': 
                    title2 = comp2['title']
                    position2 = comp2['org-position']
                    domain2 = comp2['domain']
                    if title1 == title2: ### if the change type is move or unchanged
                        found = True
                        diff = position1-position2
                        d = {'change': diff, 'title': title1} 
                        if diff == 0:
                            d['change_type'] = 'unchanged'
                        else:
                            d['change_type'] = 'move'
                        organicResult[domain1] = d
            if found == False: ## if results disappeared
                organicResult[domain1] = {'title': title1, 'change_type': 'disappear'}

    for comp2 in contrast[2]:
        if comp2['type'] == 'organic': 
            domain2 = comp2['domain']
            title2 = comp2['title']
            position2 = comp2['org-position']
            if domain2 not in organicResult: ### if new results appeared
                organicResult[domain2] = {'title': title2, 'change': position2, 'change_type': 'appear'}

    return organicResult


def findNonorganicChange(contrast):
    nonOrganicresult = {}
    for comp1 in contrast[1]:
        if comp1['type'] != 'organic':
            type1 = comp1['type']  ## type1 is the component type
            found = False
            for comp2 in contrast[2]:
                if comp2['type'] != 'organic': 
                    type2 = comp2['type']
                    if type1 == type2: ### if the change type is move or unchanged
                        found = True
                        nonOrganicresult[type1] = {'change_type': 'unchanged'}
            if found == False: ## if results disappeared
                nonOrganicresult[type1] = {'change_type': 'disappear'}

    for comp2 in contrast[2]:
        if comp2['type'] != 'organic': 
            type2 = comp2['type']
            if type2 not in nonOrganicresult: ### if new results appeared
                nonOrganicresult[type2] = {'change_type': 'appear'}

    return nonOrganicresult

def main(file1path, file2path, query, date1, date2):
    with open(file1path, "r") as infile:
        data1 = json.load(infile)
    with open(file2path, "r") as infile:
        data2 = json.load(infile)
    
    contrast = {1: data1, 2:data2}
    organicResult = findOrganicChange(contrast)
    nonOrganicresult = findNonorganicChange(contrast)
    result = nonOrganicresult
    result['organic'] = organicResult

    with open(f'{query}_changebetween_{date1}_and_{date2}.json', "w") as outfile:
        json.dump(result, outfile)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])