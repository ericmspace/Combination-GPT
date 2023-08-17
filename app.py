#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, render_template, request, redirect, url_for
import openai
import replicate, os, json, time, requests


# In[2]:


# Configurations
# 读取环境变量
openai_api_key = os.environ.get("OPENAI_API_KEY")
replicate_token = os.environ.get("REPLICATE_TOKEN")

# 设置header
REPLICATE_HEADER = {
    "Authorization": f"Token {replicate_token}",
    "Content-Type": "application/json"
}

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        choice = request.form.get("choice")  # A new input to decide between openai or duplicate
        q = request.form.get("question")
        
        if choice == "openai":
            res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": q}]
            )
            return render_template("index.html", result=res["choices"][0]["message"]["content"])

        elif choice == "duplicate":
            body = json.dumps(
                {
                    "version": "db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
                    "input": {"prompt": q}
                }
            )
            output = requests.post('https://api.replicate.com/v1/predictions', data=body, headers=REPLICATE_HEADER)
            time.sleep(10)
            get_url = output.json()['urls']['get']
            get_result = requests.post(get_url, headers=REPLICATE_HEADER).json()['output']

            return render_template("index.html", result=get_result[0])

    else:
        return render_template("index.html", result="waiting")


# In[ ]:


if __name__ == "__main__":
    app.run()

