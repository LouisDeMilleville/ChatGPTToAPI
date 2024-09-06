# What's ChatGPTToAPI

(French below)

This project allows you to create your own ChatGPT API server which will use your own ChatGPT to ask questions to GPT using the web interface (it won't use tokens, so it's technically free API). It creates a Chromium account using Selenium and log into your ChatGPT account using cookies that you will have to create before using this server. You will then be able to make an api request to your API from other devices, and you will receive an answer from ChatGPT exactly like if you were using the official API, but without the need to buy tokens.

⚠️ This API is NOT designed to handle multiple requests at the same time, and can take more than 10s to get the answer depending on the lenght of the answer. The goal is to provide a way to use GPT on your personnal projects which don't need to send many requests at the same time nor fast answers. If you have an intensive usage of ChatGPT in your projects, you should use the official API ⚠️

# How does it works ?

This server works by creating an instance of Chromium using Selenium, then loads your ChatGPT account using cookies. 

When you ask a question to your server, it will create a new chat on your account, ask your question to ChatGPT then return the answer.

It uses a custom chromedriver because the protections used by OpenAI prevent browsers detected as automated to use ChatGPT. You can run it fully in the background so you won't see the Chromium instance.

# How can i use it ?

⚠️ This bot has been developped and tested on Linux (Ubuntu 22.04 & 24.04). It should work on Windows and other systems since it uses Python and Chromium, but you may have to do some adjustements ⚠️

You will need python and pip first, if it's not already installed.

Then install chromium

> sudo apt-get install chromium

Now clone this repo and move to it's folder, then create a virtual environnement and activate it.

> virtualenv venv
>
> source venv/bin/activate

Now install the requirements inside your virtual environnement

> pip3 install -r requirements.txt

Now you will need to create the cookies to allow the bot to use your ChatGPT account, follow the tutorial in the README file in the account folder.

Once you created the cookies, you're ready to start the server. Run it at least one time with chromium visible to make sure it works on your side

> python3 main.py

To verify the server fully works, you can try to ask a question from the terminal:

> curl -X POST http://YOUR_SERVER_IP:20999/ask -H "Prompt: PUT_YOUR_PROMPT_HERE"

You should see your question being prompted in the Chromium instance, then you should see the answer in the terminal. If it's the case, you can now run it in the background.

# How to run it on the background

Once you verified everything works perfectly, you can run it on the background to avoid rendering chromium and save ressources.

Install xvfb to be able to run a headless chromium without the headless mode (OpenAI can detect that you're using a headless browser and block the follow tries so we use this to avoid being detected).

> sudo apt-get install xvfb

Now you can run it in the background. Just open a terminal and move to the project's folder, then type this.

> source venv/bin/activate && xvfb-run -a -s "-screen 0 1080x720x24" python3 server.py &

You can now close the terminal. The server is now running fully in the background and you should be able to ask questions and get answers from other devices on your network.

