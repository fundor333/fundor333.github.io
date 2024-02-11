---
title: "Django With Barcode and Qrcode"
date: 2022-02-22T12:39:07+01:00
feature_link: "https://unsplash.com/photos/ZqjNiJnzZqw"
feature_text: "Photo by Katya Azi on Unsplash"
tags:
- django
- hacking
- api
- qrcode
- barcode
slug: "django-with-barcode-and-qrcode"
categories:
- post
- fingerfood
description: "How to make a django form for reading BarCode and QRCode"
type: "post"
meta:
---
For work I need to implement a strange usercase: I need to have a form with QRCode and BarCode input.

The short story: I need to read the info from a BarCode and find the book.

The long story: I need to read the barcode with a phone/tablet/something with a camera and post it in a django form. So I search on the web and find some solution.

## The premium solution

First solution I found is a premium solution. I find the [Dynamsoft](https://www.dynamsoft.com/)'s [tutorial](https://www.dynamsoft.com/barcode-reader/programming/python/user-guide.html) where you can build a script for read QrCode, BarCode, etc... but you need a license for your code to work.
It's an easy way IF you have the budget and I don't have it.
So I need something different.
An AI?

## The AI solution

After more searching I find some Google and Amazon solution for reading BarCode with AI but

1) It isn't free, it is a premium services
2) It's hard for the server (CPU intensive) and you need to send the photo to the server
3) You can run the code on the client but you need to make an app (iOS or Android)

So I need another solution.

## Other solution

I find a Perl solution (a big no no for me), some more Python solution (but you need to know where the BarCode is) and some magic tricks find in StackOverflow.

![Copy and Paste from StackOverflow](CopyPastingStackOverflow.jpeg)

And searching in StackOverflow I found the solution: an JS solution.

So I search some JS library and find a library: [Html5-QRcode](https://github.com/mebjas/html5-qrcode)

## The final solution

Making this template for the form you can scan the BarCode from the cam of the pc/phone/table and push the form with the info read.

``` html
<script src="https://unpkg.com/html5-qrcode" type="text/javascript">


<div id="reader" width="600px" height="600px"></div>

  <form id="form_isbn" method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Submit">
  </form>

  <script>
function onScanSuccess(decodedText, decodedResult) {
  // handle the scanned code as you like, for example:
  console.log(`Code matched = ${decodedText}`, decodedResult);
  document.getElementById('id_isbn').value = decodedText;
  document.getElementById('form_isbn').submit();
}

function onScanFailure(error) {
  // handle scan failure, usually better to ignore and keep scanning.
  // for example:
  console.warn(`Code scan error = ${error}`);
}

let html5QrcodeScanner = new Html5QrcodeScanner(
  "reader",
  { fps: 10, qrbox: {width: 250, height: 250} },
  /* verbose= */ false);
html5QrcodeScanner.render(onScanSuccess, onScanFailure);
  </script>
```

This code fragment is indipendent from the django version and the software installed in the server.
It's also all client side code so the server get only the string inside the BarCode/QrCode.
