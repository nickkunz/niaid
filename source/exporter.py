## libraries
from selenium import webdriver
from driver import driver_options
from driver import driver_profile
from scrapper import data_scrapper
from scrapper import data_cleaner


## -- local machine input -- ##
exe_path = '/usr/local/bin/geckodriver'
csv_path = '/usr/local/niaid-dir-org.csv'

## webdriver settings
option_flags = [
    '--headless',
    '--no-sandbox',
    '--start-maximized',
    '--ignore-certificate-errors',
    '--disable-extensions'
]

options = driver_options(
    opt = option_flags
)

profile = driver_profile()

## webdriver initalization
driver = webdriver.Firefox(
    executable_path = exe_path,
    firefox_profile = profile,
    options = options
)

## data features *strictly* named and ordered
feats = tuple((
    'Name',
    'Education',
    'Branch',
    'Section'
    )
)

## web scraping and processing
data = data_scrapper(
    feats = feats,
    driver = driver,
    url = 'https://www.niaid.nih.gov/research/division-intramural-research-labs',
    t = 12
)

## data processing
data = data_cleaner(
    data = data,
    feats = feats
)

## data to disk
data.to_csv(
    path_or_buf = csv_path,
    index = False
)

