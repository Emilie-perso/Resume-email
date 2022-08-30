import imaplib
import email
from email.header import decode_header
import os
import json 

from classes import Text

def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

def read_mail():
        # connection au compte outlook
    username = ""
    password = ""
    imap_server = "imap-mail.outlook.com"
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
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                print("Subject:", subject)
                print("From:", From)
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
                            print(body)
                        elif "attachment" in content_disposition:
                            # download attachment
                            filename = part.get_filename()
                            if filename:
                                folder_name = clean(subject)
                                if not os.path.isdir(folder_name):
                                    # make a folder for this email (named after the subject)
                                    os.mkdir(folder_name)
                                filepath = os.path.join(folder_name, filename)
                                # download attachment and save it
                                open(filepath, "wb").write(part.get_payload(decode=True))
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        # print only text email parts
                        print(body)

            # if content_type == "text/html":
                    # if it's HTML, create a new HTML file and open it in browser
                    #folder_name = clean(subject)
                # if not os.path.isdir(folder_name):
                        # make a folder for this email (named after the subject)
                    # os.mkdir(folder_name)
                    #filename = "index.html"
                    #filepath = os.path.join(folder_name, filename)
                    # write the file
                    #open(filepath, "w").write(body)
                    # open in the default browser
                    #webbrowser.open(filepath)

                #print("="*100)
            
    # close the connection and logout
    imap.close()
    imap.logout()


    def resume_email(text : Text) :
        # import des librairies  
        import nltk
        from nltk.corpus import stopwords 
        from nltk.tokenize import word_tokenize, sent_tokenize

        #Tokeninzing
        stopWords = set(stopwords.words("french"))
        words = word_tokenize(text.resume)

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

        sentences = sent_tokenize(text.resume)
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