# Intro #

Purpose of this project is to show how to automate communication over WhatsApp messenger.

# Requirements #

* [Python 2.7](https://www.python.org/download/releases/2.7/)
* [Chromium Web Browser](https://download-chromium.appspot.com/)

### Used frameworks ###

* [Selenium with Python](http://selenium-python.readthedocs.io/)

### How do I get set up? ###

#### Python ####

* Install Python (find python installation instructions on the internet)

#### Python libs ####

* [Install Python pip tool for installing Python packages](https://pip.pypa.io/en/stable/installing/)

* Install all required packages for the bot to be run:
~~~
pip install -r whatsapp-pybot/requirements.txt
~~~

#### How do I launch the bot? ####

* Launch the bot using next command:
~~~
python ./pybot/whatsapp/Bot.py -u ./resources/users_sample.txt -m ./resources/message_sample.txt

, where:
-u <FILE_WITH_USERS> - file with users it is going to talk to
-m <FILE_WITH_MESSAGE> - message it is going to send to the users
~~~


* Open WhatsApp on your mobile phone and select Whatsapp Web menu option from the top bar in WhatsApp app

![Phone Setup](/docs/phone.png)

* Scan the QR code that appears on the Chrome browser screen with your WhatsApp app on the phone

![Desktop Setup](/docs/desktop.png)

* Enjoy!

![Chat Window](/docs/chat_window.png)

### Contributors ###

Developer: [Iryna Volkodav](mailto:for.iren86@gmail.com)

Screenshots source: [QRCODE.es](https://www.qrcode.es/en/whatsapp-in-your-pc-screen-scanning-a-qr-code/)

### License ###
MIT
