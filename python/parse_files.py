# parse_files.py

import pdf_text
import csv
import json

def get_references(filenames):
""" Return a list of references """
    references = []
    
    for f in filenames:
        try:
            text = pdf_text.extract_text("../Papers/" + f)
            references.append(f + " " + ",".join(pdf_text.get_references(text)))
        except:
            references.append(f + " " + "Could not get references")
            
    return references


def get_filenames():
""" Turn list of authors and years into list of filenames """
    f = open('../data/paper_list.tsv', 'rb')
    f = csv.reader(f, delimiter = '\t')
    
    filenames = []
    
    for row in f:
        if row[0] != "Year":
            author = row[0].split(" ")[0]
            filenames.append(author + row[1] + ".pdf")
            
    return filenames


def get_citations():
""" Turn list of authors and years into brief citations of the form Author1 & Author2 Year"""
    f = open('../data/paper_list.tsv', 'rb')
    f = csv.reader(f, delimiter = '\t')
    
    citations = []
    
    for row in f:
        if row[0] != "Year":
            citations.append(row[0] + " " + row[1][:4])
            
    return citations


def get_fulltext_json(f, c, p):
""" Extract the full text of papers from files and save as json
    f = list of filenames, c = list of citations, p = path to papers
 """
 
    fulltext = []
    
    for i in range(len(filenames)):
        txt = pdf_text.extract_text(p + filenames[i])
        fulltext.append({"paper": citations[i], "text": txt})
    
    with open('../data/fulltext.json', 'w') as outfile:
        json.dump(fulltext, outfile)
        

if __name__ == "__main__":
    
    filenames = get_filenames()
    citations = get_citations()
    get_fulltext_json(filenames, citations, "../Papers/")
    
    
        
    
 
