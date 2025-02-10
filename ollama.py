import requests 
import json 

class Ollama:
  def __init__(self, slug, endpoint="http://localhost:11434/v1/chat/completions", **kwargs):
    self.slug = slug
    self.endpoint = endpoint 
    self.session = requests.Session()
    self.config = {"temperature": 0.7, "n": 1, **kwargs}
    print(f"Intialize Ollama with {self.slug} api endpoint {self.endpoint} config {self.config} ")

  def run(self, question, **kwargs):
    output = ""
    payload = {"model": self.slug, "messages": [{"role": "user", "content": question}], **self.config}
    
    with self.session.post(self.endpoint, json=payload, stream=True) as res:
      if res.status_code == 200:
        data =  res.json()
        return data["choices"][0]["message"]["content"]
      else: 
        print(f"Error : can't post message to ollama {res.status_code}")

    return output.strip()
  

  def __call__(self, question, **kwargs):
    return self.run(question, **kwargs)

