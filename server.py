import time
import os
import json
from flask import Flask, request, make_response
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)
driver = None

#Function to create a Chromium instance we will use later to send the prompts to ChatGPT
def create_driver():
    #We add some options to reduce the probability of being detected for using Selenium
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = uc.Chrome(options=chrome_options)
    
    # We also execute a few scripts to hide Selenium
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_script('''window.navigator.chrome = {
        runtime: {},
        // etc.
    };''')
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});")
    
    return driver

# Function to load the cookies of our account on the Chromium instance
def loadCookies(driver, path_cookies):
    driver.get('https://chatgpt.com/')
    time.sleep(5)
    with open(path_cookies, 'r', encoding='utf-8') as cookiesfile:
        cookies = json.load(cookiesfile)
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(e)
            print(f"Problem adding this cookie(May not be necessary to be connected to ChatGPT) : {cookie}")
    time.sleep(1)
    driver.get('https://chatgpt.com/')
    print("Cookies loaded")

# Function to get the id of the last chat we used
def get_chat_id(driver):
    try:
        # First, we locate the button to the chat
        chat_element = driver.find_element(By.XPATH, '//a[contains(@class, "flex items-center gap-2 p-2")]')
        # Then we save the content of the href attribute which contains the id of our chat
        href = chat_element.get_attribute('href')
        # Finally, we only keep the id since we don't need a url
        chat_id = href.split('/c/')[1]
        return chat_id
    except Exception as e:
        print(f"An error occurred while getting the chat ID: {e}")
        return None

# Function to detect when the answer is fully generated
def wait_for_assistant_response(driver):
    while True:
        try:
            # The detection works by checking if the send button is there (it's replaced by the stop button while the answer is generated)
            stop_button_present = driver.find_elements(By.XPATH, '//button[@data-testid="stop-button"]')
            send_button_present = driver.find_elements(By.XPATH, '//button[@data-testid="send-button"]')

            if send_button_present:
                # When the answer is completed, we extract it from the page
                elements = driver.find_elements(By.XPATH, '//div[@data-message-author-role="assistant"]')
                
                # We save the chat id so we can use it later
                chat_id = get_chat_id(driver)
                answer_id = len(elements) - 1
                return f"Chat id : {chat_id}\nAnswer : {elements[answer_id].text}"
                #if len(elements) > 0:
                #    if len(elements) == 1:
                #        return f"Chat id : {chat_id}\nAnswer : {elements[0].text}"
                #    elif len(elements) == 2:
                #        return f"Answer 1 : {elements[0].text}\nAnswer 2 : {elements[1].text}"
                break
            else:
                # If there's no send button, it means the answer is still being generated so we wait before checking again
                time.sleep(1)
                
        except Exception as e:
            print(f"An error occured: {e}")
            break

# The endpoint to ask a question from outside our server
@app.route('/ask', methods=['POST'])
def ask():
    global driver
    if not driver:
        return make_response("Driver not initialized", 500)

    # First we get the prompt from the 'Prompt' header
    prompt = request.headers.get('Prompt')
    if not prompt:
        return make_response("Prompt not provided", 400)

    # We make sure the prompt is in utf8
    prompt = prompt.encode('utf-8').decode('utf-8')

    # Then we reload chatGPT to make sure we're on a new chat
    driver.get('https://chatgpt.com/')
    time.sleep(3)
    
    # Then we paste the prompt on the text area and we send it
    #textarea_xpath = "/html/body/div[1]/div[2]/main/div[1]/div[2]/div/div[1]/div/form/div/div[2]/div/div/div[2]/textarea"
    textarea_xpath = "//*[@id=\"prompt-textarea\"]"
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, textarea_xpath))
        ) 
        element.send_keys(prompt)
        element.send_keys(Keys.RETURN)
        time.sleep(5)
        response = wait_for_assistant_response(driver)
        # Again, we make sure the answer sent to the user is also in utf8
        response_utf8 = response.encode('utf-8').decode('utf-8')
        return make_response(response_utf8, 200)
        
    except Exception as e:
        print(e)
        return make_response(str(e), 500)
        
# The endpoint to reply to an existing chat by providing it's id
@app.route('/reply', methods=['POST'])
def reply():
    global driver
    if not driver:
        return make_response("Driver not initialized", 500)

    chat_id = request.headers.get('Chat_id')
    print(f"Chat_id: {chat_id}")
    print(f"Request headers:\n{request.headers}")
    # First we get the prompt from the 'Prompt' header
    prompt = request.headers.get('Prompt')
    if not prompt:
        return make_response("Prompt not provided", 400)
    # Then we save the chat id
    chat_id = request.headers.get('Chat-id')
    if not chat_id:
        return make_response("Chat_id not provided. If it's intentional, you should use the /ask endpoint instead")

    # We make sure the prompt is in utf8
    prompt = prompt.encode('utf-8').decode('utf-8')

    # Then we reload chatGPT to make sure we're on a new chat
    chat_url = 'https://chatgpt.com/c/' + str(chat_id)
    driver.get(chat_url)
    time.sleep(3)
    
    # Then we paste the prompt on the text area and we send it
    #textarea_xpath = "/html/body/div[1]/div[2]/main/div[1]/div[2]/div/div[1]/div/form/div/div[2]/div/div/div[2]/textarea"
    textarea_xpath = "//*[@id=\"prompt-textarea\"]"
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, textarea_xpath))
        ) 
        element.send_keys(prompt)
        element.send_keys(Keys.RETURN)
        time.sleep(5)
        response = wait_for_assistant_response(driver)
        # Again, we make sure the answer sent to the user is also in utf8
        response_utf8 = response.encode('utf-8').decode('utf-8')
        return make_response(response_utf8, 200)
        
    except Exception as e:
        print(e)
        return make_response(str(e), 500)

def main():
    global driver
    accounts = []
    welcome_screen = """
     ██████╗██╗  ██╗ █████╗ ████████╗ ██████╗ ██████╗ ████████╗    ████████╗ ██████╗      █████╗ ██████╗ ██╗
    ██╔════╝██║  ██║██╔══██╗╚══██╔══╝██╔════╝ ██╔══██╗╚══██╔══╝    ╚══██╔══╝██╔═══██╗    ██╔══██╗██╔══██╗██║
    ██║     ███████║███████║   ██║   ██║  ███╗██████╔╝   ██║          ██║   ██║   ██║    ███████║██████╔╝██║
    ██║     ██╔══██║██╔══██║   ██║   ██║   ██║██╔═══╝    ██║          ██║   ██║   ██║    ██╔══██║██╔═══╝ ██║
    ╚██████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║        ██║          ██║   ╚██████╔╝    ██║  ██║██║     ██║
     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝        ╚═╝          ╚═╝    ╚═════╝     ╚═╝  ╚═╝╚═╝     ╚═╝
                                                                                                        
    By https://github.com/LouisDeMilleville \n
    """
    print(welcome_screen)
    print("Starting the bot...")
    # When the server starts, we begin by creating a Chromium instance
    driver = create_driver()
    # Then, we load the cookies of our ChatGPT account and add them to our Chromium instance
    for filename in os.listdir('account'):
        if filename != "README.txt":
            file_path = os.path.join('account', filename)
            accounts.append(file_path)
    loadCookies(driver, accounts[0])
    time.sleep(3)

if __name__ == '__main__':
    main()
    app.run(host='0.0.0.0', port=20999)

