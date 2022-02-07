# FunctionsAndWorkflows
The code for the functions and workflows used in our manuscript "Predicting the Costs of Serverless Workflows".

## Functions
The five folders correspond to the functions Text2Speech, Profanity-Detection, Conversion, Censor and Compression. Each function consists of a main.py containing the function code and a requrements.txt that specifies the required python libraries. These files can be deployed using the Google Cloud UI. During our experimentation, each function was deployed with 512 MB.

## Workflows
The files WorkflowA.py and WorkflowB.py are an Airflow implementation of the workflows WorkflowA and WorkflowB from the manuscript. They can be deployed on an Airflow cluster as Jobs using the Airflow UI. For the experiments on Google Cloud, we used Google Cloud Composer, a managed Airflow solution.

## Cite Us

The audio processing workflows were first used in our manuscript [Predicting the Costs of Serverless Workflows](https://doi.org/10.1145/3358960.3379133). If you find them useful, please cite the following publication:

    @inproceedings{EiGrEyHeKo2020-ICPE-ServerlessWorkflows,
      author = {Eismann, Simon and Grohmann, Johannes and van Eyk, Erwin and Herbst, Nikolas and Kounev, Samuel},
      booktitle = {Proceedings of the 2020 ACM/SPEC International Conference on Performance Engineering},
      month = {April},
      pages = {265–276},
      series = {ICPE '20},
      title = {Predicting the Costs of Serverless Workflows},
      year = 2020
    }
