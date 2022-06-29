"""
Webscraping for CodeChef Present Contest 
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Hold
from selenium.webdriver.support import expected_conditions as EC
import json
import CONSTANTS
import Contest

WEB_DRIVER_PATH = CONSTANTS.WEB_DRIVER_PATH
present_contest = []

driver = webdriver.Chrome(WEB_DRIVER_PATH)
driver.get(CONSTANTS.CodeChefContest)

try:
	print("Waiting for the contest to load...")

	element = Hold(driver, 10).until( EC.presence_of_element_located((By.ID, "present-contests-data")) )
	print("Contest loaded!\t Starting to scrape...")
	print("Ongoing Contests Scraped\n")
	
	# storing the data in a list
	element_list = element.text.split("\n")

	print(element_list)

	# Contest class object to store the data
	contests = Contest.Contest() 

	# looping through the list with increment of 2
	for contest in range(0, len(element_list), 2):
		contest_code = ''
		contest_name = ''
		contest_start_date = ''
		contest_start_time = ''
		contest_end_time = ''
		contest_duration = ''

		# extracting the contest code
		contests_code = element_list[contest].split(" ")[0]
		# print("Contest Code: " + contests_code)

		# extracting the contest name by looping until the last third word (len - 3)
		i = 1
		while i < len(element_list[contest].split(" ")) - 3:
			contest_name += element_list[contest].split(" ")[i] + " "
			i += 1

		contest_name = contest_name.strip()
		# print("Contest Name: " + contest_name)

		# extracting the contest start date
		while i < len(element_list[contest].split(" ")):
			contest_start_date += element_list[contest].split(" ")[i] + " "
			i += 1

		contest += 1

		contest_start_date += element_list[contest].split(" ")[0]
		contest_start_date = contest_start_date.strip()
		# print("Contest Start Date: " + contest_start_date)

		# extracting the contest start time
		contest_start_time = element_list[contest].split(" ")[1]
		contest_start_time = contest_start_time.strip()
		# print("Contest Start Time: " + contest_start_time)

		# extracting the contest duration
		for i in range(0, len(element_list[contest].split("  "))): # splitting the string into two parts based on double spaces
			j = 2
			while j < len(element_list[contest].split("  ")[i].split(" ")):
				contest_duration += element_list[contest].split("  ")[i].split(" ")[j] + " "
				j += 1
		contest_duration = contest_duration.strip()
		# print("Contest Duration: " + contest_duration)

		i = 1
		# extracting the contest end time
		while i < len(element_list[contest].split("  ")): # splitting the string into two parts based on double spaces
			j = 0
			while j < len(element_list[contest].split("  ")[i]):
				contest_end_time += element_list[contest].split("  ")[i][j]
				j += 1
			i += 1
		contest_end_time = contest_end_time.strip()
		# print("Contest End Time: " + contest_end_time)

		# Adding the contest data to the contests object and appending it to the present_contest list
		contests.code = contests_code
		contests.name = contest_name
		contests.startDate = contest_start_date
		contests.startTime = contest_start_time
		contests.endTime = contest_end_time
		contests.duration = contest_duration

		present_contest.append(contests.makeContest())
	
	print("\n\n\n")

	print("Contest Data Scraped!")
	print("\n")

	# Writing the data to a file
	with open("./present_contests.txt", "w") as f:
		for contest in present_contest:
			f.write(str(contest) + "\n")
	print("Contest Data written to file!")
	print("\n")

	# Adding the data to the json file
	json_data = json.loads(str(present_contest).replace("'", '"'))	
	with open('./presentContests.json', 'w') as f:
		json.dump(json_data, f, indent=4, sort_keys=True)

	driver.quit()
	print(str(present_contest))


except Exception as e:
	print("Error: " + str(e))
	driver.quit()
	print("Scraping Failed!")
	exit(1)