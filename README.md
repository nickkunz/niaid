# NIAID DIR Laboratory Descriptions Data Set
This repo creates a data set of the National Institute of Allergy or Infectious Diseases (NIAID) Division of Intramural Research (DIR) organizational structure. The data set was created for later consumption into a Neo4j graph representation and subsequently integrated into the PubMed Knowledge Graph (PKG) for further analyses. To that end, the script outputs a CSV. In order to obtain the data, this repo utilizes web scraping directly from the information found in the NIAID DIR Laboratory Descriptions. It includes the following features of substantive interest.

_**Date:** Jan 2022_

_**Contact:** Nick Kunz, Deloitte Consulting LLP (nkunz@deloitte.com)_

## Data Features
1. **Name:** Name of the principal investigators, staff scientists, and staff clinicians. There are 180 unique names.
2.  **Education:** Research and training credentials for each name. There are 15 unique credentials.
3. **Branch:** The branch name nested within the DIR. There are 20 unique branches.
4. **Section:** The section/unit name nested within its respective branch. There are 162 unique sections.

## Dependencies
1. **Python** (3.8.2): Language
2. **Pandas** (1.2.4): Dataframes for data manipulation
3. **Requests** (2.26.0): Web requests for naviation
3. **Selenium** (3.141.0): Framework for web automation
4. **TQDM** (4.61.2): Progress bar for job status and completion
5. **GeckoDriver** (0.30.0): WebDriver utilized in Selenium 

_Note: All dependencies are installed automatically when running as a Docker Container. However, if executed as a Jupyter Notebook, these dependencies will need to be installed manually._

## Getting Started

The data set is located in the directory ```/data/niaid-dir-org.csv```. There you will find the results from the source. If desired, the data set can be built the following two ways.

The first is with a **Docker Container** (highly recommended). The second is with the **Jupyter Notebook** located in the directory ```/notebooks/niaid-dir.ipynb``` . Below are the instructions for both.

### Docker Container

1. Ensure that Docker is installed on your local machine. If not, you can download it here: 

    https://docs.docker.com/get-docker/

2. Clone this repo to a local directory and navigate to the project folder.

    ```cd <path to project folder>```

3. Build the Docker container.

    ```docker build -t niaid-dir-org .```

    _Note: this step may take awhile, especially if you're building the container for the first time._

4. Run the Docker container.

    ```docker run --name data niaid-dir-org```

    To run this container again after a failed attempt, you can choose to either 1) run it under a different name (```--name <different-name>```) or 2) run it under the same name (```--name data```). 
    
    Choosing the later will require you to remove the dangling image. This can be a accomplished with the following:

    ```docker system prune```

    Alternatively, you can open Docker Desktop, navigate to Containers / Apps, hover over the selection and delete it.

5. Copy data set from the Docker container to your local machine.

    ```docker cp data:/usr/local/niaid-dir-org.csv <path on host machine> ```

    At this time, web scraping is complete and the NIAID DIR data set should appear in the specified path on your local machine (```<path on host machine>/niaid-dir-org.csv```).

### Juypter Notebook

1. Ensure that Python 3.8.2 is installed on your local machine. If not, you can download it here: 

    https://www.python.org/downloads/release/python-382/

2. Ensure that the required libraries are installed on your local machine with the correct versions.

    ```
    pip install pandas==1.2.4
    pip install requests==2.26.0
    pip install selenium==3.141.0
    pip install tqdm==4.61.2
    ```

    Alternatively, you can install them using ```requirements.txt```.
    ```
    py -3.8 -m pip install -r requirements.txt
    ```

3. Ensure that an executable GeckoDriver is installed on your local machine. If not, you can download it here:

    https://github.com/mozilla/geckodriver/releases

    Alternatively, if your local machine is Windows, you can enable GeckoDriver auto download by uncommenting the following block of code located in the **Execution** section of the notebook (near the bottom).

    ```
    gecko_downloader(os = 'win64')
    ```

    _Note: Notebook only supports GeckoDriver auto download on Windows machines. If you are running Linux or Mac, you will need to download GeckoDriver and specify its excutable path manually. Also, requires Python kernel to accept web requests._

4. Specify the GeckoDriver executable path and data set output path on your local machine with the block of code found in the **Execution** section of the notebook (near the bottom).
    ```
    exe_path = './geckodriver.exe'
    csv_path = '../data/niaid-dir-org.csv'
    ```

5. Run all blocks. The **Execution** block should return of the following upon successful completion.

    ```
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 228 entries, 0 to 227
    Data columns (total 4 columns):
    #   Column     Non-Null Count  Dtype 
    ---  ------     --------------  ----- 
    0   Name       228 non-null    object
    1   Education  228 non-null    object
    2   Branch     228 non-null    object
    3   Section    228 non-null    object
    dtypes: object(4)
    memory usage: 7.2+ KB
    ```
    At this time, web scraping is complete and the NIAID DIR data set should appear in the specified path on your local machine (```<path on host machine>/niaid-dir-org.csv```).

## References
National Institute of Allergy and Infectious Diseases. (Nov. 2021). Division of Intramural Research Laboratory Descriptions. https://www.niaid.nih.gov/research/division-intramural-research-labs. [Accessed: Jan. 2022]
