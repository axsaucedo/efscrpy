
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# # Driver settings
# DRIVER IS FOR MAC, CHANGE IF YOU NEED OTHER OS
CURR_DIR = os.getcwd()
DRIVER_LOCATION = os.path.join(CURR_DIR, "chromedriver")

# Change this depending on your internet speed
WAITING_TIME = 5

# EF Credentials
USERNAME = "a@e-x.io"
PASSWORD = "eM[#MMQm9BXYF4k.zMMc"

# # Programme global variables
efsite = "https://programme.joinef.com/#/cohort/d5622818-30c7-4b6b-90d2-cc276a5fb9f1/members?"

# check if file exists otherwise download.
if not os.path.exists(DRIVER_LOCATION):
	print ("Chrome driver not found, please download it and put it in base folder")

driver = webdriver.Chrome(DRIVER_LOCATION)

# Open website
driver.get(efsite)

##################
# Performing login
##################

# Waiting until page loads
username_input = WebDriverWait(driver, WAITING_TIME).until(
        EC.presence_of_element_located((By.ID, "a0-signin_easy_email"))
    )
# Getting elements 
username_input = driver.find_element_by_id("a0-signin_easy_email")
passowrd_input = driver.find_element_by_id("a0-signin_easy_password")
login_button = driver.find_elements_by_class_name("a0-next")

# Entering details
username_input.send_keys(USERNAME)
passowrd_input.send_keys(PASSWORD)
login_button[0].click()


##################
# Getting all people
##################

# Waiting until page loads
WebDriverWait(driver, WAITING_TIME).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="cohort-member-view-incomplete-profile-a6a6d532-38ed-4b2d-9888-94f07badc772"]'))
)

# Variable will hold person's details

honey_badgers = []


num_hbs = len(driver.find_elements_by_class_name("cohort-members-grid-item"))

for idx in range(num_hbs):
	print("Number", idx, "out of", num_hbs)

	# Need to refresh items as we do a full page refresh
	honey_badger_items = driver.find_elements_by_class_name("cohort-members-grid-item")
	honey_badger_item = honey_badger_items[idx]

	profile_btn = honey_badger_item.find_elements_by_class_name("profile-button")
	profile_btn[0].click()

	# Wait until profile loads
	try:
		honey_badger_button = WebDriverWait(driver, WAITING_TIME).until(
		    EC.element_to_be_clickable((By.ID, "cohort-member-favourite-profile"))
		)
	except:
		# Check if this is not my own profile...
		# If it, just keep going
		try:
			my_own = driver.find_element_by_id("cohort-member-edit-profile")
		except:
			# Nope, it's just not working
			raise("Something wrong")
		else:
			# All good, it was just your own profile
			# So we just skip this one...
			driver.execute_script("window.history.go(-1)")
			honey_badger_items = WebDriverWait(driver, WAITING_TIME).until(
			    EC.element_to_be_clickable((By.XPATH, '//*[@id="cohort-member-view-incomplete-profile-a6a6d532-38ed-4b2d-9888-94f07badc772"]'))
			)
			continue


	# Collect data
	full_name = driver.find_element_by_xpath('//*[@id="cohort-member-page"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/h5')
	edge_elm = driver.find_element_by_xpath('//*[@id="cohort-member-page"]/div[2]/div/div[2]/div[2]/div[1]/div[2]/h5')
	email_elm = driver.find_element_by_xpath('//*[@id="cohort-member-page"]/div[2]/div/div[2]/div[2]/div[2]/div/h5')
	skills_elms = driver.find_elements_by_class_name("label")
	question_elms = driver.find_elements_by_class_name("answer")
	
	honey_badger = {
		"first_name": full_name.text.split()[0],
		"last_name": " ".join(full_name.text.split()[1:]),
		"email": email_elm.text,
		"skills": [l.text for l in sorted(skills_elms, key=str.lower)],
		"questions": [q.text for q in question_elms]
	}
	honey_badgers.append(honey_badger)

	# Return to previous window
	driver.execute_script("window.history.go(-1)")

	# Wait until previous menu loads
	honey_badger_items = WebDriverWait(driver, WAITING_TIME).until(
	    EC.element_to_be_clickable((By.XPATH, '//*[@id="cohort-member-view-incomplete-profile-a6a6d532-38ed-4b2d-9888-94f07badc772"]'))
	)

driver.quit()

##################
# Save into CSV
##################
print("writing to file")
with open('honey_badgers.csv', 'w', newline='') as fp:
    a = csv.writer(fp, delimiter='\t') # we need tab delimiter as skills have commas
    
    rows = []
    
    header_row = [
    		"first_name",
    		"last_name",
    		"email",
    		"skills",
    		"q1",
    		"q2",
    		"q3",
    		"q4"
    	]

    for hb in honey_badgers:
    	
    	values = [
    		hb["first_name"],
    		hb["last_name"],
    		hb["email"],
    		", ".join(hb["skills"]),
    	]
    	
    	if len(hb["questions"]):
    		for q in hb["questions"]:
    			values.append(q)

    	rows.append(values)

    a.writerows(data)







