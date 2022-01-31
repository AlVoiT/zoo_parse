# parse_zooplus
## Describe

    Python3.9 

    Parse https://www.zooplus.de/

# Instruction:
### 1. Download the project:
    git clone https://github.com/AlVoiT/zoo_parse.git

### 2. Set variables in get_zooplus_data.py like:
   - [OPTIONAL] List of columns for CSV headers .

     A container of the allowable values for the argument. (--headers)
     
        
     
address  ,  behandlung ,  brands_txt ,  brand_others_txt ,
breadcrumb ,  count_reviews ,       avg_review_score ,
city ,  city_slug_txt ,  id ,  is_profile_linked ,
keywords ,  lat ,       lng ,  location ,  name ,  open_time ,
paymentmethods_txt ,  parkingoptions_txt ,       profile_image ,
schwerpunkt ,  reviews_nest ,  slug ,  telefon ,
wheelchair_accessible_txt ,       zip ,_last_index_update_date
   - [OPTIONAL] Number of page parse .

     --page
     default = 3


   - [OPTIONAL] Path to CSV file .

        --path
        default = 'DATA.csv'


          

### 3. Create and activate pythonvenv. 
   https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
  
### 4. Install Python packages:
    pip install -r requirements.txt

### 5. Run file app/get_zooplus_data.py
example: 'python get_zooplus_data.py --headers name, city --page 3--path data.csv'