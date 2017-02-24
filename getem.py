
import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# # Programme global variables
efsite = "https://programme.joinef.com/#/cohort/d5622818-30c7-4b6b-90d2-cc276a5fb9f1/members?"
MIN_BADGERS = 70

def __wait_until_cohort_main_screen_loaded(driver):
	"""
		Helper function to wait until all profile containers load
		in the main screen. This function is passed to the
		expected_conditions (EC) waiting method
	"""

	thumbs = driver.find_elements_by_class_name("bookmark-button")
	if len(thumbs) > MIN_BADGERS:
		return True

	return False

def __close(driver):
	driver.close()

def __setup(chrome_driver):

	driver = None

	if chrome_driver:
		# CHOOSE DESIRED DRIVER - CHROME, PHANTOMJS ETC
		if not os.path.exists(chrome_driver):
			print ("Chrome driver not found, please download it and put it in base folder")
			exit(1)
		driver = webdriver.Chrome(chrome_driver)

	else:
		driver = webdriver.PhantomJS() # or add to your PATH
		driver.set_window_size(1024, 768) # optional

	# Open website
	driver.get(efsite)

	return driver

def __do_login(driver, username, password, waiting_time):
	# Waiting until page loads
	username_input = WebDriverWait(driver, waiting_time).until(
	        EC.presence_of_element_located((By.ID, "a0-signin_easy_email"))
	    )
	# Getting elements
	username_input = driver.find_element_by_id("a0-signin_easy_email")
	passowrd_input = driver.find_element_by_id("a0-signin_easy_password")
	login_button = driver.find_elements_by_class_name("a0-next")

	# Entering details
	username_input.send_keys(username)
	passowrd_input.send_keys(password)
	login_button[0].click()

	# Waiting until page loads
	WebDriverWait(driver, waiting_time).until(__wait_until_cohort_main_screen_loaded)
	# Quickfix to wait until all elements are rendered
	# TODO: Replace sleep with proper check
	time.sleep(5)


def __get_hbs(driver, waiting_time):

	# Variable will hold person's details
	honey_badgers = []

	# We only want the people with thumbnails
	num_hbs = len(driver.find_elements_by_class_name("thumbnail"))

	for idx in range(num_hbs):

		# Need to refresh items as we do a full page refresh
		honey_badger_items = driver.find_elements_by_class_name("cohort-members-grid-item")
		honey_badger_item = honey_badger_items[idx]

		profile_btn = honey_badger_item.find_elements_by_class_name("profile-button")
		profile_btn[0].click()

		# Wait until profile loads
		try:
			WebDriverWait(driver, waiting_time).until(
			    EC.element_to_be_clickable((By.ID, "cohort-member-favourite-profile"))
			)
		except:
			# Check if this is not my own profile...
			# If it, just keep going
			try:
				driver.find_element_by_id("cohort-member-edit-profile")
			except Exception as exc:
				# Nope, it's just not working
				raise(exc)
			else:
				# All good, it was just your own profile
				# So we just skip this one...
				print("Skipping your profile...")
				driver.execute_script("window.history.go(-1)")
				honey_badger_items = WebDriverWait(driver, waiting_time).until(
				    EC.element_to_be_clickable((By.XPATH, '//*[@id="cohort-member-view-incomplete-profile-a6a6d532-38ed-4b2d-9888-94f07badc772"]'))
				)
				continue


		# Collect data
		full_name = driver.find_element_by_xpath('//*[@id="cohort-member-page"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/h5')
		edge_elm = driver.find_element_by_xpath('//*[@id="cohort-member-page"]/div[2]/div/div[2]/div[2]/div[1]/div[2]/h5')
		email_elm = driver.find_element_by_xpath('//*[@id="cohort-member-page"]/div[2]/div/div[2]/div[2]/div[2]/div/h5')
		type_elm = driver.find_element_by_xpath('//*[@id="cohort-member-page"]/div[2]/div/div[2]/div[2]/div[1]/div[2]/h5')
		skills_elms = driver.find_elements_by_class_name("label")
		question_elms = driver.find_elements_by_class_name("answer")
		img_elem = None

		try:
			img_elem = driver.find_element_by_xpath('//*[@id="cohort-member-page"]/div[2]/div/div[2]/div[1]/div/div/img')
		except:
			# User has not updated profile
			pass

		honey_badger = {
			"first_name": full_name.text.split()[0],
			"last_name": " ".join(full_name.text.split()[1:]),
			"email": email_elm.text,
			"picture": img_elem.get_attribute("src") if img_elem else "",
			"edge": edge_elm.text.split()[0],
			"type": type_elm.text,
			"skills": sorted([l.text for l in skills_elms], key=str.lower),
			"questions": [q.text for q in question_elms]
		}
		honey_badgers.append(honey_badger)

		print("Done", idx+1, "out of", num_hbs, ":", honey_badger["first_name"], honey_badger["last_name"])

		# Return to previous window
		driver.execute_script("window.history.go(-1)")

		# Wait until previous menu loads
		honey_badger_items = WebDriverWait(driver, waiting_time).until(__wait_until_cohort_main_screen_loaded)

	return honey_badgers



def __save_to_csv(honey_badgers):

	print("Saving to honey_badgers.csv.")

	with open('honey_badgers.csv', 'w', newline='') as fp:

	    a = csv.writer(fp, delimiter=',') # we need tab delimiter as skills have commas

	    rows = []

	    for hb in honey_badgers:

	    	values = [
	    		hb["first_name"],
	    		hb["last_name"],
	    		hb["email"],
	    		hb["picture"],
	    		hb["edge"],
	    		"|".join(hb["skills"]),
	    	]

	    	if len(hb["questions"]):
	    		for q in hb["questions"]:
	    			# Quickfix to change for ’ into '
	    			values.append(q.replace("’", "'"))

	    	rows.append(values)

	    # Sort all rows alphabetically by email to ensure that everything always stays in order
	    rows.sort(key=lambda x: x[2].lower())

	    header_row = [
	    		"First name",
	    		"Last name",
	    		"Email",
	    		"Picture",
	    		"Edge",
	    		"Skills",
	    		"Q1",
	    		"Q2",
	    		"Q3",
	    		"Q4"
	    	]

	    rows.insert(0, header_row)

	    a.writerows(rows)

def main(args):
	driver = __setup(args.chrome)
	__do_login(driver, args.username, args.password, args.waiting)
	hbs = __get_hbs(driver, args.waiting)
	__save_to_csv(hbs)
	__close(driver)






