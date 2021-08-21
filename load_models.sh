python3 -m venv venv/
source venv/bin/activate
pip install gdown

gdown --id 16iOzmpngF-t7b_wzeU3bxcQ8mB1QpWzD -O model_files/
cd model_files/
unzip models.zip