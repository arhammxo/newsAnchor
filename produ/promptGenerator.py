import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

genai.configure(api_key="AIzaSyCWna-D27sTjqf3IuIBgd_BD5ZFfvIfQrA")

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

def scrape_bbc_news(url):
    try:
        # Set user-agent header
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        # Make HTTP request
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse HTML
        doc = BeautifulSoup(response.text, 'html.parser')

        # Scrape URLs
        links = doc.find_all('a', {'class': 'gs-c-promo-heading'})
        res=[]
        for link in links:
            res.append(link['href'])
        return res

    except requests.exceptions.RequestException as e:
        print("\033[31mAn error occurred during the scraping process:\033[0m", str(e)) 
        return None


# Scrape BBC News
url = 'http://www.bbc.co.uk/news'
res = scrape_bbc_news(url)

count = 1

for news in res:
    nu = str(news)
    newsDict = {}
    url = 'http://www.bbc.co.uk'+nu
    # print(url)
    if count<=3:
        # Set user-agent header
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        # Make HTTP request
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse HTML
        doc = BeautifulSoup(response.text, 'html.parser')

        #Headlines
        h = doc.find('h1')
        head = h.text
        # print(head)
        tb = []
        for block in doc.find_all('div', {"data-component": "text-block"}):
            tb.append(block.getText())
        
        if len(tb) == 0:
            print("NO NEWS")
        else:
            info = ""
            for t in tb:
                info = "" + str(t)
            # print(info+'\n')
            # prompt_parts = ['f"Pretend you are an anchor for a news channel, act as one for the news headline '{head}' with details as: {info}"',
            prompt_parts = [
                 f"Pretend you are an anchor for a news channel, act as one for the news headline {head} with details as: {info} \n",
                ]
            response = model.generate_content(prompt_parts)
            # print(response.text)
            # response = model.generate_content(prompt_parts)
            promtRes = response.text 
            newsDict.update({head : promtRes})
            # print(response.text)
        count+=1
    for k in newsDict:
        print(f"HEADLINE: {k} \n")
        print(f"PROMPT: {newsDict.get(k)}")

    # except:
    #     print("Error for url:" + news)
    
    # break




