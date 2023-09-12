

## Workflow:
- August_2_2023: Have run update_trove_id.py on all sheetsgenerated prior to migration, and after 23 June 2022 (208 sheets). These are located in ```/Users/fiannualamorgan/Documents/2023/TBC_Data_Entry/done/processed_files``` 
- August_8_2023: Have completed the update_trove_id.py code, just need to implement functionality to load in entire folder and will run overnight. Should take approx 15 hours to process. 

## Processed and Cleaned Data
- sheets generated after June 2022 located in: ```/Users/fiannualamorgan/Documents/2023/TBC_Data_Entry/data_cleaning_done_August_4/processed_files_output```
* There are 308 sheets in this folder 
- Need to check:
- ```/Users/fiannualamorgan/Documents/2023/TBC_Data_Entry/data_cleaning/done_August_4/processed_files_output/files_to_check```
- Need to check ```/Users/fiannualamorgan/Documents/2023/TBC_Data_Entry/data_cleaning/done_August_4/processed_files_output/files_to_upload_step_1/Processed_API```
- Cleaned files have been given to Galen.

## Notes:
- At the time of the download of Cloudstor, a number of sheets were still included in the working folder. We will have to ensure these are processed.
- Go through documents in ```'column_not_found.txt'``` and make list of sheets that need to be processed still
- 3 August I have proccessed 308 sheets (those generated since June 2022), still need to process 160 sheets for dates preceeding June 2022 (weird file formats)
- need to write code to compose list of sheets that did not update to a new trove_id (from 4 August)
- the output is currently saved in ```/Users/fiannualamorgan/Documents/2023/TBC_Data_Entry/done/processed_files/processed_files```
- make sure to reprocess '192_filtered_results_chapters_only_96_ELIZ_UPDATED_MAPPING.csv' REMOVED FROM 
- Tasks:
**for Monday 7 August**
1. Run ```'clean_and_check_data.py'``` on ```/Users/fiannualamorgan/Documents/2023/TBC_Data_Entry/done_August_4/processed_files/to_reprocess/Updated_Mappings_to_Reprocess```. Move results back into ```'/Users/fiannualamorgan/Documents/2023/TBC_Data_Entry/done_August_4/processed_files_output'```. Should be 308 files (doubled). 
- Need to move file 'sheet_to_check' files in 'done_August_4' folder, into new folder. Then process the 'sheet_to_upload' files through ```'check_title_id_query_API.py'``` 
**Tuesday 15 August**


**August 22**
Have given **Aug_15_reprocessed_updated_data.json** to Galen.


