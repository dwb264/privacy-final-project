# parse_files.py

import pdf_text
import csv
import json

def get_references(filenames):
    references = []
    
    for f in filenames:
        try:
            text = pdf_text.extract_text("Papers/" + f)
            references.append(f + " " + ",".join(pdf_text.get_references(text)))
        except:
            references.append(f + " " + "Could not get references")
            
    return references
            
            
def get_soc_media(filenames):
    paper_sm = []
    paper_sm_formatted = []
    platforms = []
    
    for f in filenames:
        
        try:
            text = pdf_text.extract_text("Papers/" + f)
            sm = pdf_text.get_sm(text)
            paper_sm.append([f, sm])
            
            for s in sm.keys(): 
                if s not in platforms: platforms.append(s)
            
        except:
            continue
        
    for s in paper_sm:
        file_info = [s[0]]
        sms = s[1]
        for p in platforms:
            try:
                file_info.append(sms[p])
            except:
                file_info.append(0)
        paper_sm_formatted.append(file_info)
    
    return platforms, paper_sm_formatted


def get_filenames():
    f = open('paper_list.tsv', 'rb')
    f = csv.reader(f, delimiter = '\t')
    
    filenames = []
    
    for row in f:
        if row[0] != "Year":
            author = row[0].split(" ")[0]
            filenames.append(author + row[1] + ".pdf")
            
    return filenames


def get_citations():
    f = open('paper_list.tsv', 'rb')
    f = csv.reader(f, delimiter = '\t')
    
    citations = []
    
    for row in f:
        if row[0] != "Year":
            citations.append(row[0] + " " + row[1][:4])
            
    return citations


if __name__ == "__main__":
    
    filenames = get_filenames()
    citations = get_citations()
    
    fulltext = []
    
    for i in range(len(filenames)):
        txt = pdf_text.extract_text("Papers/" + filenames[i])
        fulltext.append({"paper": citations[i], "text": txt})
    
    with open('fulltext.json', 'w') as outfile:
        json.dump(fulltext, outfile)
        
    
 
