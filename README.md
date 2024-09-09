# What's ChatGPTToAPI

(French below)

This project allows you to create your own ChatGPT API server which will use your own ChatGPT to ask questions to GPT using the web interface (it won't use tokens, so it's technically free API). It creates a Chromium instance using Selenium and log into your ChatGPT account using cookies that you will have to create before using this server. You will then be able to make an api request to your API from other devices, and you will receive an answer from ChatGPT exactly like if you were using the official API, but without the need to buy tokens.

⚠️ This API is NOT designed to handle multiple requests at the same time, and can take more than 10s to get the answer depending on the lenght of the answer. The goal is to provide a way to use GPT on your personnal projects which don't need to send many requests at the same time nor fast answers. If you have an intensive usage of ChatGPT in your projects, you should use the official API ⚠️

# How does it works ?

This server works by creating an instance of Chromium using Selenium, then loads your ChatGPT account using cookies. 

When you ask a question to your server, it will create a new chat on your account, ask your question to ChatGPT then return the answer.

It uses a custom chromedriver because the protections used by OpenAI prevent browsers detected as automated to use ChatGPT. You can run it fully in the background so you won't see the Chromium instance.

# Available endpoints
- /ask
  
  Description : Creates a new chat and ask your prompt to ChatGPT
  
  Required : - A POST request which must include a "Prompt" header with the prompt you want to ask as the value of this header
  
  Returns :
  
  Chat id : XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
  
  Answer : {the_answer}

- /reply
- 
  Description : Reply to an existing chat so ChatGPT will take in account your previous prompts to answer your prompt
  
  Required : - A POST request which must include a "Prompt" header with the prompt you want to ask as the value of this header, and a "Chat-id" header with the id of the chat you want to reply on as the value of this header
  
  Returns :
  
  Chat id : XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
  
  Answer : {the_answer}


# How can i use it ?

⚠️ This server has been developped and tested on Linux (Ubuntu 24.04). It should work on Windows and other systems since it uses Python and Chromium, but you may have to do some adjustements ⚠️

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

If you want to verify the replies works too, you can also try to reply from the terminal :

> curl -X POST http://YOUR_SERVER_IP:20999/reply -H "Prompt: PUT_YOUR_PROMPT_HERE" -H "Chat-id: ID_OF_YOUR_CHAT"

# How to run it on the background

Once you verified everything works perfectly, you can run it on the background to avoid rendering chromium and save ressources.

Install xvfb to be able to run a headless chromium without the headless mode (OpenAI can detect that you're using a headless browser and block connections to ChatGPT so we use this to avoid being detected).

> sudo apt-get install xvfb

Now you can run it in the background. Just open a terminal and move to the project's folder, then type this.

> source venv/bin/activate && xvfb-run -a -s "-screen 0 1080x720x24" python3 server.py &

You can now close the terminal. The server is now running fully in the background and you should be able to ask questions and get answers from other devices on your network.

===============================================================================================================================================================================

# Qu'est-ce que ChatGPTToAPI

Ce projet vous permet de créer votre propre serveur API ChatGPT qui utilisera votre propre compte ChatGPT pour poser des questions à GPT en utilisant l'interface web (Cela n'utilisera pas de tokens donc c'est techniquement une API gratuite). Il crée une instance de Chromium via Selenium et se connecte à votre compte ChatGPT en utilisant des cookies que vous lui aurez fourni au préalable. Vous serez ensuite en mesure de faire une requête API vers votre serveur depuis d'autres appareils, et vous reçevrez une réponse de ChatGPT comme si vous utilisiez l'API officielle, mais sans avoir à acheter des tokens.

⚠️ Cette API n'est PAS prévue pour gérer plusieurs questions en simultané, et peut prendre plus de 10s à donner une réponse en fonction de la longueur de la réponse. Le but est de fournir un moyen gratuit d'utiliser GPT dans vos projets personnels qui ne nécessitent ni de poser plusieurs questions en simultané, ni d'avoir des réponses très rapidement. Si vous avez un usage intensif de ChatGPT dans vos projets, vous devriez plutôt utiliser l'API officielle ⚠️

# Comment ça marche ?

Ce serveur fonctionne en créant une instance de Chromium utilisant Selenium, puis se connecte à votre compte ChatGPT en utilisant des cookies. 

Lorsque vous posez une question via votre serveur, cela créera une nouvelle conversation sur votre compte, posera votre question à ChatGPT et renverra la réponse.

Il utilise un chromedriver modifié car les protections utilisées par OpenAI empêchent les navigateurs détectés comme automatisés d'utiliser ChatGPT. Vous pouvez le faire tourner totalement en arrière plan afin de ne plus voir l'instance Chromium.

# Endpoints disponibles
- /ask
  
  Description : Crée une nouvelle conversation et pose votre question à ChatGPT
  
  Requis : - Une requête POST qui doit contenir un header "Prompt" avec comme valeur la question que vous souhaitez poser à ChatGPT
  
  Retourne :
  
  Chat id : XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
  
  Answer : {la_réponse}

- /reply
  
  Description : Répond à une conversation existante afin que ChatGPT prenne en compte vos questions précédentes pour répondre à votre question
  
  Requis : - Une requête POST qui doit contenir un header "Prompt" avec comme valeur la question que vous souhaitez poser à ChatGPT, et un header "Chat-id" avec l'id de la conversation à laquelle vous souhaitez répondre comme valeur.
  
  Retourne :
  
  Chat id : XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
  
  Answer : {la_réponse}

# Comment l'utiliser ?

⚠️ Ce serveur a été développé et testé sur Linux (Ubuntu 24.04). Il devrait fonctionner sur Windows et d'autres systèmes puisqu'il utilise Python et Selenium, mais vous pourriez avoir à faire quelques ajustements ⚠️

Vous devrez déjà installer python et pip, si ce n'est pas déjà installé.

Ensuite, installez chromium

> sudo apt-get install chromium

Maintenant clonez ce dépôt et déplacez vous dans son dossier, puis créez un environnement virtuel et activez le.

> virtualenv venv
>
> source venv/bin/activate

Maintenant installez les prérequis dans votre environnement virtuel

> pip3 install -r requirements.txt

Maintenant vous devrez créer les cookies pour permettre à votre serveur d'utiliser votre compte, suivez le tutoriel dans le fichier README du dossier account.

Une fois que vous avez créé les cookies, vous êtes prêt à utiliser le serveur. Lancez le au minimum une fois avec Chromium de visible afin de vérifier qu'il fonctionne correctement

> python3 main.py

Pour vérifier que le serveur fonctionne parfaitement, vous pouvez essayer de lui poser une question via le terminal:

> curl -X POST http://YOUR_SERVER_IP:20999/ask -H "Prompt: METTEZ_VOTRE_QUESTION_ICI"

Vous devriez voir votre question être posée dans l'instance Chromium, Puis vous devriez voir la réponse apparaitre dans le terminal. Si c'est le cas, vous pouvez désormais le lancer en arrière plan.

Si vous voulez vérifier que les réponses à une conversation existante fonctionnent, vous pouvez essayer ceci depuis le terminal :

> curl -X POST http://YOUR_SERVER_IP:20999/reply -H "Prompt: METTEZ_VOTRE_QUESTION_ICI" -H "Chat-id: ID_DE_LA_CONVERSATION_A_LAQUELLE_REPONDRE"

# Comment le lancer en arrière plan ?

Une fois que vous avez vérifié que tout fonctionne parfaitement, vous pouvez le lancer en arrière plan pour éviter d'afficher l'instance Chromium et économiser des ressources.

Installez xvfb pour être en mesure de lancer un chromium headless sans le mode headless (OpenAI peut détecter que vous utilisez un navigateur headless et bloquer vos connexions à ChatGPT, donc on utilise ceci pour éviter d'être détecté).

> sudo apt-get install xvfb

Vous pouvez maintenant le lancer en arrière plan. Ouvrez simplement un terminal et déplacez vous dans le dossier du projet, puis tapez ceci.

> source venv/bin/activate && xvfb-run -a -s "-screen 0 1080x720x24" python3 server.py &

Vous pouvez désormais fermer le terminal. Le serveur fonctionne désormais totalement en arrière-plan, et vous devriez être en mesure de poser des questions et reçevoir des réponses depuis d'autres appareils sur votre réseau.

