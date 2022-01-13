## librariers
import pandas as pd
from tqdm import tqdm
from extractor import link_clicker
from extractor import name_section_extractor
from extractor import name_section_processor
from extractor import name_educat_processor
from extractor import branch_extractor
from extractor import section_processor
from namer import name_processor


## web scaper
def data_scraper(feats, driver, url, anch_a = 354, anch_b = 374, n = 3, t = 30):

    """
    Desc:
        Primary web scraping function. Unifies all subordinate functions to 
        traverses website through anchor ID's and pre-process the data returned 
        in a DataFrame.

    Args:
        feats (tuple): Columns as string values.
        driver (obj): Selenium WebDriver object.
        url (str): URL of website.
        anch_a (int): Anchor ID at start of website traversal.
        anch_b (int): Anchor ID at end of website traversal.
        n (int): Number of web request attempts after first failure.
        t (int): Load latency of website (seconds).

    Returns:
        DataFrame: 'Name', 'Education', 'Branch', 'Section' features.
    
    Raises:
        TypeError: Incorrect data type in an argument.
    """

    ## arg quality
    if type(feats) is not tuple:
        raise TypeError('feats arg requires tuple of str.')
    
    if driver is None:
        raise TypeError('driver arg requires Selenium WebDriver object.')
    
    if type(url) is not str:
        raise TypeError('url arg requires a valid str.')
    
    if type(anch_a) is not int:
        raise TypeError('url arg requires a pos int within anchor ID range.')

    if type(anch_b) is not int:
        raise TypeError('url arg requires a pos int within anchor ID range.')
    
    if type(n) is not int or t < 1:
        raise TypeError('n arg requires a pos int.')
    
    if type(t) is not int or t < 1:
        raise TypeError('t arg requires a pos int.')
    
    else:
        pass

    ## make dataframe
    feats = list(feats)
    data = pd.DataFrame(
        columns = feats
    )

    ## traverse lab desc
    for i in tqdm(range(anch_a, anch_b), 
        ascii = True, 
        desc = "Scraping Data from NIAID DIR Laboratory Descriptions"
        ):

        ## link nav
        link_clicker(
            url = url,
            driver = driver,
            anch_x =  'anch_{x}'.format(x = i),
            n = n,
            t = t
        )

        ## -- name, edu, section -- ##
        ## name and section raw extraction
        data_list = name_section_extractor(
            driver = driver,
            anch_a = '//*[@class="block block-layout-builder block-field-blocknodedivisionfield-subtopic-division"]',
            anch_b = '//*[@class="clearfix text-formatted field field--name-field-body field--type-text-long field--label-hidden field__item"]',
            anch_c = '//h1',
            anch_d = '//*[@id="anch_346"]',
            n = n,
            t = t
        )

        ## name and section feat processing
        data_loop = name_section_processor(
            data = data_list,
            feat_a = feats[0],
            feat_b = feats[3]
        )

        ## education feat processing
        data_loop = name_educat_processor(
            data = data_loop,
            feat_a = feats[0],
            feat_b = feats[1]
        )

        ## -- branch and section -- ##
        # branch raw extraction
        data_loop = branch_extractor(
            driver = driver,
            data = data_loop,
            feat_a = feats[3],
            feat_b = feats[2],
            anch_c = '//h1',
            t = t
        )

        ## -- global -- ##
        ## create data
        data = data.append(
            other = data_loop,
            ignore_index = True
        )

    ## name feat processing
    data = name_processor(
        data = data,
        feat = feats[0],
        reap = 2
    )

    ## branch and section processing
    data = section_processor(
        data = data,
        feat_a = feats[3],
        feat_b = feats[2]
    )

    return data


## data wrangling
def data_cleaner(data, feats):

    """
    Desc:
        Utilized for global data cleaning results from web scraping and data
        manipulation. Removes whitespace, sorts, and resets index in DataFrame.
    
    Args:
        data (df): A valid DataFrame.
        feats (list): List of column names as string values.

    Returns:
        DataFrame: Cleaned and sorted assumed for export to disk.
    
    Raises:
        None.
    """

    ## remove whitespace
    for i in data.columns:
        data[i] = data[i].str.strip()

    data.replace(
        to_replace = {' +':' '},
        regex = True,
        inplace = True
    )

    ## arbitrary sorting
    data.sort_values(
        by = [feats[2], feats[0]],
        inplace = True
    )

    ## reset index
    data.reset_index(
        drop = True,
        inplace = True
    )

    return data

