# -*- coding: utf-8 -*-
# pdf_text.py

import textract
import re
import PyPDF2
from PIL import Image


def extract_text(filename):
    """ Returns the text from a PDF """
    text = textract.process(filename)
    return text


def get_section_headers(text):
    """ Returns the numbered section headers from the text """
    reg = '\n(([0-9]+\.)+\s[A-Z]+[A-Za-z\s]*)\n'
    headers = re.findall(reg, text)
    headers = [h[0].split("\n")[0] for h in headers]
    return headers

 
def get_references_section(text):
    """ returns the references section """
    section = " ".join(re.split("\nR\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s[A-Za-z\s]*\n", text, flags=re.IGNORECASE))[1:]
    return section

    
def get_references(text):
    """ Returns the references from the references section """
    
    reg_cite_apa = '((([A-Z][A-Za-z\-\s]+,?\s[A-Z]\.(\s?[A-Z]\.)?)(,\s))*(&|and)?\s?([A-Z][A-Za-z\-\s]+,\s[A-Z]\.(\s?[A-Z]\.)?),?\s\(?[0-9]{4}\)?)'
    #reg_cite_ieee = '((((([A-Z]\.\s?)+)\s[A-Z][A-Za-z\-\s]+,?\s)*((([A-Z]\.\s?)+)\s[A-Z][A-Za-z\-\s]+,?\s)).*[12]{1}[0-9]{3})'
                     
    references = re.findall(reg_cite_apa, text)
    references = [h[0].replace("\n", "") for h in references]
    
    
    formatted_refs = []

    if len(references) > 0:
        # APA format
        reg_names = "[A-Z][A-Za-z\-]+"
        reg_year = "[0-9]{4}"
        
        for r in references:
            names = re.findall(reg_names, r)
            year = re.findall(reg_year, r)
            
            if len(names) == 1:
                formatted_refs.append(names[0] + " " + year[0])
            elif len(names) == 2:
                formatted_refs.append(names[0] + " & " + names[1] + " " + year[0])
            else:
                formatted_refs.append(names[0] + " et al " + year[0])
        
    else:
        # IEEE format
        references = re.split("\[[0-9]+\]\s", text)
                
        if len(references) < 2:
            references = re.split("\n[0-9]{1,3}\.\s", text)
        
        reg_allnames = "^(((([A-Z]\.\s?)+)\s[A-Z][A-Za-z\-\s]+,?\s)*(and\s)?(([A-Z]\.\s?)+)\s[A-Z][A-Za-z\-\s]+.\s)"
        reg_allnames2 = "[A-Z][A-Za-z\-\s]+,\s[A-Z]\."
        
        reg_names = "[A-Z][A-Za-z\-]+"
        reg_year = "[12]{1}[90]{1}[0-9]{2}"
                
        ref_data = []
        
        for r in references:
            if len(r.strip()) > 0:
                ref = {}
                allnames = re.findall(reg_allnames, r)
                if len(allnames) == 0:
                    allnames = re.findall(reg_allnames2, r)
                    names = [re.findall(reg_names, n)[0] for n in allnames]
                    ref["names"] = names
                else:
                    ref["names"] = re.findall(reg_names, allnames[0][0])
                
                if len(allnames) == 0: continue
                
                try:
                    ref["year"] = re.findall(reg_year, r)[0]
                    ref_data.append(ref)
                except:
                    continue
                                
        for r in ref_data:
            if len(r["names"]) == 1:
                formatted_refs.append(r["names"][0] + " " + r["year"])
            elif len(r["names"]) == 2:
                formatted_refs.append(r["names"][0] + " & " + r["names"][1] + " " + r["year"])
            else:
                formatted_refs.append(r["names"][0] + " et al " + r["year"])
    
    return formatted_refs


def get_sm(text):
    """ Get mentions of social media from text """
    sm_list = ['academia.edu', 'about.me', 'advogato', 'anobii', 'asianavenue', 'asmallworld', 'athlinks', 'audimated.com', 'baidu', 'bbm', 'bebo', 'biip.no', 'blackplanet', 'bolt.com', 'busuu', 'buzznet', 'cafemom', 'care2', 'caringbridge', 'classmates.com', 'cloob', 'couchsurfing', 'cozycot', 'crunchyroll', 'cucumbertown', 'cyworld', 'dailybooth', 'dailystrength', 'delicious', 'deviantart', 'diaspora*', 'disaboom', 'dol2day', 'dontstayin', 'draugiem.lv', 'douban', 'doximity', 'dreamwidth', 'dxy.cn', 'elftown', 'ello', 'elixio', 'eons.com', 'etoro', 'facebook', 'fetlife', 'filmaffinity', 'filmow', 'fledgewing', 'flixster', 'flickr', 'focus.com', 'fotki', 'fotolog', 'foursquare', 'friendica', 'friendster', 'fuelmyblog', 'fyuse', 'gab.ai', 'gaia', 'gamerdna', 'gapyear.com', 'gather.com', 'gays.com', 'geni.com', 'gentlemint', 'getglue', 'girlsaskguys', 'gogoyoko', 'goodreads', 'goodwizz', 'google+', 'govloop', 'grindr', 'grono.net', 'habbo', 'hi5', 'hotlist', 'hr.com', 'ibibo', 'identi.ca', 'indaba', 'influenster', 'instagram', 'irc-galleria', 'italki', 'itsmy', 'jaiku', 'jiepang', 'kaixin001', 'kakaotalk', 'kiwibox', 'laibhaari', 'last.fm', 'librarything', 'lifeknot', 'linkedin', 'linkexpats', 'listography', 'livejournal', 'livemocha', 'makeoutclub', 'meetin', 'meetup', 'meettheboss', 'millatfacebook', 'mixi', 'mocospace', 'mog', 'mouthshut.com', 'mubi', 'myheritage', 'myspace', 'nasza-klasa.pl', 'netlog', 'nexopia', 'ning', 'odnoklassniki', 'orkut', 'outeverywhere', 'patientslikeme', 'partyflock', 'pingsta', 'pinterest', 'plaxo', 'playfire', 'playlist.com', 'plurk', 'poolwo', 'quechup', 'quora', 'qq', 'qzone', 'raptr', 'ravelry', 'reddit', 'renren', 'reverbnation.com', 'ryze', 'sciencestage', 'sharethemusic', 'shelfari', 'skoob', 'skyrock', 'skype', 'snapchat', 'socialvibe', 'sonico.com', 'soundcloud', 'spot.im', 'spring.me', 'stage 32', 'stickam', 'streetlife', 'studivz', 'stumbleupon', 'talkbiznow', 'taringa!', 'teachstreet', 'telegram', 'termwiki', 'travbuddy.com', 'travellerspoint', 'tsu', 'tribe.net', 'trombi.com', 'tuenti', 'tumblr', 'twitter', 'tylted', 'untappd', 'uplike', 'vk', 'vampirefreaks.com', 'viadeo', 'viber', 'virb', 'vkontakte', 'vox', 'wattpad', 'wayn', 'weeworld', 'weheartit', 'weibo', 'wellwer', 'wepolls.com', 'wer-kennt-wen', 'weread', 'wechat', 'whatsapp', 'wooxie', 'writeaprisoner.com', 'xanga', 'xing', 'xt3', 'yammer', 'yelp', 'yookos', 'youtube', 'yy', 'zoo.gr']
    text = text.lower().split(" ")
    counts = {}
    for s in sm_list:
        if text.count(s) > 0:
            counts[s] = text.count(s)      
    return counts
    


if __name__ == "__main__":
    text = extract_text("Papers/Millham2016.pdf")