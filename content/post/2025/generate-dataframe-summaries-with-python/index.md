---
date: '2025-09-03T17:13:02+08:00'
title: Generate Dataframe Summaries With Python
feature_link: https://www.midjourney.com/home/
feature_text: by AI Midjourney
description: How to generate dataframe summaries with python and AI for a type of
  dataset
isStarred: false
tags:
- datascience
- dataframe
- pandas
- llm
- Ollama
- mistral
categories:
- dev
images: null
keywords: null
series:
- Data and Data Tools
syndication:
- https://mastodon.social/@fundor333/115141868712801218
comments:
  host: mastodon.social
  username: fundor333
  id: '115141868712801218'
---

How much time do you spend with making summaries of dataset? Too much and I don't like doing it so I search to do it with the AI. So this is my sperimentation with some medical data see at PyDataVe 22nd event and Mistral model.

## The code for the inizializzation

For start I need to install some dipendency

~~~ text
langchain>=0.3.27
langchain-ollama>=0.3.7
pandas>=2.3.2
~~~


```python
import pandas as pd
from langchain_ollama import ChatOllama
from typing import Literal

df = pd.read_csv("data/test.csv")

print("-*-" * 20)
print(f"Dataset shape: {df.shape}")
print("-*-" * 20)
print("Missing value stats:")
print(df.isnull().sum())
```

    -*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-
    Dataset shape: (418, 20)
    -*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-
    Missing value stats:
    ID                 0
    N_Days             0
    Status             0
    Drug             106
    Age                0
    Sex                0
    Ascites          106
    Hepatomegaly     106
    Spiders          106
    Edema              0
    Bilirubin          0
    Cholesterol      134
    Albumin            0
    Copper           108
    Alk_Phos         106
    SGOT             106
    Tryglicerides    136
    Platelets         11
    Prothrombin        2
    Stage              6
    dtype: int64


This is a section of the dataset and what is missing value of the stats.

Now we will start with the AI. In my case I user Ollama with Mistral model.
I install the model with

~~~ bash
ollama run mistral
~~~

And prepare the code for use the model. First you need to make a connection with the local LLM instance. This code use Mistral but you can pass any local LLM instance you have.



```python
def get_llm(model_name: str = "mistral:latest") -> ChatOllama:
    """
    Create and configure a ChatOllama instance for local LLM inference.

    This function initializes a ChatOllama client configured to connect to a
    local Ollama server. The client is set up with deterministic output
    (temperature=0) for consistent responses across multiple calls with the
    same input.

    Parameters
