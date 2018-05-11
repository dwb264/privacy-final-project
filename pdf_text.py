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
    references = get_references_section(text)
    references = """ Amirkhan, James H. 1990. A Factor Analytically Derived Measure of Coping: The Coping Strategy
Indicator. Journal of Personality and Social Psychology, 59 (5): 1066–1074.
Ashworth, Laurence and Clinton Free. 2006. Marketing Dataveillance and Digital Privacy: Using
Theories of Justice to Understand Consumers’ Online Privacy Concerns. Journal of Business
Ethics, 67 (2): 107–123.
Bagnaschi, Kelly and John Geraci. 2003. Kids and Online Privacy. Trends & Tudes, 2 (4): 1–4.
www.harrisinteractive.com/news/newsletters/k12news/HI_Trends&TudesNews2003_V2_iss4.pdf
(Accessed June 1, 2007).
Baron, Reuben M. and David A. Kenny. 1986. The Moderator-Mediator Variable Distinction in
Social Psychological Research: Conceptual, Strategic, and Statistical Considerations. Journal of
Personality and Social Psychology, 51 (6): 1173–1182.
Bart, Yakov, Venkatesh Shankar, Fareena Sultan, and Glen L. Urban. 2005. Are the Drivers and
Role of Online Trust the Same for All Web Sites and Consumers? A Large-Scale Exploratory
Empirical Study. Journal of Marketing, 69 (October): 133–152.
Bearden, William O., David M. Hardesty, and Randall L. Rose. 2001. Consumer Self-Confidence:
Refinements in Conceptualization and Measurement. Journal of Consumer Research, 28 (June):
121–134.
Brown, Mark and Rose Muchira. 2004. Investigating the Relationship Between Internet Privacy
Concerns and Online Purchase Behavior. Journal of Electronic Commerce Research, 5 (1): 62–
70.
Chester, Jeff and Kathryn Montgomery. 2007. Interactive Food & Beverage Marketing:
Targeting Children and Youth in the Digital Age. Berkeley Media Studies Group.
http://digitalads.org/documents/digiMarketingBrief.pdf (Accessed September 1, 2007).
Dinev, Tamara and Paul Hart. 2004. Internet Privacy Concerns and their Antecedents—Measurement
Validity and a Regression Model. Behavior and Information Technology, 23 (6): 413–423.
———. 2005–2006. Internet Privacy Concerns and Social Awareness as Determinants of Intention
to Transact. International Journal of Electronic Commerce, 10 (2): 7–29.
Dommeyer, Curt J. and Barbara L. Gross. 2003. What Consumers Know and What They Do: An
Investigation of Consumer Knowledge, Awareness, and Use of Privacy Protection Strategies.
Journal of Interactive Marketing, 17 (2): 34–51.
Eastin, Matthew S. and Robert LaRose. 2000. Internet Self-Efficacy and the Psychology of the
Digital Divide. Journal of Computer-Mediated Communication, 6 (1): http://jcmc.indiana.edu/
vol6/issue1/eastin.html (Accessed May 15, 2005).

FALL 2009 VOLUME 43, NUMBER 3 415
eMarketer. 2006. Tweens and Teens Online: From Mario to MySpace, September. http://www.
emarketer.com/Reports/All/Em_tweens_oct06.aspx (Accessed June 10, 2007).
Endler, Norman S. and James D. Parker. 1990. Multidimensional Assessment of Coping: A Critical
Evaluation. Journal of Personality and Social Psychology, 58 (5): 844–854.
Espejo, Eileen and Christina Glaubke. 2005. Interactive Advertising and Children: Issues and
Implications. Children & the Media Policy Belief, Summer 1–8. http://www.childrennow.org/
assets/pdf/issues_media_iadbrief_2005.pdf (Accessed December 15, 2007).
Floyd, Donna L., Steven Prentice-Dunn, and Ronald W. Rogers. 2000. A Meta-Analysis of Research
on Protection Motivation Theory. Journal of Applied Social Psychology, 30 (2): 407–429.
Gervey, Ben and Judy Lin. 2000. Obstacles on the Internet: A New Advertising Age Survey Finds
Privacy and Security Concern Are Blocking the Growth of E-commerce. Advertising Age, 71
(16): 13.
Goodwin, Cathy. 1991. Privacy: Recognition of a Consumer Right. Journal of Public Policy &
Marketing, 10 (Spring): 149–166.
Graeff, Timothy R. and Susan Harmon. 2002. Collecting and Using Personal Data: Consumers’
Awareness and Concerns. Journal of Consumer Marketing, 19 (4): 302–318.
Grant, Ian C. 2005. Young Peoples’ Relationships with Online Marketing Practices: An Intrusion
Too Far? Journal of Marketing Management, 21 (5): 607–623.
———. 2006. Online Privacy—An Issue for Adolescents? Proceedings of the Child and Teen
Consumption 2006. Copenhagen, Denmark. http://www.cbs.dk/content/download/41873/616561/
file/Paper%2046_Ian%20Grant.pdf.
Herman-Stahl, M.A., M. Stemmler, and A.C. Petersen. 1995. Approach and Avoidant Coping:
Implications for Adolescent Mental Health. Journal of Youth and Adolescence, 24 (6): 649–665.
Hui, Kai-Lung, Hock Hai Teo, and Sang-Yong Tom Lee. 2007. The Value of Privacy Assurance:
An Exploratory Field Experiment. MIS Quarterly, 31 (1): 19–33.

Jordan, Mark K. and Donald J. O’Grady. 1982. Children’s Health Beliefs and Concepts: Impli-
cations for Child Health Care. In Child Health Psychology: Concepts and Issues, edited by

Paul Karoly, John J. Steffen, and Donald J. O’Grady, (58–76). New York, NY: Pergamon.
Lanier, Clinton D. and Amit Saini. 2008. Understanding Consumer Privacy: A Review and
Future Directions. Academy of Marketing Science Review, 12 (2): http://www.amsreview.org/
articles/lanier02-2008.pdf (Accessed October 20, 2008).
LaRose, Robert and Nora J. Rifon. 2007. Promoting i-Safety: Effects of Privacy Warnings and
Privacy Seals on Risk Assessment and Online Privacy Behavior. Journal of Consumer Affairs,
41 (Summer): 127–149.
LaRose, Robert, Dana Maestro, and Matthew S. Eastin. 2001. Understanding Internet Usage:
A Social–Cognitive Approach to Uses and Gratifications. Social Science Computer Review,
19 (4): 395–413.
LaRose, Robert, Nora Rifon, Sunny Liu, and Doohwang Lee. 2005. Understanding Online Safety
Behavior: A Multivariate Model. Paper presented to the Communication and Technology
Division at the International Communication Association, New York, NY, May.
Lee, Laurie Thomas. 2000. Privacy, Security, and Intellectual Property. In Understanding the
Web: Social, Political, and Economic Dimensions of the Internet, edited by A.B. Albarran, and
D.H. Goff, (135–164). Ames: Iowa State University Press.
———. 2002. Defining Privacy: Freedom in a Democratic Constitutional State. Journal of
Broadcasting & Electronic Media, 46 (4): 646–650.
Lee, Doohwang and Robert LaRose. 2004. Keeping Our Network Safe: A Model of Online
Safety Behavior. Paper presented to the Association for Education in Journalism and Mass
Communication, Toronto, August.
Lee, Doohwang, Robert LaRose, and Nora Rifon. 2008. Keeping Our Network Safe: A Model of
Online Protection Behavior. Behaviour & Information Technology, 27 (5): 445–454.
Lenhart, Amanda. 2005. Protecting Teens Online. Pew Internet & American Life Project.
http://www.pewinternet.org/PPF/r/152/report_display.asp (Accessed March 1, 2006).

416 THE JOURNAL OF CONSUMER AFFAIRS

Lenhart, Amanda and Mary Madden. 2007. Teens, Privacy & Online Social Networks. Pew Internet
& American Life Project. http://www.pewinternet.org/PPF/r/211/report_display.asp (Accessed
June 13, 2007).
Lenhart, Amanda, Mary Madden, and Paul Hitlin. 2005. Teens and Technology: Youth Are Leading
the Transition to a Fully Wired and Mobile Nation. Pew Internet & American Life Project.
http://www.pewinternet.org/pdfs/PIP_Teens_Tech_July2005web.pdf (Accessed June 11, 2006).
Lenhart, Amanda, Lee Rainie, and Oliver Lewis. 2001. Teenage Life Online: The Rise of the
Instant-Message Generation and the Internet’s Impact on Friendship and Family Relationships.
Pew Internet & American Life Project. http://www.pewinternet.org/pdfs/PIP_Teens_Report.pdf
(Accessed December 20, 2001).
Liau, Albert Kienfie, Angeline Khoo, and Peng Hwa Ang. 2005. Factors Influencing Adolescents
Engagement in Risky Internet Behavior. CyberPsychology & Behavior, 8 (6): 513–520.

Livingstone, Sonia. 2008. Internet Literacy: Young People’s Negotiation of New Online Opportu-
nities. In Digital Youth, Innovation, and the Unexpected, edited by Tara McPherson, (101–122).

Cambridge, MA: MIT.

Lwin, May O. and Jerome D. Williams. 2003. A Model Integrating the Multidimensional Develop-
mental Theory of Privacy and Theory of Planned Behavior to Examine Fabrication of Information

Online. Marketing Letters, 14 (4): 257–272.
Lwin, May O., Andrea J.S. Stanaland, and Anthony D. Miyazaki. 2008. Protecting Children’s
Privacy Online: How Parental Mediation Strategies Affect Website Safeguard Effectiveness.
Journal of Retailing, 84 (2): 205–217.
Lwin, May O., Jochen Wirtz, and Jerome D. Williams. 2007. Consumer Online Privacy Concerns
and Responses: A Power-Responsibility Equilibrium Perspective. Journal of the Academy of
Marketing Science, 35 (4): 572–585.
Maddux, James E. and Ronald W. Rogers. 1983. Protection Motivation and Self-Efficacy: A
Revised Theory of Fear Appeals and Attitude Change. Journal of Experimental Social
Psychology, 19 (September): 469–479.

Maddux, James E., Michael C. Roberts, Elizabeth A. Sledden, and Logan Wright. 1986. Develop-
mental Issues in Child Health Psychology. American Psychologist, 41 (1): 25–34.

Mangleburg, Tamara F. and Terry Bristol. 1998. Socialization and Adolescents’ Skepticism toward
Advertising. Journal of Advertising, 27 (3): 11–21.
Market Wire. 2006. Tweens Flock Online and Spend Big; New eMarketer Report Says 71%

of Pre-teens Will Be Internet Users by 2010, October 4. http://www.marketwire.com/press-
release/Emarketer-693833.html (Accessed June 1, 2007).

Mermelstein, Robin J. and Lee Ann Riesenberg. 1992. Changing Knowledge and Attitudes about
Skin Cancer Risk Factors in Adolescents. Health Psychology, 11 (6): 371–376.
Metzger, Miriam. 2004. Privacy, Trust, and Disclosure: Exploring Barriers to Electronic Commerce.
Journal of Computer-Mediated Communication, 9 (4): http://jcmc.indiana.edu/vol9/issue4/
metzger.html (Accessed March 20, 2005).
Milne, George R. 2003. How Well Do Consumers Protect Themselves from Identity Theft? Journal
of Consumer Affairs, 37 (Winter): 388–402.
Milne, George R. and Maria-Eugenia Boza. 1999. Trust and Concern in Consumers’ Perceptions of
Marketing Information Management Practices. Journal of Interactive Marketing, 13 (1): 5–24.
Milne, George R. and Mary J. Culnan. 2004. Strategies for Reducing Online Privacy Risks: Why
Consumers Read (Or Don’t Read) Online Privacy Notices. Journal of Interactive Marketing, 18
(3): 15–29.
Milne, George R. and Mary Ellen Gordon. 1993. Direct Mail Privacy-Efficiency Trade-Offs Within
an Implied Social Contract Framework. Journal of Public Policy & Marketing, 12 (Fall): 206–
215.
Milne, George R., Andrew J. Rohm, and Shalini Bahl. 2004. Consumers’ Protection of Online
Privacy and Identity. Journal of Consumer Affairs, 38 (Winter): 217–232.
Miyazaki, Anthony D. and Ana Fernandez. 2000. Internet Privacy and Security: An Examination of
Online Retailer Disclosures. Journal of Public Policy & Marketing, 19 (Spring): 54–61.

FALL 2009 VOLUME 43, NUMBER 3 417
———. 2001. Consumer Perceptions of Privacy and Security Risks for Online Shopping. Journal
of Consumer Affairs, 35 (Summer): 27–44.
Moore, Elizabeth S. 2004. Children and the Changing World of Advertising. Journal of Business
Ethics, 52 (2): 161–167.
Moscardelli, Deborah M. and Richard Divine. 2007. Adolescents’ Concern for Privacy When Using
the Internet: An Empirical Analysis of Predictors and Relationships With Privacy-Protecting
Behaviors. Family and Consumer Sciences Research Journal, 35 (3): 232–252.
Norberg, Patricia A., Daniel R. Horne, and David A. Horne. 2007. The Privacy Paradox: Personal
Information Disclosure Intentions versus Behaviors. Journal of Consumer Affairs, 41 (Summer):
100–126.

Nowak, Glen and Joseph Phelps. 1992. Understanding Privacy Concerns: An Assessment of Con-
sumers’ Information-Related Knowledge and Beliefs. Journal of Direct Marketing, 6 (4): 28–39.

———. 1995. Direct Marketing and the Use of Individual-Level Consumer Information: Determin-
ing How and When “Privacy” Matters. Journal of Direct Marketing, 9 (3): 46–60.

Pechmann, Cornelia, Guangzhi Zhao, Marvin E. Goldberg, and Ellen Thomas Reibling. 2003. What
to Convey in Antismoking Advertisements for Adolescents: The Use of Protection Motivation
Theory to Identify Effective Message Themes. Journal of Marketing, 67 (April): 1–18.
Phelps, Joseph, Giles D’Souza, and Glen Nowak. 2001. Antecedents and Consequences of Consumer
Privacy Concerns: An Empirical Investigation. Journal of Interactive Marketing, 15 (4): 2–17.

Phelps, Joseph, Glen Nowak, and Elizabeth Ferrell. 2000. Privacy Concerns and Consumer Willin-
gness to Provide Personal Information. Journal of Public Policy & Marketing, 19 (Spring): 27–41.

Piko, Bettina. 2001. Gender Differences and Similarities in Adolescents’ Ways of Coping. The
Psychological Record, 51 (2): 223–236.
Rainie, Lee. 2006. Life Online: Teens and Technology and the World to Come. Speech to annual
conference of public library association, Boston, MA: The Pew Internet & American Life Project.
March 3. http://www.pewinternet.org/ppt/Teens %20and %20technology.pdf (Accessed July 15,
2007).
Raman, Pushkala and Kartik Pashupati. 2004. Online Privacy: The Impact on Self Perceived
Technological Competence. 2004 American Marketing Association Educators’ Proceedings, 15
(Summer): 5–6.
Rifon, Nora J., Robert LaRose, and Sejung Marina Choi. 2005. Your Privacy Is Sealed: Effects of
Web Privacy Seals on Trust and Personal Disclosures. Journal of Consumer Affairs, 39 (Winter):
339–362.
Rifon, Nora J., Robert LaRose, and Melissa L. Lewis. 2007. Resolving the Privacy Paradox: Toward
a Social-Cognitive Theory of Consumer Privacy Protection. http://www.msu.edu/∼wirthch1/
privacyparadox07.pdf (Accessed October 20, 2008).
Rogers, Ronald W. 1975. A Protection Motivation Theory of Fear Appeals and Attitude Change.
Journal of Psychology, 91 (1): 93–114.
———. 1983. Cognitive and Physiological Processes in Fear Appeals and Attitude Change:
A Revised Theory of Protection Motivation. In Social Psychophysiology, edited by
John T. Cacioppo and Richard Petty, (153–176). New York: Guilford.
Romer, Dan. 2006. Stranger Contact in Adolescent Online Social Networks Common but Likelihood
of Contact Depends on Types of Web Sites; Open Sites, Such as MySpace, More Prone to
Stranger Contact Than Facebook. Philadelphia: The Annenberg Public Policy Center of the
University of Pennsylvania. http://www.annenbergpublicpolicycenter.org/Downloads/Releases/
Release_HC20060920 /Report_HC20060920.pdf (Accessed June 7, 2007).
Sheehan, Kim B. 1999. An Investigation of Gender Differences in Online Privacy Concerns and
Resultant Behaviors. Journal of Interactive Marketing, 13 (4): 24–38.
Sheehan, Kim B. and Mariea G. Hoy. 1999. Flaming, Complaining, Abstaining: How Online Users
Respond to Privacy Concerns. Journal of Advertising, 28 (3): 37–51.
———. 2000. Dimensions of Privacy Concern Among Online Consumers. Journal of Public Policy
& Marketing, 19 (Spring): 62–73.

418 THE JOURNAL OF CONSUMER AFFAIRS

Siponen, Mikko, Seppo Pahnila, and Adam Mahmood. 2007. Employees’ Adherence to Information
Security Policies: An Empirical Study. In New Approaches for Security, Privacy and Trust in
Complex Environments, edited by H. Venter, M. Eloff, L. Labuschagne, J. Eloff, and R. von
Solms, (133–144). Boston, MA: Springer.
Steeves, Valerie. 2006. It’s Not Child’s Play: The Online Invasion of Children’s Privacy. University
of Ottawa Law & Technology Journal, 3 (1): http://ssrn.com/abstract=999687 (Accessed October
20, 2008).

Sturges, James W. and Ronald W. Rogers. 1996. Preventive Health Psychology From a Develop-
mental Perspective: An Extension of Protection Motivation Theory. Health Psychology, 15 (3):

158–166.
Subrahmanyam, Kaveri and Patricia Greenfield. 2008. Online Communication and Adolescent
Relationships. The Future of Children, 18 (1): 119–146.
Tanner, John F., James B. Hunt, and David R. Eppright. 1991. The Protection Motivation Model:
A Normative Model of Fear Appeals. Journal of Marketing, 55 (July): 36–45.
Turow, Joseph. 2001. Privacy Policies on Children’s Websites: Do They Play by the Rules?
Philadelphia, PA: The Annenberg Public Policy Center. http://www.asc.upenn.edu/usr/jturow/
PrivacyReport.pdf.
Turow, Joseph and Lilach Nir. 2000. The Internet and the Family 2000: The View From Parents, the
View From Kids. Philadelphia, PA: The Annenberg Public Policy Center. http://www.appcpenn.
org/Downloads/Information_And_Society/20000516_Internet_and_family/20000516_Internet_
and_family_report.pdf (Accessed April 20, 2002).
Ward, Steven, Kate Bridges, and Bill Chitty. 2005. Do Incentives Matter? An Examination of Online
Privacy Concerns and Willingness to Provide Personal and Financial Information. Journal of
Marketing Communication, 11 (1): 21–40.
Westin, Alan. 1967. Privacy and Freedom. New York: Atheneum.
White, Tiffany Barnett. 2004. Consumer Disclosure and Disclosure Avoidance: A Motivational
Framework. Journal of Consumer Psychology, 14 (1–2): 41–51.

Willard, Nancy. 2006. Youth Risk Online: Foundational Concerns. http://www.education-
world.com/a_tech/columnists/willard/willard002.shtml (Accessed June 7, 2007).

Wirth, Christina B., Nora J. Rifon, Robert J. LaRose, and Melissa L. Lewis. 2007. Promoting
Teenage Online Safety with an i-Safety Intervention Enhancing Self-Efficacy and Protective
Behaviors. https://www.msu.edu/∼wirthch1/childsafety07.pdf (Accessed October 20, 2008).

Wirtz, Jochen, May O. Lwin, and Jerome D. Williams. 2007. Causes and Consequences of Con-
sumer Online Privacy Concern. International Journal of Service Industry Management, 18 (4):

326–348.
Wolburg, Joyce M. 2001. The “Risky Business” of Binge Drinking Among College Students: Using
Risk Models for PSAs and Anti-Drinking Campaigns. Journal of Advertising, 30 (4): 23–39.
Wright, Peter, Marian Friestad, and David M. Boush. 2005. The Development of Marketplace
Persuasion Knowledge in Children, Adolescents, and Young Adults. Journal of Public Policy &
Marketing, 24 (Fall): 222–233.
Xie En, Hock-Hai Teo, and Wen Wan. 2006. Volunteering Personal Information on the Internet:
Effects of Reputation, Privacy Notices, and Rewards on Online Consumer Behavior. Marketing
Letters, 17: 61–74.
Yan, Zheng. 2005. Age Differences in Children’s Understanding of Complexity of the Internet.
Journal of Applied Developmental Psychology, 26 (4): 385–396.
———. 2006. What Influences Children’s and Adolescents’ Understanding of the Complexity of
the Internet? Developmental Psychology, 42 (3): 418–428.

Yao, Mike Z. and Daniel G. Linz. 2008. Predicting Self-Protections of Online Privacy. CyberPsy-
chology & Behavior, 11 (5): 615–617.

Youn, Seounmi. 2005. Teenagers’ Perceptions of Online Privacy and Coping Behaviors: A Risk-
Benefit Appraisal Approach. Journal of Broadcasting & Electronic Media, 49 (1): 86–110.

———. 2008. Parental Influence and Teens’ Attitude Toward Online Privacy Protection. Journal of
Consumer Affairs, 42 (Fall): 362–388. """
    
    years = re.findall("[12][09][0-9]{2}", references)
    #years = [y.replace(")", "").replace("(", "") for y in years]
    
    references = re.split("[12][09][0-9]{2}", references)
    refs = []
    
    print years, references
    for i in range(len(references) -1):
        r = re.findall("([A-Z][A-Za-z\-']+,\s[A-Z][A-Za-z\-']+(\s[A-Z]\.)?((\,\s[A-Z][A-Za-z\-']+\s([A-Z]+\.\s)?[A-Z][A-Za-z\-']+)?\sand\s[A-Z][A-Za-z\-']+\s([A-Z]+\.\s)?[A-Z][A-Za-z\-']+)?)", references[i].decode('utf-8', 'ignore'))
        if len(r) > 0: 
            r = r[0][0].split(",")
            r = [r[0]] + r[1].split("and")
        print r
        if len(r) == 2:
            refs.append(r[0] + " " + years[i])
        elif len(r) == 2:
            refs.append(r[0].split(" ")[0] + " & " + r[1].split(" ")[0] + " " + years[i])
        elif len(r) > 2:
            refs.append(r[0].split(" ")[0] + " et al " + years[i])
            
    for r in refs: print r
    #print get_references(references)
    #print ",".join(get_references(references))
