# NIAID DIR Laboratory Descriptions & Section Similarity
This repo is the implementation guide for building a novel data set of the National Institute of Allergy and Infectious Diseases (NIAID) Division of Intramural Research (DIR) organizational structure and integrating it into the PubMed Knowledge Graph (PKG) Graph DB for constructing a similarity matrix of lab sections based on 7 dimensions of similarity.

Broadly, there are 3 main phases conducted in this analysis. They are the following:

1. **NIAID DIR Data Set:** Creates a novel data set of the NIAID DIR organizational structure.
2. **PKG Graph DB Integration:** Adds the NIAID DIR data set to an existing PKG Graph DB.
3. **NIAID DIR Section Similarity:** Calculates and combines 7 dimensions of similarity using data from the PKG Graph DB integrated with the NIAID DIR data set.


This repo is organized into folders. The following is a guide:

* ```/data/``` : CSV files as outputs and for use in Jupyter Notebooks and Neo4j
* ```/media/``` : Plots and figures as outputs from Jupyter Notebooks and Neo4j.
* ```/notebooks/``` : Jupyter Notebooks for data and analyses.
* ```/queries/``` : Cypher queries used in Neo4j.
* ```/source/``` : Python scripts used in Docker for building the NIAID DIR Data Set.
* ```/``` : Root folder containing docs, license, dependencies, and bash script for Docker.

_**Contacts:**_
* _Nick Kunz, Deloitte Consulting LLP (nkunz@deloitte.com)_
* _Joshua Porter, Deloitte Consulting LLP (joporter@deloitte.com)_
* _Elene Nakas, Deloitte Consulting LLP (enakas@deloitte.com)_

_**Date:** Feb 2022_

<br><br>

# 1. NIAID DIR Data Set
 The first phase of the analysis creates a novel data set of the NIAID DIR organizational structure. It was created for later consumption into Neo4j and subsequently integrated into a PubMed Knowledge Graph (PKG) Graph DB for further analyses. To that end, the script outputs a CSV. In order to obtain the data, this repo utilizes web scraping directly from the information found in the NIAID DIR Laboratory Descriptions. It includes the following features of substantive interest.

## Data Features
1. **Name** (object): Name of the principal investigators, staff scientists, and staff clinicians. There are 180 unique names.
2.  **Education** (object): Research and training credentials for each name. There are 15 unique credentials.
3. **Branch** (object): The branch name nested within the DIR. There are 20 unique branches.
4. **Section** (object): The section/unit name nested within its respective branch. There are 162 unique sections.

    _Note: All features (1 to 4) contain string values. Length, n = 228 (non-null)._

## Dependencies
1. **Python** (3.8.2): Language
2. **Pandas** (1.2.4): Dataframes for data manipulation
3. **Requests** (2.26.0): Web requests for navigation
3. **Selenium** (3.141.0): Framework for web automation
4. **TQDM** (4.61.2): Progress bar for job status and completion
5. **GeckoDriver** (0.30.0): WebDriver utilized in Selenium
6. **Docker** (4.4.4): Framework for containerization
7. **Jupyter** (2022.1.110): Notebook support for interactive Python development

_Note: All dependencies are installed automatically when running as a Docker Container. However, if executed as a Jupyter Notebook, these dependencies will need to be installed manually._

## Data Set Build

The data set is located in the directory ```/data/niaid-dir-org.csv```. There you will find the results from the source. If desired, the data set can be built using one the following two ways.

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

    Alternatively, you can install them using the requirements text file located in the repo's root folder (```/requirements.txt```).
    ```
    py -3.8 -m pip install -r requirements.txt
    ```
3. Locate the NIAID DIR Laboratory Descriptions Data Set notebook contained in this repo (```/notebooks/niaid-dir-org.ipynb```).


4. Ensure that an executable GeckoDriver is installed on your local machine. If not, you can download it here:

    https://github.com/mozilla/geckodriver/releases

    Alternatively, if your local machine is running Windows, you can enable GeckoDriver auto download by uncommenting the following block of code located in the **Execution** section of the notebook (near the bottom).

    ```
    gecko_downloader(os = 'win64')
    ```

    _Note: Notebook only supports GeckoDriver auto download on Windows machines. If you are running Linux or Mac, you will need to download GeckoDriver and specify its excutable path manually. Also, requires Python kernel to accept web requests._

5. Specify the GeckoDriver executable path and data set output path on your local machine with the code block found in the **Execution** section of the notebook (near the bottom).
    ```
    exe_path = './geckodriver.exe'
    csv_path = '../data/niaid-dir-org.csv'
    ```

6. Run all code blocks. The **Execution** block should return of the following upon successful completion.

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

<br><br>

# 2. PKG Graph DB Integration
The second phase of the analysis integrates the NIAID DIR Data Set into an existing PubMed Knowledge Graph (PKG) Graph DB implemented in Neo4j. It assumes access to or build of the PKG into a graph representation. In this context, the PKG Graph DB was pre-built. This assumption is one of the many limitations in this implementation, as it assumes quite a lot. However, if the assumption is met, these instructions remain valid.

## Dependency
1. **Neo4j** (4.3.7): Framework for Graph DB with Cypher

## Graph DB Integration
1. Locate the NIAID DIR data set contained in this repo (```/data/niaid-dir-org.csv```).
2. Launch Neo4j (4.3.7) with an existing PKG Graph DB (https://neo4j.com/download). 
3. Copy the NIAID DIR data set to the Neo4j import path of the existing PKG Graph DB (```<neo4j dbms path>/import/niaid-dir-org.csv```).
4. Add the NIAID DIR data set into the existing PKG Graph DB by executing the integration query (```/queries/int-pkg.cql```). The following is a preview.
    ```
    // load niaid data
    LOAD CSV WITH HEADERS FROM 'file:///niaid-dir-org.csv' AS i
    WITH i

    // create niaid nodes
    MERGE (n:NAME {Name: i.Name})
    MERGE (e:EDUCATION {Name: i.Education})
    MERGE (b:BRANCH {Name: i.Branch})
    MERGE (s:SECTION {Name: i.Section})

    // create niaid relationships
    MERGE (n)-[:HAS]->(e)
    MERGE (n)-[:BELONGS_TO]->(s)
    MERGE (s)-[:PART_OF]->(b)

    ...(full query continued in: "/queries/int-pkg.cql")
    ```
5. Ensure the NIAID DIR data set has been successfully added with the verification query (```/queries/int-pkg-ver.cql```).

    ```
    // verify niaid data into pkg
    MATCH (p:PERSON)-[:PROXY_TO]-(n:NAME)-[:BELONGS_TO]-(s:SECTION)-[:PART_OF]->(b:BRANCH)
    RETURN p, n, s, b
    ```
    ![NIAID DIR Graph DB](/media/pkg-ver.png)
    At this time, NIAID DIR data set integration into the existing PKG Graph DB is complete and should be functioning for the next phase of the analysis.

<br><br>

# 3. NIAID DIR Section Similarity
The third phase of the analysis conducts Jaccard Similarity using the PKG Graph DB for the 7 specified similarity metrics of substantive interest. It also concatenates the data sets produced from the table results. The data sets were combined for later transformation in to a similarity matrix for visualization and consumption. To that end, the script outputs a pairwise similarity table and two similarity matrix plots. In order to obtain the data, this notebook utilizes the CSV files that were exported from Neo4j. It includes the following features of substantive interest.

## Data Features
1. **Section A** (object): A given lab section name.
2. **Section B** (object): A given lab section name, not including a duplicate from Section A.
3. **Journal Category** (float64): Lab section similarity measured by publications in the same journal category.
4. **Journal Title** (float64): Lab section similarity measured by publications in the same journal.
5. **Keyword** (float64): Lab section similarity measured by publications containing the same keyword.
6. **MeSH** (float64): Lab section similarity measured by publications containing the same Medical Subject Heading (MeSH).
7. **Paper** (float64): Lab section similarity measured by co-authored publications.
8. **Project Category** (float64): Lab section similarity measured by projects with overlapping project spending category.
9. **Project Term** (float64):** Lab section similarity measured by projections with overlapping terms.
10. **Normal Inverse Distance** (float64): Normalized n-Dimensional Inverse Euclidean Distance, used for combining individual measurements of similarity.

    _Note: Lab section name features (1 to 2) contain string values. Lab section similarity features (3 to 10) contain float values bound between 0 and 1. Length, n = 12880 (non-null)._

## Dependencies
1. **Python** (3.8.2): Language
2. **NumPy** (1.21.4): Scientific computing
3. **Pandas** (1.2.4): Dataframes for data manipulation
4. **Matplotlib** (3.5.1): Data visualization
5. **Seaborn** (0.11.2): Data visualization
6. **Jupyter** (2022.1.110): Notebook support for interactive Python development
7. **Neo4j** (4.3.7): Framework for Graph DB with Cypher

## Section Similarity
1. Launch Neo4j (4.3.7) with an existing PKG Graph DB (https://neo4j.com/download).

2. Conduct Jaccard Similarity seperately for each dimension of similarity specified in the section similarity queries (```/queries/sec-sim.cql```). The following is one example.
    ```
    // section node similarity by paper co-authorship
    MATCH (s1:SECTION)<-[:BELONGS_TO]-(:NAME)-[:PROXY_TO]-(:PERSON)-[:AUTHORED]->(p1)
    WITH s1, collect(id(p1)) as p1_papers
    MATCH (s2:SECTION)<-[:BELONGS_TO]-(:NAME)-[:PROXY_TO]-(:PERSON)-[:AUTHORED]->(p2) 
    WHERE s1 <> s2 AND s1.Name > s2.Name
    WITH s1, p1_papers, s2, collect(id(p2)) AS p2_papers
    RETURN s1.Name AS section_a, s2.Name AS section_b,
        gds.alpha.similarity.jaccard(p1_papers, p2_papers) AS paper_similarity
    ORDER BY paper_similarity DESCENDING, section_a, section_b
    ```
     ![Section Similarity Matrix: Top 25](/media/pkg-sec-sim.png)

3. For each similarity query export the result table to a CSV in a known file path. All of the result tables have been pre-populated and are contained in this repo (```/data/sec-sim/```).

4. Ensure that Python 3.8.2 is installed on your local machine. If not, you can download it here:

    https://www.python.org/downloads/release/python-382/

5. Ensure that the required libraries are installed on your local machine with the correct versions.
    ```
    pip install numpy==1.21.4
    pip install pandas==1.2.4
    pip install matplotlib==3.5.1
    pip install seaborn==0.11.2
    ```
6. Locate and open the NIAID DIR Section Similarity Notebook contained in this repo (```/notebooks/niaid-dir-sec-sim.ipynb```).

7. Specify the path of the query result tables on your local machine with the code block found in the **Data** section of the notebook (near the top).
    ```
    data_path = '../data/sec-sim/'
    ```

8. Run all code blocks. The **Post-Process** block should return of the following upon successful completion.

    ```
    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 12880 entries, 0 to 12867
    Data columns (total 10 columns):
    #   Column                   Non-Null Count  Dtype  
    ---  ------                   --------------  -----  
    0   Section A                12880 non-null  object 
    1   Section B                12880 non-null  object 
    2   Journal Category         12880 non-null  float64
    3   Journal Title            12880 non-null  float64
    4   Keyword                  12880 non-null  float64
    5   MeSH                     12880 non-null  float64
    6   Paper                    12880 non-null  float64
    7   Project Category         12880 non-null  float64
    8   Project Term             12880 non-null  float64
    9   Normal Inverse Distance  12880 non-null  float64
    dtypes: float64(8), object(2)
    memory usage: 1.1+ MB
    ```
    
    The **Plot Subset** block should return of the following upon successful completion.

    ![Section Similarity Matrix: Top 25](/media/sec-sim-mtx-top.png)

    At this time, the NIAID DIR section similarity data concatentations, calculations, and visualizations are complete to be later utilized as presentation content.

<br>

## References
National Institute of Allergy and Infectious Diseases. (Nov. 2021). Division of Intramural Research Laboratory Descriptions. https://www.niaid.nih.gov/research/division-intramural-research-labs. [Accessed: Jan. 2022]

University of Texas at Austin, Domain Informational Vocabulary Extraction (DIVE). (2020). PubMed Knowledge Graph Datasets, PKG2020S4 (1781-Dec. 2020), Version 4. http://er.tacc.utexas.edu/datasets/ped. [Accessed: Feb. 2022]

Xu, J., Kim, S., Song, M., Jeong, M., Kim, D., Kang, J., Rousseau, J. F., Li, X., Xu, W., Torvik, V. I., Bu, Y., Chen, C., Ebeid, I. A., Li, D., & Ding, Y. (2020). Building a PubMed Knowledge Graph. Scientific Data, 7(1), [205]. https://doi.org/10.1038/s41597-020-0543-2. [Accessed: Feb. 2022]