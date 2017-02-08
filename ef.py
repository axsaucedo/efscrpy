
import urllib.request
import os
import zipfile
from selenium import webdriver

# # Driver settings
# DRIVER IS FOR MAC, CHANGE IF YOU NEED OTHER OS
DRIVER_DL_URL = "https://chromedriver.storage.googleapis.com/2.27/"
DRIVER_DL_NAME = "chromedriver_mac64"
DRIVER_FOLDER = "chromedriver_extracted/"
DRIVER_NAME = "chromedriver"
CURR_DIR = os.getcwd()

# # Programme global variables
efsite = "https://programme.joinef.com/#/cohort/d5622818-30c7-4b6b-90d2-cc276a5fb9f1/members?"


# check if file exists otherwise download.
print(os.path.join(CURR_DIR, DRIVER_FOLDER))
if not os.path.exists(os.path.join(CURR_DIR, DRIVER_FOLDER)):
	
	print ("Chrome driver not found")

	if not os.path.exists(os.path.join(CURR_DIR, DRIVER_DL_NAME + ".zip")):
		print("Downloading chrome driver zip file")
		# Download web driver 
		urllib.request.urlretrieve(DRIVER_DL_URL + DRIVER_DL_NAME + ".zip", DRIVER_DL_NAME + ".zip")
		print("file downloaded")
	else:
		print("Zip file found")

	print("Extracting file")
	zip_ref = zipfile.ZipFile(os.path.join(CURR_DIR, DRIVER_DL_NAME + ".zip"), 'r')
	zip_ref.extractall(os.path.join(CURR_DIR, DRIVER_FOLDER))
	zip_ref.close()

else:
	print("Chrome driver found")

print(os.path.join(DRIVER_FOLDER, DRIVER_NAME))
print(os.path.join(CURR_DIR, os.path.join(DRIVER_FOLDER, DRIVER_NAME)))
driver = webdriver.Chrome(os.path.join(CURR_DIR, os.path.join(DRIVER_FOLDER, DRIVER_NAME)))

driver.get(efsite)










