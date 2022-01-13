## libraries
from selenium.webdriver import FirefoxProfile
from selenium.webdriver import FirefoxOptions


## make webdriver options
def driver_options(opt):

    """
    Desc:
        Specifies Selenium WebDriver options for Firefox.

    Args:
        opt (list): Option string value flags (e.g. "--headless").

    Returns:
        FirefoxOptions: Selenium WebDriver options object for Firefox.

    Raises:
        TypeError: Incorrect data type in argument.
    """

    ## arg quality
    if type(opt) is not list:
        raise TypeError('opt arg requires list of str.')
    
    else:
        pass

    ## firefox options
    options = FirefoxOptions()

    for i in opt:
        options.add_argument(
            argument = i
        )

    return options


## make webdriver profile
def driver_profile():

    """
    Desc:
        Creates Selenium WebDriver profile for Firefox.

    Args:
        None.

    Returns:
        FirefoxProfile: Selenium WebDriver profile object for Firefox.
    
    Raises:
        None.
    """

    ## firefox profile
    profile = FirefoxProfile()

    profile.set_preference(
        key = 'browser.startup.homepage',
        value = 'about.blank'
    )

    return profile

