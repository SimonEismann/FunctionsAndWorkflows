# FunctionsAndWorkflows
The code for the functions and workflows used in our manuscript "Predicting the Costs of Serverless Workflows".

## Functions
The five folders correspond to the functions Text2Speech, Profanity-Detection, Conversion, Censor and Compression. Each function consists of a main.py containing the function code and a requrements.txt that specifies the required python libraries. These files can be deployed using the Google Cloud UI. During our experimentation, each function was deployed with 512 MB.

## Workflows
The files WorkflowA.py and WorkflowB.py are an Airflow implementation of the workflows WorkflowA and WorkflowB from the manuscript. They can be deployed on an Airflow cluster as Jobs using the Airflow UI. For the experiments on Google Cloud, we used Google Cloud Composer, a managed Airflow solution.
