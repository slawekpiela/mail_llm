import time
from openai import OpenAI
from configuration import api_key, assistant_id,Models

client = OpenAI(api_key=api_key)


def query_model(prompt):
    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )

    thread_messages = client.beta.threads.messages.list(thread.id)

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
        instructions="You are helpfull assistant. Answer in the shortest way possible. Answer only based on information in the files. Answer in Polish language. If you do not find answer in the files say 'I do not know the answer' ",

        #tools=[{"type": "retrieval"}]
    )

    status = "start"
    count=0
    print("\n")
    while status != "completed":
     result = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
     )
     status=result.status
     print("\rStatus: ",status, count, end="") #"Status",count, result.status, end="\r")  # print current status
     count=count+1
     time.sleep(1)

    messages = client.beta.threads.messages.list(thread_id=thread.id) # ststus is completes. get completion

    result= messages.data[0].content[0].text.value # extract text from cpmpletion
    full_result= messages
    return result, full_result
