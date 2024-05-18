# --------------------------------------------------------------
# setup.py: Retreiving the fine-tuned model id
# --------------------------------------------------------------

# Import necessary packages
import openai
import random
import time

# Open AI api key
openai.api_key = "sk-proj-0SF6MpP1H0wrOgxek1kfT3BlbkFJ8WavPhfOBSQDTzcanFMW"


# Splits the lines of the input file into training and evaluation files.
def split_file(input_filename, train_filename, eval_filename, split_ratio=0.8, max_lines=100):

    with open(input_filename, 'r') as infile:
        lines = infile.readlines()
    
    # Shuffle lines to ensure randomness
    random.shuffle(lines)

    lines = lines[:max_lines]

    # Calculate the number of lines for training
    train_len = int(split_ratio*len(lines))

    # Split the lines
    train_lines = lines[:train_len]
    eval_lines = lines[train_len:]

    # Write to the respective files
    with open(train_filename, 'w') as trainfile:
        trainfile.writelines(train_lines)

    with open(eval_filename, 'w') as evalfile:
        evalfile.writelines(eval_lines)

split_file('./conversations.jsonl', 'DATA_train.jsonl', 'DATA_eval.jsonl')
print("Splitting data into train and test completed...")
time.sleep(2)
print("Now extracting train and test ids...")
time.sleep(3)

# Upload training data
train = openai.File.create(
    file=open('DATA_train.jsonl', 'rb'),
    purpose='fine-tune'
)
train_id = train['id']
print(f"Train ID generated: {train_id}")
time.sleep(2)

# Upload validation data
val = openai.File.create(
    file=open('DATA_eval.jsonl'),
    purpose='fine-tune'
)
val_id = val['id']
print(f"Validation ID generated: {val_id}")
time.sleep(3)


# Creating the fine-tuned model
response = openai.FineTuningJob.create(
  training_file=train_id,
  validation_file=val_id, 
  model="gpt-3.5-turbo",
  hyperparameters={
      "n_epochs":2
  }
)

# Retrieve the state of a fine-tune
job_id = response['id']

# Fine-tuned model
fine_tuned_model_id = response['fine_tuned_model']

print(f"Fine-tuned model ID: {fine_tuned_model_id}")
time.sleep(4)
print(f"Generating the fine-tuned model may take time. Please store the job ID and check the status after sometime: {job_id}")
response = openai.FineTuningJob.retrieve(job_id)

# Uncomment the comment below to print the status of the fine-tuning job
# print(response)


# --------------------------------------------------------------
# EOF - Please put the fine-tuned model ID in main.py
# --------------------------------------------------------------