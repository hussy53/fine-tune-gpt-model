
# Fine-Tuning a GPT Model for Smart Home Device Control

**Objective**:

*Develop and fine-tune a GPT model capable of interpreting natural language commands for
controlling smart home devices and fetching weather information, transforming these commands
into actionable function calls.*



## Process and library installments...
Libraries:
- openai
- random
- pandas

IDE:
- Visual Studio Code
- Jupyter Notebook or
- (Any of your choice)
## OpenAI API Models

The OpenAI API is powered by a diverse set of models with different capabilities and price points. You can also make limited customizations to our original base models for your specific use case with fine-tuning.




## Set Up

1. Download the folder from github onto your desktop.
2. Open the folder on your preferred IDE.
3. There are 4 files:
- *setup.py* - The setup file for fine-tuning the model. It consists of functions that create training and testing files based on the JSONL file and then uploads to Open AI to retreive the fine-tuned model.
- *main.py* - The main file that runs and tests the model on different input commands.
- *predict.py* - Trains the JSONL file on unseen data. This file is created for internal purposes to determine how well the model performs on unseen/untrained data.
- *conversations.jsonl* - This is a JSONL file used to train and test data and prepare the fine-tuned model.
- *test_queries.csv* - Unseen command file prepared to train for the fine-tuned model.

4. To deploy, open terminal and navigate to your folder and run:

```bash
  python .\setup.py
```
Once you retreive the fine-tuning model then run:

```bash
  python .\main.py
```

5. To see how it performs on unseen data, run:

```bash
  python .\predict.py
```


## Things to consider

1. Make sure to install all the libraries:

```bash
  pip install openai
  pip install random
  pip install pandas
```

2. Substitute 
- your own api key where it says ```YOUR_API_KEY```.
- the fine-tuned model ID where it says ```YOUR FINE-TUNE ID```.

3. To change commands, alter the ```user_prompt``` variable and put your own commands.

4. **Report**: Elaboration of the code in the report.
