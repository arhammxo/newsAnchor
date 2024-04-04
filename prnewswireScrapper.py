import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

genai.configure(api_key=GEMINI_API_KEY)

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
]
model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


# Main Webpage Url to get specific articles
url = 'https://www.prnewswire.com/news-releases/english-releases/'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# List to store links
links = []


# Finding and storing the links in the list
for news_item in soup.find_all('a', class_='newsreleaseconsolidatelink display-outline w-100'):
    links.append(news_item['href'])

u = 'https://www.prnewswire.com'

count = 1
newsDict = {}

for link in links:
    if count <= 5:
            # Generating the web-accessable link 
            al = str(u+link) 

            # Initializing the scrapper
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            res = requests.get(al, headers=headers)
            doc = BeautifulSoup(res.content, 'html.parser')
            
            # Extracting the Headline
            head = doc.find('h1')
            head = head.text

            # Extracting Content of the article
            content = doc.find('div', class_='col-lg-10 col-lg-offset-1')
            content = content.text
            content = content.strip()

            # print("\n Headline: "+head+"\n Content: "+content+"\n")

            # Confiuring the prompt to get the desired format as result of the content. 
            prompt_parts = [
                   f"As an anchor for a news channel, present the news in about a minute long summary with the headline {head} and its content as {content}. Make sure to use only the neccessary details as a professional news anchor would do but also be as elaborative as possible. Word it as if you are speaking the result as an actual anchor and add some humanness to the result as well. \n",]
            pr = model.generate_content(prompt_parts)
            # print(response.text)
            # response = model.generate_content(prompt_parts)
            promtRes = pr.text 

            # Appending the news to the dictionary as a storage
            newsDict.update({head : promtRes}) 
            print("\n PROMPT RES OF "+str(count)+" : \n")
            print(promtRes)

            count = count + 1