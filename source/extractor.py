## libraries
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


## navigation by link anchors
def link_clicker(driver, url, anch_x, n, t):

    """ 
    Desc:
        Navigates to link in website specified by anchor ID in 'anch_x'. Makes 
        'n' number of web request attempts before time out failure with 't' load 
        latency time. 

    Args:
        url (str): URL of website.
        driver (obj): Selenium WebDriver object.
        anch_x (int): Anchor ID of link.
        n (int): Number of web request attempts after first failure.
        t (int): Load latency of website (seconds).
    
    Returns:
        None
    
    Raises:
        RuntimeError: Max 'n' number of attempts reached.
    """

    ## get request url
    driver.get(
        url = url
    )

    ## load latency
    wait = WebDriverWait(
        driver = driver,
        timeout = t
    )

    ## try n times
    i = 1

    ## nav to link
    while i < n:
        try:
            branch = wait.until(
                method = EC.element_to_be_clickable(
                    locator = (By.ID, anch_x)
                )
            )
            branch.click()
            break

        ## try again on failure
        except:
            i += 1
            print('Unsuccessful request, trying again. Attempt: {x}'.format(
                    x = i
                )
            )

            ## get request url again
            driver.get(
                url = url
            )
            pass

        ## time out failure on too many attempts
        if n == i:
            raise RuntimeError(
                'Unsuccessful request, now stopping. Max number of attempts.'
            )


## name and section data
def name_section_extractor(driver, anch_a, anch_b, anch_c, anch_d, n, t):

    """
    Desc:
        Primary function for retrieving raw data for 'Name', 'Education', and 
        'Section' features. Makes 'n' number of web request attempts before 
        time out failure with 't' load latency time. Anchor ID's 'anch_a', 
        'anch_b', 'anch_c', 'anch_d' pre-specified from known information 
        based on prior website inspection.

    Args:
        driver (obj): Selenium WebDriver object.
        anch_a (str): Anchor ID of link.
        anch_b (str): Anchor ID of link.
        anch_c (str): Anchor ID of link.
        anch_d (str): Anchor ID of link.
        n (int): Number of web request attempts after first failure.
        t (int): Load latency of website (seconds).

    Returns:
        list: List of lists containing strings of names and lab desc.

    Raises:
        ValueError: Cannot split strings.
        RuntimeError: Max 'n' number of attempts reached. 
    """

    ## load latency
    wait = WebDriverWait(
        driver = driver,
        timeout = t
    )

    ## try n times
    i = 1

    ## nav to link
    while i < n:
        try:

            ## -- multiple researcher profiles -- ##
            ## contains branch and section/unit columns
            try:

                ## global web elements
                element_all = wait.until(
                    method = EC.presence_of_element_located(
                        locator = (By.XPATH, anch_a)
                    )
                )

                ## global list
                element_all_lst = element_all.find_elements_by_tag_name(
                    name = "li"
                )

                people_all = list()

                for i in element_all_lst:
                    people_all.append(i.text)

                ## global list to contain only names, edu, section/unit
                people_all = [i for i in people_all if "\n" in i]

                ## subset web elements
                element_sub = wait.until(
                    method = EC.presence_of_element_located(
                        locator = (By.XPATH, anch_b)
                    )
                )

                ## subset web element list
                element_sub_lst = element_sub.find_elements_by_tag_name(
                    name = "li"
                )

                people_sub = list()

                for i in element_sub_lst:
                    people_sub.append(i.text)

                ## subset web element list to contain only names, edu, section/unit
                people_sub = [i for i in people_sub if "\n" in i]

                ## section/unit list
                n = len(people_sub)
                people_sec = people_all[n:]

                people_sec_spt = list()
                n = len(people_sec)

                for i in range(0, n):
                    try:
                        people_sec_spt.append(
                            [people_sec[i].split('\n')[1], people_sec[i].split('\n')[0]]
                        )

                    except ValueError as err:
                        print(err.args, 'Cannot split strings in Sections and Units element.')

                ## branch list
                people_sub_spt = list()
                n = len(people_sub)

                for i in range(0, n):
                    try:
                        people_sub_spt.append(
                            people_sub[i].split('\n')
                        )
                    except ValueError as err:
                        print(err.args, 'Cannot split strings in People element.')

                ## combined branch and section/unit list
                people_all_spt = people_sec_spt + people_sub_spt

                ## remove duplicates
                for i in people_all_spt:
                    n = len(i)
                    if n > 2:
                        people_all_spt.remove(i)

            ## -- single researcher profile -- ##
            ## does not contain branch and section/unit columns
            except:

                ## name, edu, section/unit
                people_all_spt = list()
                string_all_spt = list()

                ## name, section/unit text
                anchors = [
                    anch_c,
                    anch_d
                ]

                n = len(anchors)

                for i in range(0, n):
                    element_all = wait.until(
                        method = EC.presence_of_element_located(
                            locator = (By.XPATH, anchors[i])
                        )
                    )
                    string_all_spt.insert(i, element_all.find_element_by_xpath(
                            xpath = anchors[i]
                        ).text
                    )

                ## store list in list
                people_all_spt.insert(0, string_all_spt)

            finally:
                return people_all_spt

        ## try again on failure
        except:
            i += 1
            print('Unsuccessful request to link, trying again. Attempt: {x}'.format(
                    x = i
                )
            )
            pass

        ## time out failure on too many attempts
        if n == i:
            raise RuntimeError(
                'Unsuccessful request, now stopping. Max number of attempts.'
            )


## name and section pre-processing
def name_section_processor(data, feat_a, feat_b):

    """
    Desc:
        Addresses 'Section' feature. Subordinate function for determining
        duplicate observations by values in 'feat_b' encoded with a special
        character (comma). Removes redundant observations.

    Args:
        data (df): A valid DataFrame.
        feat_a (str): Reference column, typically 'Name'.
        feat_b (str): Modification column, typically 'Section'.
    
    Returns:
        DataFrame: Contains modified 'feat_b' feature.
    
    Raises:
        None.
    """
    
    ## make researcher name and section feats
    feats = [
        feat_a,
        feat_b,
    ]

    data = pd.DataFrame(
        data = data,
        columns = feats
    )

    ## remove multiple section names
    return data[~data[feat_b].str.contains(',')]


## name and education pre-processing
def name_educat_processor(data, feat_a, feat_b):

    """
    Desc:
        Creates new 'Education' feature. Removes job title and family suffix 
        from values in 'feat_a'. Utilizes remaining substring values to move 
        specified education credentials to 'feat_b'. Duplicate values in 
        'feat_a' will occure where there are multiple education credentials.

    Args:
        data (df): A valid DataFrame.
        feat_a (str): Reference column, typically 'Name'.
        feat_b (str): Creation column, typically 'Education'.
        
    Returns:
        DataFrame: Contains new 'feat_b' feature.
    
    Raises:
        None.
    """
    
    ## job title suffix
    titles = [
        'Chief',
        'Director',
        'Diplomate',
        'Senior Investigator',
        'Facility Veterinarian',
        'FRCPA Staff Clinician',
        'FRCPA',
        'Diplomate ACLAM',
        'ACLAM',
        'FAAAAI',
        'Acting',
        'Associate',
        'Staff Clinician'
    ]

    ## punctuation
    puncs = [
        ';',
        ',',
        '.'
    ]

    ## remove job title suffix and punctuation
    remove = titles + puncs

    for i in remove:
        data[feat_a] = data[feat_a].str.replace(
            pat = i,
            repl = '',
            case = True,
            regex = False
        )

    ## remove leading and trailing whitespace
    for i in data.columns:
        data[i] = data[i].str.strip()

    ## edu suffix
    edu = [
        'MA',
        'MSc',
        'MS',
        'MHSc',
        'MHS',
        'MPVM',
        'MPH',
        'MD',
        'ScD',
        'DSc',
        'DVM',
        'DPhil',
        'PhD',
        'Dr rer nat'
    ]

    ## make edu feature
    data.insert(
        loc = 1,
        column = feat_b,
        value = None
    )

    ## move edu from suffix to edu feature
    n = len(data)

    for i in range(0, n):
        for j in edu:
            if j in data[feat_a].iloc[i]:
                data[feat_a].iloc[i] = data[feat_a].iloc[i].replace(j, '')
                data[feat_a].iloc[i] = data[feat_a].iloc[i].replace('  ', ' ')
                if data[feat_b].iloc[i] is None:
                    data[feat_b].iloc[i] = j
                else:
                    data = data.append(data.iloc[i])
                    data[feat_b].iloc[i] = None
                    data[feat_b].iloc[i] = j

    ## assume credentials not listed
    data[feat_b].fillna(
        value = 'Other',
        inplace = True
    )

    ## remove duplicate edu
    for i in edu:
        data[feat_a] = data[feat_a].str.replace(
            pat = i,
            repl = '',
            case = True,
            regex = False
        )

    ## remove parath
    data[feat_a] = data[feat_a].str.replace(
            pat = r"\(.*\)",
            repl = '',
            regex = True
        )

    ## remove leading and trailing whitespace
    for i in data.columns:
        data[i] = data[i].str.strip()

    ## remove duplicate observations
    data.drop_duplicates(
        inplace = True
    )

    return data


## branch data and pre-processing
def branch_extractor(driver, data, feat_a, feat_b, anch_c, t):

    """
    Desc:
        Creates new 'Branch' feature. Utilizies web requests and DataFrame 
        referencing. For multiple researchers per 'feat_b', 'feat_a' will 
        contain different values than 'feat_b'. For one researcher per 'feat_b',
        'feat_a' and 'feat_b' contain the same values.

    Args:
        driver (obj): Selenium WebDriver object.
        data (df): A valid DataFrame.
        feat_a (str): Reference column, typically 'Section'.
        feat_b (str): Target column, typically 'Branch'.
        anch_c (str): Anchor ID of link.
        t (int): Load latency of website (seconds).

    Returns:
        Dataframe: Contains new 'feat_b' feature.
    
    Raises:
        ValueError: Could not locate web resource.
        ValueError: 'Branch' feature could not be created.
    """

    ## load latency
    wait = WebDriverWait(
        driver = driver,
        timeout = t
    )

    ## add feat
    n = len(data)

    ## multiple researchers
    if n > 1:
        try:
            element = wait.until(
                method = EC.presence_of_element_located(
                    locator = (By.XPATH, anch_c)
                )
            )

            feat_branch = element.find_element_by_xpath(
                xpath = anch_c
            ).text

        except ValueError as err:
            print(err.args, 'Cannot find heading.')

    ## single researcher
    elif n == 1:
        feat_branch = data[feat_a].iloc[0]

    else:
        raise ValueError('Could not create branch name feature.')

    data.insert(
        loc = 2,
        column = feat_b,
        value = feat_branch
    )

    return data


## modify section names
def section_processor(data, feat_a, feat_b):

    """
    Desc:
        Addresses 'Section' feature. Modifies string values to observations in 
        'feat_a' by including the corresponding string values found in 'feat_b' 
        if there are duplicate values in 'feat_a', where the values found in 
        'feat_b' are different.

    Args:
        data (df): A valid DataFrame.
        feat_a (str): Target column, typically 'Section'.
        feat_b (str): Reference column, typically 'Branch'.

    Returns:
        Dataframe: Annotated observations in 'feat_a' column.
    
    Raises:
        None.
    """

    ## add parenth for matching sections with different branch
    mix_sec = list()

    for i in data[feat_a].unique():
        if len(data[data[feat_a] == i][feat_b].unique()) > 1:
            mix_sec.append(i)

    for i in mix_sec:
        data_sec = data[data[feat_a] == i].copy()
        n = len(data_sec)
        for j in range(0, n):
            name_sec = (
                data_sec[feat_a].iloc[j] + ' ' + '(' + data_sec[feat_b].iloc[j] + ')'
            )
            data_sec[feat_a].iloc[j] = name_sec

        data.update(
            other = data_sec
        )

    ## reindex data
    data.reset_index(
        drop = True,
        inplace = True
    )

    return data

