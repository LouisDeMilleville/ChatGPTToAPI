HOW TO IMPORT YOUR CHATGPT ACCOUNT
==================================
First, install chromium on your device
sudo apt-get install chromium

Then, install this extension to be able to export cookies easily in json
https://chromewebstore.google.com/detail/export-cookie-json-file-f/nmckokihipjgplolmcmjakknndddifde


Now, for the ChatGPT account you want to use for the server, do this(I highly recommand to create another account, since using you main account will break the cookies if you use it on another device after that and you will have to regenerate the cookies to use your personal API again):
/!\ Disconnect from ALL the other browsers where this account is connected /!\
- Log into the account on chromium
- Go on the main page of ChatGPT (A new conversation)
- Click on the extension and export the cookies
- Copy the generated json file in this folder (account)
- Now on chromium, right click + inspect element
- Click on the arrow on the side panel > application, then delete all the entries linked to ChatGPT in the categories local_storage, session_storage and cookies
- Now refresh the page. You should be disconnected from your account. If it's still connected, make sure that you have deleted all the required entries in the storage

/!\ Reminder : Do not use this account on another browser, as it will break the cookies you just generated. Prefer to create an account you will use only for this API /!\
