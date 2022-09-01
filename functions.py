import imaplib
import email
from email.header import decode_header
import os
import json 
from classes import Text
import re
import config as cfg

def clean_text(text):
    cleaned_text = re.sub(r'http\S+', '', text)
    cleaned_text = cleaned_text.replace('\r','')
    cleaned_text = cleaned_text.replace('\n','')
    cleaned_text = cleaned_text.replace('\u200c','')
    return cleaned_text

def read_mail():
    # connection au compte outlook
    username = cfg.outlook["username"]
    password = cfg.outlook["password"]
    # use your email provider's IMAP server, you can look for your provider's IMAP server on Google
    # or check this page: https://www.systoolsgroup.com/imap/
    # for office 365, it's this:
    imap_server = "outlook.office365.com"
    global mail 
    mail= ""
    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL(imap_server)
    # authenticate
    imap.login(username, password)
    status, messages = imap.select("INBOX")
    # number of top emails to fetch
    N = 3
    # total number of emails
    messages = int(messages[0])
    for i in range(messages, messages-N, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # print text/plain emails and skip attachments
                           # print(body)
                            mail += body
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        # print only text email parts
                       # print(body)
                        mail += body
                print("="*100)
    # close the connection and logout
    imap.close()
    imap.logout()
    cleaned_mail = clean_text(mail)
    return cleaned_mail


def resume_email(text) :
    # import des librairies  
    import nltk
    from nltk.corpus import stopwords 
    from nltk.tokenize import word_tokenize, sent_tokenize

    #Tokeninzing
    stopWords = set(stopwords.words("french"))
    words = word_tokenize(text)

    #frequency table

    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    sentences = sent_tokenize(text)
    sentenceValue = dict()

    for sentence in sentences:
        for word , freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq

    sumValues = 0 
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

    average = int(sumValues / len(sentenceValue))

    summary = ''
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
            summary += " " + sentence
    return summary