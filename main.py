#import de fast API
from fastapi import FastAPI
# import de BaseModel 
from pydantic import BaseModel


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
class Text(BaseModel):
    resume: str


@app.post("/")
async def resume_email(text : Text) :
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

    return(summary)