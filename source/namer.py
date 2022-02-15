## modify first names
def first_namer(data, feat):

    """
    Desc:
        Addresses 'Name' feature. Performs ad hoc changes to abbreviated or 
        otherwise misspelled first names. This function should evolve when 
        errors in first names are recognized or improved info.
     
    Args:
        data (df): A valid DataFrame.
        feat (str): Target column, typically 'Name'.

    Returns:
        DataFrame: Cleaned first name substring values in 'feat' column.
    
    Raises:
        None.
    """

    ## individual name corrections
    feat_repl = {

        ## slight abuse of original purpose
        ## info: https://ned.nih.gov/search/
        feat: {
            'Beth Fischer': 'Elizabeth Fischer',
            'David Hackstadt': 'Ted Hackstadt'
        }
    }

    data.replace(
        to_replace = feat_repl,
        inplace = True
    )

    return data


## modify middle names
def middle_namer(data, feat):

    """
    Desc:
        Addresses 'Name' feature. Inserts middle initial or name into string
        values that have matching first and last names when compared to other
        observation, but where the middle initial or name is absent.
     
    Args:
        data (df): A valid DataFrame.
        feat (str): Target column, typically 'Name'.

    Returns:
        DataFrame: Cleaned middle name substring values in 'feat' column.
    
    Raises:
        None.
    """

    ## clean names
    n = len(data) - 1

    for i in range(0, n):

        ## use full name containing middle initial
        name_one = str(
            data[feat].iloc[i].split()[0] + ' ' + 
            data[feat].iloc[i].split()[-1]
        )

        name_two = str(
            data[feat].iloc[i + 1].split()[0] + ' ' + 
            data[feat].iloc[i + 1].split()[-1]
        )

        if name_one == name_two:
            n_name_one = len(data[feat].iloc[i].split())
            n_name_two = len(data[feat].iloc[i + 1].split())

            if n_name_one != n_name_two:
                if n_name_one > 2:
                    name_use = data[feat].iloc[i]
                if n_name_two > 2:
                    name_use = data[feat].iloc[i + 1]
                else:
                    pass

                data[feat].iloc[i] = name_use
                data[feat].iloc[i + 1] = name_use

            else:
                pass

        else:
            pass
    
    ## individual name corrections
    feat_repl = {

        ## slight abuse of original purpose
        ## info: https://ned.nih.gov/search/
        feat: {
            'Elizabeth Fischer': 'Elizabeth R Fischer', 
            'David Sacks': 'David L Sacks',
            'Daniella Schwartz': 'Daniella M Schwartz',
            'Richard Davey': 'Richard T Davey',
            'Louis Miller': 'Louis H Miller',
            'Catharine Bosio': 'Catharine M Bosio'
        }
    }

    data.replace(
        to_replace = feat_repl,
        inplace = True
    )

    ## remove duplicates
    data.drop_duplicates(
        inplace = True
    )

    return data


## modify last names
def last_namer(data, feat, reap = 3):

    """
    Desc:
        Addresses 'Name' feature. Modifies last name substring by correcting 
        errors when misspellings are assumed to be missing letters. Replaces 
        assumed misspelling with string value of greater length. Also removes 
        family name suffix.
     
    Args:
        data (df): A valid DataFrame.
        feat (str): Target column, typically 'Name'.
        reap (int): Number of substrings in last name to compare.

    Returns:
        DataFrame: Cleaned last name substring values in 'feat' column.
    
    Raises:
        None.
    """

    ## clean names
    n = len(data) - 1

    for i in range(0, n):

        ## remove suffix from last names
        name_sir = data[feat].iloc[i].split()[-1]
        n_name_sir = len(name_sir)

        ## remove suffix errors
        if n_name_sir == 1:
            data[feat].iloc[i] = data[feat].iloc[i][:-2]

        ## remove family suffix
        if n_name_sir <= 3:
            fam_suf = [
                'III',
                'II',
                'Jr',
                'Sr'
            ]

            for j in fam_suf:
                if name_sir == j:
                    data[feat].iloc[i] = ' '.join(data[feat].iloc[i].split()[:-1])

        else:
            pass

        ## replace missing letters in last names 
        ## assumes same last name for first 'reap' repeated letters
        name_giv_one = data[feat].iloc[i].split()[0]
        name_giv_two = data[feat].iloc[i + 1].split()[0]

        name_sir_one = data[feat].iloc[i].split()[-1]
        name_sir_two = data[feat].iloc[i + 1].split()[-1]

        if name_giv_one == name_giv_two and name_sir_one[0:reap] == name_sir_two[0:reap]:
            n_name_sir_one = len(name_sir_one)
            n_name_sir_two = len(name_sir_two)

            if n_name_sir_one != n_name_sir_two:
                if n_name_sir_one > n_name_sir_two:
                    data[feat].iloc[i + 1] = data[feat].iloc[i]

                if n_name_sir_one < n_name_sir_two:
                    data[feat].iloc[i] = data[feat].iloc[i + 1]

            else:
                pass

        else:
            pass


    ## individual name corrections
    feat_repl = {

        ## slight abuse of original purpose
        ## info: https://ned.nih.gov/search/
        feat: {
            'Jennifer M Cuellar-Rodriguez': 'Jennifer M Cuellar-Rodríguez',
            'Sumati Ragagopalan': 'Sumati Rajagopalan'
        }
    }

    data.replace(
        to_replace = feat_repl,
        inplace = True
    )

    return data


## naming wrapper
def name_processor(data, feat, reap):

    """
    Desc:
        Addresses 'Name' feature. Unifies subordinate naming functions for 
        string and substring values. Utilized for later implementation in
        web scraping procedure.
     
    Args:
        data (df): A valid DataFrame.
        feat (str): Target column, typically 'Name'.
        reap (int): Number of characters to compare in last name substring.

    Returns:
        DataFrame: Cleaned name string values in 'feat' column.
    
    Raises:
        None.
    """

    ## remove whitespace
    data[feat] = data[feat].str.strip()

    data.replace(
        to_replace = {' +':' '},
        regex = True,
        inplace = True
    )

    ## sort data by names
    data.sort_values(
        by = feat,
        ascending = False,
        inplace = True
    )
    
    ## first
    data = first_namer(
        data = data,
        feat = feat
    )

    ## middle
    data = middle_namer(
        data = data,
        feat = feat
    )

    ## last
    data = last_namer(
        data = data,
        feat = feat,
        reap = reap  ## num char to compare
    )

    return data