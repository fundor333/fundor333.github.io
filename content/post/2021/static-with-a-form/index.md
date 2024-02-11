---
title: "Static With a Form in Python"
date: 2021-07-19T14:00:54+02:00
feature_link: "https://unsplash.com/photos/3hs4xso-4KM"
feature_text: "Photo by Zoe on Unsplash"
tags:
- hugo
- microservice
- flask 
slug: "Static-with-a-Form"
categories: 
- dev
- fingerfood
description: "If you have a static site you can also have forms"
type: "post"
---

Sometime you need to make a contact form or something similar but you have a static site. So what do you do?
If you have a static site you don't have a way to save data or send email with the data how do you save/elaborate the form? You need an other software.

# Make a backend for your static site

You have a lot of way to have a backend. Some more simple and cost effective solution for "free plan" site (like a Github Pages) and some more advance solution for more advance system with a static site.

My personal solution for this problem is a *Microservice[^1]* *Rest Api[^2]* with *Captcha[^3]* support. With this system I don't have something to maintain. Also this is a very easy and clean piece of code and if make in the right way you will not edit it ever again.

[^1]: [Wikipedia definition of *Microservice*](https://en.wikipedia.org/wiki/Microservices)
[^2]: [Wikipedia definition of *Rest Api*](https://en.wikipedia.org/wiki/Representational_state_transfer)
[^3]: [Wikipedia definition of *Captcha*](https://en.wikipedia.org/wiki/CAPTCHA)

You can also implement this code in a larger system but I make this code for a *Microservice*. 
Also this is my *Python* implementation because *I use Python* but you can make this solution with your favorite language[^4].

[^4]: If your favorite language is *Cobol* or *Pascal* I suggest my code for your mental stability

## The implementation

For this you need two part. One is the frontend and one is the backend.

### Frontend Html and JS

``` html
<script src="https://www.google.com/recaptcha/api.js"></script>

<form method="post" action="/somewhere_else">
	... your form data ...
<button class="g-recaptcha" 
        data-sitekey="reCAPTCHA_site_key" 
        data-callback='onSubmit' 
        data-action='submit'>Submit</button>
</form>             

<script>
   function onSubmit(token) {
     document.getElementById("demo-form").submit();
   }
</script>
```

With this code for form the client will call the Google server for the *reCaptcha* validation and send the form data to *"/somewhere_else"* as our endpoint. 

This code is *Universal* so any backend you will use its allways be usefull. For more info about *reCaptcha* and how to use them you can read the [official Google Guide](https://developers.google.com/recaptcha/docs/v3)[^5]. 

[^5]: [Link](https://developers.google.com/recaptcha/docs/v3)

### Backend Python Flask and Requests

In my solution I use MailGun for send me the content of the form. This code send all the the content of the post without check it. It can be use for multiple form at the same time. 

All the config are environment variables so you can recicle the script without a lot of work and this script is ready for *serveless* implementations.

``` python
from flask import Flask, redirect
from flask import request
import requests as r
import os

DOMAIN = os.environ.get("DOMAIN")
API_KEY = os.environ.get("API_KEY")
SENDER_ALIAS = os.environ.get("SENDER_ALIAS")
SENDER_MAIL = f"mailgun@{DOMAIN}"
TO_MAIL = os.environ.get("TO_MAIL")
SUBJECT = os.environ.get("SUBJECT")
RECAPTCHA = os.environ.get("RECAPTCHA")
SUCCESS_URL = os.environ.get("SUCCESS_URL")

app = Flask(__name__)

def send_mailgun_message(message):
    auth = ("api", f"{API_KEY}")
    data = {
        "from": f"{SENDER_ALIAS} <{SENDER_MAIL}>",
        "to": TO_MAIL,
        "subject": SUBJECT,
        "text": message,
    }
    response = r.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages", auth=auth, data=data
    )
    return response.status_code

@app.route("/", methods=["GET", "POST"])
def hello_world():
    app.logger.error(request.method)
    if request.method == "GET":
        return "Hello, World!"
    if request.method == "POST":
        message = ""
        data = request.form[item]
        message += f"{item}\n{data}\n\n"
        send_mailgun_message(message)
        return redirect(SUCCESS_URL, code=302)
```

In this implementation you recive the post from the form and read the form data and send it to someone with MailGun. 
If you don't need to send but to save it you can easy change the *send_mailgun_message* with what you need.

## Alternative

With the html code show before you can have different endpoint. 
You can change the desination changing the function. 

For example you can send as email with SMTP or save into a database or some file in the server. The only limit is the Api Rest Post url for getting the data from the form.
