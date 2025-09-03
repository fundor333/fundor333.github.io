---
date: '2025-09-03T17:13:02+08:00'
title: 'Generate Dataframe Summaries With Python'
feature_link: "https://www.midjourney.com/home/"
feature_text: "by AI Midjourney"
description: 'How to generate dataframe summaries with python and AI for a type of dataset'
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
images:
keywords:
series:
- Data and Data Tools
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
    ----------
    model_name : str, optional
        The name of the Ollama model to use for chat completions.
        Must be a valid model name that is available on the local Ollama
        installation. Default is "mistral:latest".

    Returns
    -------
    ChatOllama
        A configured ChatOllama instance ready for chat completions.
    """
    return ChatOllama(
        model=model_name, base_url="http://localhost:11434", temperature=0
    )
```

If you want to test the connection you can use this command


```python
print(get_llm().invoke("test").content)
```

     Hallo! Wie geht es Ihnen? Ich bin hier, um Ihnen zu helfen. Was möchten Sie heute tun?

    Ich kann Ihnen beispielsweise helfen:

    * Fragen beantworten
    * Informationen suchen
    * Aufgaben lösen
    * und vieles mehr!

    Welche Aufgabe haben wir heute vor uns?


## Make a context

Now we need to generate a context for the LLM. If you do this function with all the necessary data you can relaunch this script every time you need a new README/summary of the dataset. This is better to be a dataset with a fixed schema and a date which change every year like medical data (this), monthly sell report, census data...


```python
def get_summary_context_message(df: pd.DataFrame, dataset_name:str) -> str:
    # Basic application statistics
    total_analisys = len(df)

    # Gender distribution
    gender_counts = df["Sex"].value_counts()
    male_count = gender_counts.get("M", 0)
    female_count = gender_counts.get("F", 0)

    # Stage Statistics
    stage_data = df["Stage"].dropna()
    stage_avg = stage_data.mean()
    stage_25th = stage_data.quantile(0.25)
    stage_50th = stage_data.quantile(0.50)
    stage_75th = stage_data.quantile(0.75)

    # NDays Statistics
    days_data = df["N_Days"].dropna()
    days_avg = days_data.mean()
    days_25th = days_data.quantile(0.25)
    days_50th = days_data.quantile(0.50)
    days_75th = days_data.quantile(0.75)

    def status_category(exp):
        if pd.isna(exp):
            return "Unkown"
        elif exp == "C":
            return "Censored"
        elif exp == "CL":
            return "Censored due to Lever tx"
        elif exp == "D":
            return "Death"
        else:
            return "Unkow"

    df['Status Str']= df['Status'].apply(status_category)
    status_str_stats = []

    for category in ["Censored", "Censored due to Lever tx", "Death",]:
        category_data = df[df["Status Str"] == category]
        if len(category_data) > 0:
            male = len(category_data[category_data["Sex"] == "M"])
            female = len(category_data[category_data["Sex"] == "F"])
            total = len(category_data)
            rate_m = (male / total) * 100
            rate_f = (female / total) * 100
            status_str_stats.append((category, male, female, total, rate_m, rate_f))

    summary =f"""{dataset_name}

Total Analisys: {total_analisys:,}

Gender Distribution:
- Male applicants: {male_count:,} ({male_count/total_analisys*100:.1f}%)
- Female applicants: {female_count:,} ({female_count/total_analisys*100:.1f}%)

Stage Statistics:
- Average Stage: {stage_avg:.2f}
- 25th percentile: {stage_25th:.2f}
- 50th percentile (median): {stage_50th:.2f}
- 75th percentile: {stage_75th:.2f}

N Day Statistics:
- N Days Stage: {days_avg:.2f}
- 25th percentile: {days_25th:.2f}
- 50th percentile (median): {days_50th:.2f}
- 75th percentile: {days_75th:.2f}
"""

    summary += "\n\nStatus Rates by Sex:"
    for category, male, female, total, rate_m, rate_f in status_str_stats:
        summary += (
            f"\n- {category}: {male}/{total} Male ({rate_m:.1f}% rate)"+
            f"\n- {category}: {female}/{total} Female ({rate_f:.1f}% rate)"

        )
    return summary

```

## Make a report

After checking all you need to have a template for the repo of the dataset.


```python
SUMMARIZE_DATAFRAME_PROMPT = """
You are an expert data analyst and data summarizer.
Your task is to take in complex datasets and return user-friendly descriptions and findings.

You were given this dataset:
- Name: {dataset_name}
- Source: {dataset_source}

This dataset was analyzed in a pipeline before it was given to you.
These are the findings returned by the analysis pipeline:

<context>
{context}
</context>

Based on these findings, write a detailed report in {report_format} format.
Give the report a meaningful title and separate findings into sections with headings and subheadings.
Output only the report in {report_format} and nothing else.

Report:
"""
```

This prompt and a lot of the code of this article are from [this post](https://towardsdatascience.com/llms-pandas-how-i-use-generative-ai-to-generate-pandas-dataframe-summaries-2/).

After this we need a function that take the dataset *df*, the prompt *SUMMARIZE_DATAFRAME_PROMPT* with the needed info and return the content of the report.


```python
def get_report_summary(
    dataset: pd.DataFrame,
    dataset_name: str,
    dataset_source: str,
    report_format: Literal["markdown", "html"] = "markdown",
) -> str:
    context_message = get_summary_context_message(df=dataset, dataset_name=dataset_name)
    prompt = SUMMARIZE_DATAFRAME_PROMPT.format(
        dataset_name=dataset_name,
        dataset_source=dataset_source,
        context=context_message,
        report_format=report_format,
    )
    return get_llm().invoke(input=prompt).content
```

In our case we launch it as


```python
md_report = get_report_summary(
    dataset=df,
    dataset_name="Cirrhosis Patient Survival Prediction",
    dataset_source="https://www.kaggle.com/datasets/joebeachcapital/cirrhosis-patient-survival-prediction/data"
)
print(md_report)
```

     # Cirrhosis Patient Survival Prediction Analysis Report

    ## Overview
    The dataset analyzed consists of 418 records related to cirrhosis patients, sourced from [Kaggle](https://www.kaggle.com/datasets/joebeachcapital/cirrhosis-patient-survival-prediction/data). The data provides information about the patient's gender, stage of cirrhosis, number of days since diagnosis, and final status (censored or death).

    ## Demographics
    ### Gender Distribution
    The dataset shows a significant imbalance in gender distribution with 89.5% female applicants (374) and only 10.5% male applicants (44).

    ## Cirrhosis Stage Statistics
    ### Average Stage
    The average stage of cirrhosis for the analyzed patients is 3.02, indicating a severe level of liver damage.

    ### Percentiles
    - **25th percentile**: The cirrhosis stage is at least 2.00 for 25% of the patients.
    - **Median (50th percentile)**: Half of the patients have a cirrhosis stage of 3.00.
    - **75th percentile**: For 75% of the patients, the cirrhosis stage is 4.00 or lower.

    ## N Days Statistics
    ### N Days Stage
    The average number of days since diagnosis for the analyzed patients is 1917.78 days.

    ### Percentiles
    - **25th percentile**: The minimum number of days since diagnosis for 25% of the patients is 1092.75 days.
    - **Median (50th percentile)**: Half of the patients have been diagnosed with cirrhosis for at least 1730.00 days.
    - **75th percentile**: For 75% of the patients, the number of days since diagnosis is 2613.50 days or less.

    ## Status Rates by Sex
    The following table shows the rates of different statuses (censored due to Lever tx and death) for both male and female applicants:

    |                     | Male Applicants | Female Applicants |
    |---------------------|-----------------|-------------------|
    | Censored            | 17/232 (7.3%)    | 215/232 (92.7%)   |
    | Censored due to Lever tx | 3/25 (12.0%)     | 22/25 (88.0%)     |
    | Death                | 24/161 (14.9%)   | 137/161 (85.1%)   |

    The analysis indicates that female applicants are more likely to have their status censored, either due to the lack of information or other factors, while male applicants are more likely to experience death. However, it's important to note that the sample size for male applicants is significantly smaller than that of female applicants.

