#!/usr/bin/env python3
# Functionality to check the title_id and title string of a record
# against the readallaboutit.com.au database (api).

import requests
import json
from thefuzz import fuzz
import csv
import pandas as pd
import datetime
import os
import glob

def build_url(title_id: int) -> str:
    """Builds the url to query the api with, given a title_id."""
    return f"https://readallaboutit.com.au/api/v1/title/{title_id}"


def get_title(title_id: int) -> dict:
    """Get a title record from the readallaboutit api given a title_id."""
    url = build_url(title_id)
    retries = 3  # Number of times to retry the request

    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
            print(f"Successfully fetched title_id {title_id}.")
            # print timestamp to console to show progress
            print(datetime.datetime.now().strftime("%H:%M:%S"))
            return json.loads(response.text)
        except requests.ConnectionError as e:
            print(f"Connection error when fetching title_id {title_id}: {e}. Retrying...")
            if attempt == retries - 1:
                print(f"Failed to fetch title_id {title_id} after {retries} retries. Response Code: {e}")
                return None
        except requests.HTTPError as e:
            print(f"Failed to fetch title_id {title_id}. Response Code: {e.response.status_code}")
            return None

def check_title_id_string_pair(title_id: int, title: str) -> bool:
    """
    Request a title record for a given title_id and check that the given title
    string is a perfect match (in either the 'publication_title' or 'common_title').
    """
    title_record = get_title(title_id)
    if title_record:
        if title_record['publication_title'] == title:
            return True
        elif title_record['common_title'] == title:
            return True
        else:
            return False
    else:
        return False


def fuzzy_check_title_id_string_pair(title_id: int, title: str, tolerance=75) -> bool:

    
    title_record = get_title(title_id)
    if title_record:
        print(f"Checking title_id {title_id} with title: {title}")
        title = title.lower()  # Convert to lowercase
        title_len = len(title) # Get length of title
        pub_title_len = len(title_record['publication_title'])
        com_title_len = len(title_record['common_title'])

        # Compare the title with publication_title and common_title based on the length
        if title_len < pub_title_len:
            if fuzz.ratio(title_record['publication_title'][:title_len].lower(), title) >= tolerance:
                return True
            elif fuzz.ratio(title_record['common_title'][:title_len].lower(), title) >= tolerance: #I need to change this so it checks the whole name...
                return True
        elif title_len > pub_title_len:
            if fuzz.ratio(title_record['publication_title'].lower(), title[:pub_title_len]) >= tolerance:
                return True
            elif fuzz.ratio(title_record['common_title'].lower(), title[:com_title_len]) >= tolerance:
                return True
        elif title_len == pub_title_len:
            if fuzz.ratio(title_record['publication_title'].lower(), title) >= tolerance:
                return True
            elif fuzz.ratio(title_record['common_title'].lower(), title) >= tolerance:
                return True
        else:
            print(f"Title record not found for title_id {title_id}.")
        return False
            
    return False

def process_directory(input_dir: str) -> None:
    """
    This function processes all the filesin a given directory and writes the 
    results to a directory titled 'processed_API'
    """

    # Create 'processed_files' folder in the same directory
    output_dir = os.path.join(input_dir, '3_processed_files')
    os.makedirs(output_dir, exist_ok=True)

    # Get list of all CSV files in the directory
    file_list = glob.glob(os.path.join(input_dir, '*.csv'))
    for file_path in file_list:
        # Skip temporary files
        if os.path.basename(file_path).startswith('~$'):
            continue

        # Check if this file has already been processed
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        if os.path.exists(os.path.join(output_dir, f'{base_name}_safe_upload.csv')) and \
           os.path.exists(os.path.join(output_dir, f'{base_name}_not_safe_upload.csv')):
            print(f"{file_path} has already been processed, skipping...")
            continue

        # Print to console to show progress
        print(f"working on {file_path}")
        # Print timestamp to console to show progress
        print(datetime.datetime.now().strftime("%H:%M:%S"))
        #df = pd.read_csv(file_path)

        # Create empty data frames for safe and not safe uploads
        safe_upload = pd.DataFrame()
        not_safe_upload = pd.DataFrame()

        with open(file_path, 'r') as infile:
            reader = csv.DictReader(infile)

            #determine the correct header for 'trove title'
            title_header = None
            for possible_title_header in ['Trove Title', 'trove title', 'Trove_Title', 'trove_title']:
                if possible_title_header in reader.fieldnames:
                    title_header = possible_title_header
                    break

            if title_header is None:
                print(f"Could not find title header in {file_path}")
                continue

            for row in reader:
                title_id = int(float(row['title_id']))  # Convert to float first, then to int
                title = row[title_header]
                if fuzzy_check_title_id_string_pair(title_id, title):
                    safe_upload = safe_upload.append(row, ignore_index=True)
                else:
                    not_safe_upload = not_safe_upload.append(row, ignore_index=True)

        # Create unique names for the output files based on the original file name
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        safe_upload.to_csv(os.path.join(output_dir, f'{base_name}_safe_upload.csv'), index=False)
        not_safe_upload.to_csv(os.path.join(output_dir, f'{base_name}_not_safe_upload.csv'), index=False)

   
def main():
    input_dir = 'FOLDER NAME HERE'
    process_directory(input_dir)


if __name__ == '__main__':
    main()