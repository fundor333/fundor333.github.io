---
title: "Why I Stop Making Script and Start to Make Bash Terminal Commands"
date: 2023-05-19T13:32:33+02:00
feature_link: "https://www.midjourney.com/home/"
feature_text: "by IA Midjourney"
tags:
- script
- bash
- command line
slug: "why-i-stop-making-script-and-start-to-make-bash-terminal-commands"
categories:
- coding
- hacking
description: ""
type: "post"
mp-syndicate-to:
- https://brid.gy/publish/twitter
- https://brid.gy/publish/mastodon
images:
keywords:
- pythons
- terminal
---

## The script folder of DOOM

I am a developer from a long time and, like other developer I know, I have the script/dump folder where I copy all the usefull script I find online or I wrote with blood and stackoverflow. And this toolbox of scripts became big and bigger more script I add.

![Wes Anderson inspired img of tools on the wall](toolbox.png)

So last week I made some changes. I merge some script (python in my case) in one bigger script/project and convert it in a tool for my command line.
For example I merge some script which check DNS, server status and NS statud in a unique terminal program so i can launch some command like ***dnstool check_ns --target fundor333.com*** and it check the NS of site I want. And If I don't remember the parameters I have an help command for the man of the app.

In this way I can't forget what a command do or how many parameters I need to use for the specific command.

## What do I use for the commands? Bash, SH, Perl, Python?

For the commands I implements I use [Typer](https://typer.tiangolo.com/) a python library to build CLIs.

I find easyer than [Click](https://click.palletsprojects.com/) [^1] and if you install the full package has also [Rich](https://rich.readthedocs.io/en/stable/introduction.html) [^2]
[^1]: Famous CLI library for python
[^2]: Python library for writing rich text to the terminal and show advance content

![Tywriter](typewriter.png)

For example I need to check some DNS configuration and I call the dog program for the checks.

``` python
import subprocess
from typing import List
import typer
from rich.table import Table
from rich.console import Console

app = typer.Typer()


@app.command()
def dns_check(
    url: str,
    dns: List[str] = ["8.8.8.8","8.8.4.4"],
    type: str = 'A',
):
    table = Table()
    table.add_column("Type", justify="right", style="cyan", no_wrap=True)
    table.add_column("Url", style="magenta")
    table.add_column("Time", justify="right")
    table.add_column("Record", justify="right", style="green")
    for e in dns:
        result = subprocess.run(['dog', url, f'@{e}', type], stdout=subprocess.PIPE)
        for a in result.stdout.decode('utf-8').split('\n'):
            print(a)
            table.add_row(*a.split())
    console = Console()
    console.print(table)


if __name__ == "__main__":
    app()

```

After some time I need to have something which can query multiple site for the https. So I added some code inside the command

``` python
from urllib.parse import urlparse
import http.client
import sys

@app.command()
def check_https(url:str):
    url = urlparse(url)
    conn = http.client.HTTPConnection(url.netloc)
    conn.request('HEAD', url.path)
    console = Console()
    if conn.getresponse():
        console.print(f"[green]{url}")
    else:
        console.print(f"[red]{url}")
``` 

With this command added the cli become more compless with a help autogenerate. 
At the end the script/cli will look like some like this

``` python
import subprocess
from typing import List
import typer
from rich.table import Table
from rich.console import Console
from urllib.parse import urlparse
import http.client
import sys

app = typer.Typer()


@app.command()
def dns_check(
    url: str,
    dns: List[str] = ["8.8.8.8","8.8.4.4"],
    type: str = 'A',
):
    table = Table()
    table.add_column("Type", justify="right", style="cyan", no_wrap=True)
    table.add_column("Url", style="magenta")
    table.add_column("Time", justify="right")
    table.add_column("Record", justify="right", style="green")
    for e in dns:
        result = subprocess.run(['dog', url, f'@{e}', type], stdout=subprocess.PIPE)
        for a in result.stdout.decode('utf-8').split('\n'):
            print(a)
            table.add_row(*a.split())
    console = Console()
    console.print(table)

@app.command()
def check_https(url:str):
    url = urlparse(url)
    conn = http.client.HTTPConnection(url.netloc)
    conn.request('HEAD', url.path)
    console = Console()
    if conn.getresponse():
        console.print(f"[green]{url}")
    else:
        console.print(f"[red]{url}")
        
if __name__ == "__main__":
    app()
``` 

Like this I have multiple other CLI for email, printers, networks, servers, etc and I have something more clean and organize than a bin of scripts.

![Paper](paper_organizided.png)

At the end of the day having a lot of script can be a growing problem but if you can convert them in cli operation and command you can have some sort of order for your scripts.

Have nice time making your CLI


### **Update** 

[Here]({{< ref "/post/2024/why-do-i-disinstall-pipenv-and-use-only-poetry" >}} "Here") you can find some update about the way I write code and my personal utility
