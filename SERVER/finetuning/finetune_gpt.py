from openai import OpenAI
import config_server
client = OpenAI(api_key=config_server.OPENAI_API_KEY,)

def finetunemodel(datapath):
  response  = client.files.create(
    file=open(datapath, "rb"),
    purpose="fine-tune"
  )
  print("repsonse : ")
  print(response)
  file_id = response.id

  fine_tune_response  = client.fine_tuning.jobs.create(
    training_file=file_id, 
    model="gpt-3.5-turbo"
  )
  print("fine_tune_response")
  print(fine_tune_response)
  return fine_tune_response.id


  print("debug : ")

  # List 10 fine-tuning jobs
  print1 = client.fine_tuning.jobs.list(limit=10)
  print(print1)
  # Retrieve the state of a fine-tune
  print2 = client.fine_tuning.jobs.retrieve(fine_tune_response.id)
  print(print2)


if __name__ == "__main__":
    id = finetunemodel("othercolor_data.jsonl") 
    print2 = client.fine_tuning.jobs.retrieve(id)
    print(print2)