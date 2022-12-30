# Web Scraper

## Description

This script scrapes data of differnt spefications of phones from amazon.com

### Video Demo

video link

## Project Structure

- project.py
- phones.csv
- project_test.csv
- requirments.txt
- readme.md
## Libraries

- **selenium:** Selenium is an open-source tool that automates web browsers.
- **csv:** The csv module implements classes to read and write tabular data in CSV format.
- **time:** The Python time module provides many ways of representing time in code, such as objects, numbers, and strings.
- **re:** The re module provides a set of powerful regular expression facilities.
## Functions

#### setup

This function returns a WebDriver object

#### phones

This function itrates over amazon webpage containing phones and open its 
phones on a new webpage then call data_extrator function to extract the 
data on the phone's webpage and closes the phone's webpage and switches 
back to the amazon webpage

#### data_extrator

This function extracts data from the phone's webpage and returns a Tuple of str, and if it dosen't
find the desired data it sets '-' as default value


#### csv_maker

This function takes a Generator object containing dict and converts it into a csv file