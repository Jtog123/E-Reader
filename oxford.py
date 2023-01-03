import requests
import json
import os

app_id = os.environ.get("READER_ID")
app_key = os.environ.get("READER_API_KEY")


language = "en-gb"
word_id = "example"
url = "https://od-api.oxforddictionaries.com:443/api/v2/words/en-gb?q=vigilance&fields=definitions" 
#+ language + "/" + word_id.lower()
#r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
#data = r.json()
#if more than one definition loop through
#print(data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0])


#print("code {}\n".format(r.status_code))
#print("text \n" + r.text)


'''
url  = "https://api.dictionaryapi.dev/api/v2/entries/en/nonpredictave"
r = requests.get(url)
data = r.json()
print("*************")
print(data[0]['meanings'][0]['definitions'][0]['definition'])
print("*************")
'''



