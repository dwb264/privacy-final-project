# parse_files.py

import pdf_text
import csv

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
            author = row[1].split(" ")[0]
            filenames.append(author + row[0] + ".pdf")
            
    return filenames

def get_citations():
    f = open('paper_list.tsv', 'rb')
    f = csv.reader(f, delimiter = '\t')
    
    filenames = []
    


if __name__ == "__main__":
    
    filenames = get_filenames()
    refs = get_references(filenames)
    for ref in refs: print ref
    
    #filenames = ['Acquisti2006.pdf','Amos2015.pdf','Bilogrevic2016.pdf','Cecere2015.pdf','Cho2010b.pdf','Coventry2014.pdf','Cranor1999.pdf','Dommeyer2003.pdf','Dupree2016.pdf','Dutta2011.pdf','Govani2005.pdf','Graeff2002.pdf','Hazari2013.pdf','Hoofnagle2010.pdf','Hoofnagle2012.pdf','Jiang2013.pdf','Kang2015.pdf','Kar2013.pdf','King2011.pdf','Kisilevich2010.pdf','Knijnenburg2013.pdf','Kobsa2016.pdf','Krasnova2012b.pdf','Leon2015.pdf','Madden2013.pdf','McKnight2010.pdf','Mesch2010.pdf','Morrison2012.pdf','Motiwalla2014.pdf','Pitkanen2012.pdf','Prasad2012.pdf','Schrammel2009.pdf','Sheth2014.pdf','Taddicken2014.pdf','Tow2008.pdf','Turow2003.pdf','Ward2005.pdf','Watson2015.pdf','Williams2015.pdf','Woodruff2014.pdf','Wu2012.pdf','Yang2013.pdf','Yang2012.pdf','Young2009.pdf','Zhao2016.pdf','Ernst2015.pdf','Felt2012.pdf','Fiesler2017.pdf','Fox2018.pdf','Gerlach2014.pdf','Golbeck2016.pdf','Goldfarb2012.pdf','Gomez-Barroso2016.pdf','Henne2013.pdf','Ibrahim2012.pdf','Javed2013.pdf','Malik2016.pdf','Marques2014.pdf','Marreiros2016.pdf','Smith2011.pdf','Spiliotopoulos2013.pdf','Awad2006.pdf','Chen2015.pdf','Christofides2009.pdf','Debatin2009.pdf','Dinev2005.pdf','Dinev2012.pdf','Dinev2009.pdf','Doherty2014.pdf','Dong2015.pdf','Drennan2006.pdf','Hughes-Roberts2013.pdf','Jensen2005.pdf','Joinson2008.pdf','Keith2013.pdf','Krasnova2009c.pdf','Krasnova2009b.pdf','Kulcu2014.pdf','Kwon2015.pdf','Larose2007.pdf','Li2014b.pdf','Li2010.pdf','Lin2012.pdf','Lowry2014.pdf','Lutz2014.pdf','Martin2016.pdf','Marwick2011.pdf','Millham2016.pdf','Milne2009.pdf','Miltgen2015.pdf','Norberg2007.pdf','Nov2009.pdf','Ozdemir2017.pdf','Paine2007.pdf','Posey2010.pdf','Potzch2010.pdf','Priebusch2013.pdf','Reynolds2011.pdf','Salehan2013.pdf','Schwaig2013.pdf','Strater2008.pdf','Teubner2016.pdf','Trepte2014b.pdf','Turow2008.pdf','Tuunainen2009.pdf','Wisniewski2017.pdf','Wu2014.pdf','Xu2008.pdf','Youn2009.pdf','Zafeiropoulou2013.pdf','Zlatolas2015.pdf']
    
