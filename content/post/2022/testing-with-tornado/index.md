---
title: "Testing With Tornado"
date: 2022-09-18T13:00:16+02:00
feature_link: "https://www.midjourney.com/home/"
feature_text: "by IA Midjourney"
tags:
- python
- tornado
- testing
- tox
slug: "testing-with-tornado"
categories:
- dev
- fingerfood
description: "How to test a Tornado application"

mp-syndicate-to:
- https://brid.gy/publish/twitter
- https://brid.gy/publish/mastodon
---

It is some time I start working with Tornado, and I have to say that I really like it. It is a very powerful framework, and it is very easy to use. But, as any other framework, it has its own way to do things, and it is not always easy to find the right way to do things. One of the things that I found difficult to find was how to test a Tornado application. I found a lot of examples, but they were not very clear, and I had to do a lot of research to find the right way to do it. In this post, I will try to explain how to test a Tornado application.

## Example of the Tornado application

This is a simple Tornado application that I will use to explain how to test it. It is a simple application that returns "Hello, World" or "Hello Name" if name param is fill. It is a very simple application, but it is enough to show how to test tornado code.

``` python
import asyncio
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_query_argument("name", "World")
        self.write(f"Hello, {name}")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
```

The core of this Tornado app is the "MainHandler" class. It is a very simple class that inherits from "tornado.web.RequestHandler". It has a "get" method that will be call and handle the get request.
The "make_app" function is a function that creates the Tornado application. It also manages the routes of the application. In this case, it only has one route, the "root" route, that will be handled by the "MainHandler" class.

All the remaining code is just to start the Tornado application. It is not important for the test, only for the application to run in production. I will not explain it in detail, but if you want to know more about it, you can read the [Tornado documentation](https://www.tornadoweb.org/en/stable/guide/structure.html).

## Testing the Tornado application

Now that we have the Tornado application, we can start testing it. The first thing that we need to do is to create a test file. I will call it "test_main.py". In this file, we will create a test class that will inherit from "tornado.testing.AsyncHTTPTestCase". This class will allow us to test the Tornado application.

``` python
import example
from tornado.testing import AsyncHTTPTestCase


class TestHelloApp(AsyncHTTPTestCase):
    def get_app(self):
        return example.make_app()

    def test_homepage(self):
        response = self.fetch("/")
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b"Hello, World")
        response = self.fetch("/?name=John")
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b"Hello, John")
```

In the TestHelloApp you need to implement the "get_app" method. This method will return the Tornado application that we want to test. In this case, it will return the application that we created in the "make_app" function but you can build custom routes for the tests but in this case we use the production's application.

After that, we can write the tests.
You need to create a test method that will start with "test_" (in this case test_homepage). In this method, you can use the "self.fetch" method to make a request to the application. This method will return a "Response" object that you can use to check the response of the application. In this case, we are checking that the response is 200 and that the body of the response is the correct string.

## Running the tests

After writing the tests, we can run them. To run the tests, we need to run the "unittest" module. We can do it in two ways.

The first one is to use the "pytest" module. In this case, we need to install the "pytest-tornado" module. After that, we can run the "pytest" module and it will find the tests in the test file.
The second one is to use tox to run the tests. In this case, we need to create a "pyproject.toml" file with the following content[^1]:
[^1]: This is the new way with pyproject.toml to define the dependencies of the project. You can read more about it in the [PEP 518](https://www.python.org/dev/peps/pep-0518/) and for tox part in the [tox documentation](https://tox.wiki/en/latest/example/basic.html#pyproject-toml-tox-legacy-ini).

``` toml
[build-system]
requires = [ "setuptools >= 35.0.2", "wheel >= 0.29.0"]
build-backend = "setuptools.build_meta"

[tool.tox]
legacy_tox_ini = """
[tox]
envlist = py27,py36

[testenv]
deps = pytest >= 3.0.0, <4
commands = pytest

[testenv:black]
basepython = python3
deps =
    black
commands =
    black --skip-string-normalization -t py39 .

[flake8]
exclude = .venv,.git,.tox,dist,doc,*egg,build
"""
```

With this file you can run the tests with the "tox" command.
You can use it with CI or locally to run the tests.

Good luck with your testing!
