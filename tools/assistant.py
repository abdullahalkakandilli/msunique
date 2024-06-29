import queue
import streamlit as st
import threading
import concurrent.futures
import json
from openai import OpenAI
from openai.types.beta.assistant_stream_event import (
    ThreadMessageCompleted,
    ThreadRunFailed,
)


COMPANY_LIST = ['ABB', 'IBM', 'PostFinance', 'Raiffeisen', 'Siemens', 'UBS']
VECTOR_DB = 'vs_YZqXl7Eo8tf2pEneRxbB2GrT'
ASSISTANT = 'asst_rjUmFNdSAWV5rrcAa3Sy6ADf'

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
results_queue = queue.Queue()
report_queue = queue.Queue()
executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
assistants_ = {}
prompts_ = {}


def generate_prompt(company):
    report_prompt = (
        f"Create a report for the company {company} considering your instructions"
    )
    return report_prompt


for company in COMPANY_LIST:
    assistants_[company] = ASSISTANT
    prompts_[company] = generate_prompt(company=company)

for c_name in COMPANY_LIST:
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": prompts_[c_name]}],
            }
        ]
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id, assistant_id=ASSISTANT, stream=True
    )

    for event in run:
        if isinstance(event, ThreadMessageCompleted):
            text_value = event.data.content[0].text.value
            break
        if isinstance(event, ThreadRunFailed):
            print(event)
            break

    with open(f"tools/reports/{c_name}_general_report.json", "w") as outfile:
        j_obj = text_value[8:-4]
        checked_obj = json.loads(j_obj)
        json.dump(checked_obj, outfile)


def getting_report_with_thread_logic():
    def run_thread(prompt, key_):
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}],
                }
            ]
        )
        run = client.beta.threads.runs.create(
            thread_id=thread.id, assistant_id=ASSISTANT, stream=True
        )
        for event in run:
            if isinstance(event, ThreadMessageCompleted):
                text_value = event.data.content[0].text.value
                results_queue.put({'text': text_value, 'key_': key_})

            if isinstance(event, ThreadRunFailed):
                print(event)
                break

    def submit_assistant_threads():
        futures = [
            executor.submit(
                run_thread(
                    prompt=prompts_.get(key),
                    key_=key,
                )
            )
            for key in assistants_.keys()
        ]
        for future in futures:
            report_queue.put(future)

    def process_assistant_threads():
        while True:
            try:
                future = report_queue.get(timeout=15)
                result = future.result()
            except queue.Empty:
                if (
                    not submit_thread.is_alive()
                ):  # Check if the submit_queries function has finished
                    break

    submit_thread = threading.Thread(target=submit_assistant_threads)
    process_thread = threading.Thread(target=process_assistant_threads)
    submit_thread.start()
    process_thread.start()

    submit_thread.join()
    process_thread.join()

    results = {}
    while not results_queue.empty():
        result = results_queue.get()
        key_ = result['key_']
        results[key_] = result['text']

    with open("tools/reports/whole.json", "w") as outfile:
        json.dump(results, outfile)
