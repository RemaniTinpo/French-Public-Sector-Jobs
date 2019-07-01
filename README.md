# French-Public-Sector-Jobs
Scraper on the French state jobs offers website: https://www.place-emploi-public.gouv.fr/

## Starter
- First Git clone this repository

#### With Docker
- At the root of the folder launch: docker build . -t <name_of_your_choice>
- Then: docker run -v /path/on/your/computer/:/opt/program/data <name_of_your_choice>
- When it will be done you will find a .csv file here: /path/on/your/computer/

#### Without docker
- Go into the root folder
- Run python main.py
- When it will be done you will find a .csv file within the data folder

## Parameters file
Within the src/ folder you will find a parameters.yaml file, it contains the following settings:
- url: main url
- api_path: url of the api
- parser_parameters:
  - column_name : //Xpath//
- time_sleep: time between two offsets
- max_offset: maximum number of offsets your program will crawl through (205 shall be enough) when the program fails 10 times he will shut down because it means you rich the end of the listing
- columns_need_correction:
    - name of column
- corrections:
  - 'correction' will be replace by a ''

## Tips
- Do not decrease time_sleep to much :)
- If the scraper is inoperative, have a look to the website and be sure the Xpath didn't change. In case, change the setup in the .yaml file
