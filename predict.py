# --------------------------------------------------------------
# Predict.py: To test data on unseen data
# --------------------------------------------------------------

# Import necessary packages
import openai
import pandas as pd

# Fine-tuned model
fine_tuned_model_id = "YOUR FINE-TUNE ID"

# Open AI key
openai.api_key = "YOUR_API_KEY"


# Formats the system prompt and content to OpenAI format
def format_test(row):
    formatted_message = {"role": "system", "content": "You are a smart home command operator that interprets natural language commands and transforms them into actionable function calls. Provide these details as a JSON dict."},
    {"role": "user", "content": row['Command']}
    return formatted_message

# Predicts the assistant response based on unseen data
def predict(test_messages, fine_tuned_model_id):
    response = openai.ChatCompletion.create(
        model=fine_tuned_model_id, 
        messages=test_messages,
        # Add function calling
        functions=function_descriptions
    )
    return response.choices[0].message.content

# --------------------------------------------------------------
# Pre: Takes each row of the unseen data and passes into the model
# Post: Outputs assistant response based on that data
# --------------------------------------------------------------
def store_predictions(test_df, fine_tuned_model_id):
    test_df['Prediction'] = None
    for index, row in test_df.iterrows():
        test_message = format_test(row)
        prediction_result = predict(test_message, fine_tuned_model_id)
        test_df.at[index, 'Prediction'] = prediction_result

    test_df.to_csv("predictions.csv")

test_df = pd.read_csv("test_queries.csv")
store_predictions(test_df, fine_tuned_model_id)

# --------------------------------------------------------------
# Use OpenAI’s Function Calling Feature
# --------------------------------------------------------------

function_descriptions = [

    # control_device function
    {
      "name": "control_device",
      "description": "get the command to control a device",
      "parameters": {
          "type": "object",
          "properties": {
              "device": {
                  "type": "string",
                  "description": "device name"
              },
              "command": {
                  "type": "array",
                  "description": "A list containing the idx, type and val of the command",
                  "items": {
                      "type": "object",
                      "properties": {
                          "idx": {
                          "type": "string",
                          "description": "Represents the specific control within the device, like L1 for turning on or off, L2 for grinding and so on. Each idx specifies to a specific control"
                          },

                          "type": {
                              "type": "string",
                              "enum": ["0x81", "0x80"],
                              "description": "Denotes the command type, such as 0x81 for on commands and 0x80 for off"
                          },

                          "val": {
                              "type": "number",
                              "enum": [0, 1],
                              "description": ": Represents the state to which the device should be set, like 1 for on and 0 for off ."
                          }
                        },
                        "required": ["idx", "type", "val"]
                    }
                }
          },
        "required": ["device", "command"]
      },
    },

    # set_device_mode function
    {
      "name": "set_device_mode",
      "description": "get the command to control a device",
      "parameters": {
          "type": "object",
          "properties": {
              "device": {
                  "type": "string",
                  "description": "device name"
              },
              "command": {
                  "type": "array",
                  "description": "A list containing the idx, type and val of the command",
                  "items": {
                      "type": "object",
                      "properties": {
                          "idx": {
                          "type": "string",
                          "description": "Represents the specific mode of the device, like L1 for mode 1, L2 for mode 2 and so on. Each idx can be"+
                          " of a different mode eg: low for mode 1, medium for mode 2, high for mode 3"
                          },

                          "type": {
                              "type": "string",
                              "enum": ["0x81", "0x80"],
                              "description": "Denotes the command type, such as 0x81 for on commands and 0x80 for off"
                          },

                          "val": {
                              "type": "number",
                              "enum": [0, 1],
                              "description": ": Represents the state to which the device should be set, like 1 for on and 0 for off ."
                          }
                        },
                        "required": ["idx", "type", "val"]
                    }
                }
          },
        "required": ["device", "command"]
      },
    }
]

# User prompt - Input your own commands
user_prompt = "Turn on the kitchen light."

# Chat completion process
completion = openai.ChatCompletion.create(
  model=fine_tuned_model_id,
  messages=[
    {"role": "system", "content": "You are a smart home command operator that interprets natural language commands and transforms them into actionable function calls. Provide these details as a JSON dict."},
    {"role": "user", "content": user_prompt}
    ],
    # Add function calling
    functions=function_descriptions
)

# ---------------------------------------------------------------------
# EOF - Check predictions.csv for the predicted outputs by the model
# ---------------------------------------------------------------------