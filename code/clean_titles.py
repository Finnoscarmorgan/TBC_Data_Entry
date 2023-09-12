"""
This program takes in an Excel file and extracts Roman Numerals from the 'Title' column and puts them in a new column titled 'chapter number'. 
This program also extracts  the Chapter Title from the 'Title' column and puts them in a new column titled 'chapter title'. 
"""

import pandas as pd
import re
import numpy as np
import os
import sys
import openpyxl
from fuzzywuzzy import fuzz

def identify_roman_numeral(title):
    """
    This function takes in a string and returns the Roman Numeral in the string.
    """
    #add error handling if nan is passed in 
    if type(title) == float:
        return np.nan
    else:
        # Roman Numerals
        roman_numeral = re.findall(r'\b[MDCLXVI]+\b', title)
        if roman_numeral == []:
            roman_numeral = np.nan
        else:
            roman_numeral = roman_numeral[0]
    return roman_numeral

def identify_continued(title):
    """
    This function checks to see if the title contains a word similar to 'continued' with a Levenshtein distance of 2.
    If it does, the string ' (continued)' is added to the end of the string in the 'chapter number' column.
    """
    if pd.isnull(title):
        return np.nan
    
    # Check for 'continued' or similar words
    word_list = re.findall(r'\b\w+\b', title)  # Extract individual words from the title
    for word in word_list:
        if fuzz.ratio(word.lower(), 'continued') >= 80:  # Adjust the threshold as needed
            # Add ' (Continued)' to the end of the string in the 'chapter number' column
            return ' (Continued)'
    return ''  # Return an empty string if 'continued' is not found


def identify_chapter_title(title):
#This function takes in a string and returns the string that comes after the Roman Numeral in the string except for the word 'continued'.

    if pd.isnull(title):
        return ''

    # Roman Numerals
    roman_numeral = re.findall(r'\b[MDCLXVI]+\b', title)
    if roman_numeral == []:
        return ''
    else:
        roman_numeral = roman_numeral[0]

    #Create a condition to handle instances where there is 'CHAPTER I' OR 'chapter I' in the title column and retrieve all text after it
    if re.search(r'chapter\sI(\s|\.)', title, re.IGNORECASE):
        chapter_title = title.split('CHAPTER I')[-1].strip()
        #conduct regex match of chapter title to see if it is 'continued'
        if re.match(r'continued', chapter_title.lower(), re.IGNORECASE):
            return ''
        else:
            return chapter_title

    # Chapter Title
    chapter_title = title.split(roman_numeral)[-1].strip()
    #conduct regex match of chapter title to see if it is 'continued'
    if re.match(r'continued', chapter_title.lower(), re.IGNORECASE):
        return ''

    return chapter_title







def clean_chapter_title(title):
    #remove all non-ascci characters from string 
    title = title.encode("ascii", errors="ignore").decode()
    #remove all instances of 'continued' from string as well as any leading or trailing whitespace as regex
    title = re.sub(r'continued', '', title, flags=re.IGNORECASE).strip()
    #remove all instances where there is a '. (.)' in the string or ' . ' in the string 
    title = re.sub(r'\.\s\(\.\)', '', title)
    title = re.sub(r'\.\s', '', title)
    #remove all instances of '()' from string
    title = re.sub(r'\(\)', '', title)
    #remove all instances of '(.)' or ' (.)' from string eetc.
    title = re.sub(r'\s\(\.\)', '', title)
    title = re.sub(r'\(\.\)', '', title)
    title = re.sub(r'\(\.\s', '', title)
    #remove all instances where '.' is at the beginning of the string with trailing whitespace 
    title = re.sub(r'^\.\s', '', title)
    #remove all '.' from string
    title = re.sub(r'\.', '', title)

    

    return title



def main():
    #read in the excel file
    file = 'FILE NAME HERE'
    df = pd.read_excel(file, sheet_name='Sheet1')
    
    #read in string from title column and apply identify_roman_numeral function to it and work through entire column 
    df['chapter number'] = df['title'].apply(identify_roman_numeral)
    #read in string from title title column and apply identify_continued function to it, if True, add ' (Continued)' to end of chapter number column
    df['chapter number'] = df['chapter number'].astype(str) + df['title'].apply(identify_continued).replace(np.nan, '')

    #read in string from title column and apply identify_chapter_title function to it and work through entire column
    df['chapter title'] = df['title'].apply(identify_chapter_title)

    #read in string from chapter title column and apply clean_chapter_title function to it and work through entire column
    df['chapter title'] = df['chapter title'].apply(clean_chapter_title)

    #write to new excel file
    df.to_excel('FILE NAME HERE_CLEANED.xlsx', index=False)

    




if __name__ == "__main__":
    main()
