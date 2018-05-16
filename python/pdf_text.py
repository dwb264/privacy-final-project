# -*- coding: utf-8 -*-
# pdf_text.py

import textract
import re
import PyPDF2
from PIL import Image
import string

def extract_text(filename):
    """ Returns the text from a PDF """
    text = textract.process(filename)
    return text


def get_references_section(text):
    """ Returns the section of text after the word "REFERENCES" appears """
    split = re.split("\nR\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s[A-Za-z\s]*\n", text, flags=re.IGNORECASE)
    section = " ".join(split)[(len(split)-1):]
    return section


def get_references(text, ref_type):
    """ Return citations extracted from the text. 
        ref_type can be 'apa', 'ieee', 'ama', or a custom regex.
    """
    
    references = []
    
    year_re = "18[0-9]{2}|19[0-9]{2}|20[0-9]{2}"
    names_apa = "([A-Z][A-Za-z\-']+,\s([A-Z]\.\s?){1,3})"
    names_ieee = "(([A-Z]\.\s?){1,3}[A-Z][A-Za-z\-']+)"
    names_ama = "([A-Z][A-Za-z\-']+\s([A-Z]\-?){1,3})"
    
    if ref_type == "apa":
        name_re = names_apa
    elif ref_type == "ieee":
        name_re = names_ieee
    elif ref_type == "ama":
        name_re = names_ama
    else: # custom regex
        name_re = ref_type

    years = re.findall(year_re, text)
    
    text = re.split(year_re, text)  
    
    for i in range(len(text)-1):
        
        # Extract last names
        names = re.findall(name_re, text[i].decode('utf-8'))   
        if len(names) > 0:
            last_names = []
            for n in names:
                if ref_type == "apa" or ref_type == "ama":
                    name = n[0].split(" ")[0]
                elif ref_type == "ieee":
                    name = n[0].split(" ")
                    name = name[len(name)-1]
                
                name = ''.join(ch for ch in name if ch not in set(string.punctuation))
                last_names.append(name)
            
            # Format citation
            if len(last_names) == 1:
                references.append(last_names[0] + " " + years[i])
            elif len(last_names) == 2:
                references.append(" & ".join(last_names) + " " + years[i])
            elif len(last_names) > 2:
                references.append(last_names[0] + " et al " + years[i])
    
    return references
        

if __name__ == "__main__":
    # Example of extracting references
    txt = extract_text("../Papers/Acquisti2006.pdf")
    r = get_references_section(txt)
    refs = get_references(r, "apa")
    print refs