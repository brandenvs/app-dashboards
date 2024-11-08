import time
import gspread

from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.edge.options import Options as EdgeOptions

from google.oauth2 import service_account

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from labSite.settings import CREDS_FILE

from .models import StudentProgress


# Scrape static data
# Scrape each level table
# Create objects & write to Db


class StuRecord:
    def __init__(self, task_title='No Title', task_status='No Status', task_score='N/A', task_level='No Set'):
        self.task_title = task_title
        self.task_status = task_status
        self.task_score = task_score
        self.task_level = task_level

    def __str__(self) -> str:
        return f"{self.task_title} - {self.task_status} - {self.task_score} - {self.task_level}"


# Get driver 
def get_driver(port_url: str) -> webdriver.Edge:
    # Set up Microsoft Edge options
    edge_options = EdgeOptions()
    edge_options.add_argument('--headless')  # Run in headless mode
    edge_options.add_argument('--disable-gpu')  # Disable GPU for better compatibility
    edge_options.add_argument('--no-sandbox')  # Bypass OS security model
    edge_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

    # Path to msedgedriver
    driver: webdriver.Edge = webdriver.Edge(options=edge_options)

    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver.get(port_url)

    return driver


# Accept cookies btn
def accept_cookies(driver: webdriver.Edge) -> webdriver.Edge:
    print('⌛Waiting for element ...')

    # Waiting until an button is clickable
    accept_cookie = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')))

    accept_cookie.click() # Click button

    time.sleep(1)

    return driver


# Scrap current table
def scrap_table(driver: webdriver.Edge, level: str)-> list[StuRecord]:
    student_records = []

    if level == 'Level 1':
        get_table = driver.find_element(By.ID, 'jsLevel1')
    elif level == 'Level 2':
        get_table = driver.find_element(By.ID, 'jsLevel2')
    elif level == 'Level 3':
        get_table = driver.find_element(By.ID, 'jsLevel3')

    # Extract table data
    table_body = get_table.find_element(By.TAG_NAME, 'tbody') # Table

    table_rows = table_body.find_elements(By.TAG_NAME, 'tr') # Table rows

    task_titles = [entry\
        .find_element(By.CLASS_NAME, 'jsTaskOverview' ) 
        for entry in table_rows] # Task titles

    task_details = [entry.find_elements(By.TAG_NAME, 'td') for entry in table_rows]

    for pos, detail in enumerate(task_details): 
        _title = ''
        _score = 0
        _status = ''

        try:
            _title = task_titles[pos].text
        except Exception as ex:
            print(ex)

        try:
            _status = detail[1].text
        except Exception as ex:
            print(ex)

        try:
            _score = detail[2].text
        except Exception as ex:
            print(ex)

        _record = StuRecord(
            task_title=_title,
            task_score=_score,
            task_status=_status
        )
        student_records.append(_record)
    return student_records


# Process data into information
def process_table(table: list[StuRecord]):
    completed = [task for task in table if str(task.task_status) == 'Completed'] # Completed tasks
    below_100 = [task for task in completed if int(task.task_score) < 100] # Below 100% tasks
    resubmissions = [task for task in below_100 if int(task.task_score) <= 31] # Task resubmissions

    incomplete = [task for task in table if str(task.task_score) == 'N/A'] # Incomplete tasks (0 attempts)

    total_completed = len(completed)
    total_below = len(below_100)

    total_incomplete = len(incomplete)
    total_resubmissions = len(resubmissions)

    totals = {
        'total_completed': total_completed, 
        'total_below': total_below, 
        'total_incomplete': total_incomplete, 
        'total_resubmissions': total_resubmissions
    }

    return totals


# Scrap static and align tables with object
def scrap_port(port_url: str):     
    driver = get_driver(port_url)
    WebDriverWait(driver, 10) \
        .until(EC.presence_of_element_located((By.TAG_NAME, 'body'))) # Wait for body tag to load

    try:
        accept_cookies(driver)

    except Exception as ex:
        print(ex)
        print('Cookies already accepted!')

    # Scrap student details

    fullname = driver.find_element(
        By.CLASS_NAME, 
        'profile__excerpt-fullname'
    ).text

    bootcamp = driver.find_element(
        By.CLASS_NAME, 
        'profile__excerpt-bootcamp-level'
    ).text

    data_scrapped = {
        'Fullname': fullname,
        'Enrolled Bootcamp': bootcamp,
        'Level 1': {},
        'Level 2': {},
        'Level 3': {}
    }

    # Scrap student levels
    count = 0
    while count < 4:
        count += 1

        # Scrap level 1
        level_1 = driver.find_elements(By.ID, 'jsLevel1Tab')
        if level_1:
            WebDriverWait(driver, 10)\
                .until(EC.element_to_be_clickable((By.ID, 'jsLevel1Tab'))).click()

            lvl_table = scrap_table(driver, 'Level 1')
            totals = process_table(lvl_table)
            data_scrapped.update({'Level 1': totals})

        # Scrap level 2
        level_2 = driver.find_elements(By.ID, 'jsLevel1Tab')
        if level_2:
            WebDriverWait(driver, 10)\
                .until(EC.element_to_be_clickable((By.ID, 'jsLevel2Tab'))).click()

            lvl_table = scrap_table(driver, 'Level 2')
            totals = process_table(lvl_table)
            data_scrapped.update({'Level 2': totals})

        # Scrap level 3
        level_3 = driver.find_elements(By.ID, 'jsLevel3Tab')
        if level_3:
            WebDriverWait(driver, 10)\
                .until(EC.element_to_be_clickable((By.ID, 'jsLevel3Tab'))).click()

            lvl_table = scrap_table(driver, 'Level 3')
            totals = process_table(lvl_table)
            data_scrapped.update({'Level 3': totals})
    return data_scrapped


# Sync records with scrapped data
def sync_records():
    student_records = StudentProgress.objects.all()
    port_urls = []

    create_new = False

    for student in student_records:
        port_url = student.portfolio_url
        port_urls.append(port_url)
    
    port_urls = list(set(port_urls))

    for port_url in port_urls:
        data_scrapped = scrap_port(str(port_url))

        if student_records.filter(portfolio_url=str(port_url), level='Level 1').exists():
            pass
        else:
            create_new = True

        if create_new: # Create a new StudentProgress record
            for key, value in data_scrapped.items():
                if key == 'Level 1':
                    lvl_totals = value

                    StudentProgress(
                            fullname=data_scrapped['Fullname'],
                            bootcamp=data_scrapped['Enrolled Bootcamp'],
                            level=key,
                            portfolio_url=str(port_url),
                            completed=lvl_totals['total_completed'],
                            incomplete=lvl_totals['total_below'],
                            resubmitted=lvl_totals['total_incomplete'],
                            below_100=lvl_totals['total_resubmissions'],
                        ).save()

                if key == 'Level 2':
                    lvl_totals = value

                    StudentProgress(
                            fullname=data_scrapped['Fullname'],
                            bootcamp=data_scrapped['Enrolled Bootcamp'],
                            level=key,
                            portfolio_url=str(port_url),
                            completed=lvl_totals['total_completed'],
                            incomplete=lvl_totals['total_below'],
                            resubmitted=lvl_totals['total_incomplete'],
                            below_100=lvl_totals['total_resubmissions'],
                        ).save()
            
                if key == 'Level 3':
                    lvl_totals = value

                    StudentProgress(
                            fullname=data_scrapped['Fullname'],
                            bootcamp=data_scrapped['Enrolled Bootcamp'],
                            level=key,
                            portfolio_url=str(port_url),
                            completed=lvl_totals['total_completed'],
                            incomplete=lvl_totals['total_below'],
                            resubmitted=lvl_totals['total_incomplete'],
                            below_100=lvl_totals['total_resubmissions'],
                        ).save()

        else: # Update existing records
            for key, value in data_scrapped.items():
                update_student = student_records.filter(portfolio_url=str(port_url))

                if update_student.filter(level=str(key)).exists():
                    lvl_totals = value
                    
                    updated_student = update_student.get(level=str(key))

                    updated_student.completed = lvl_totals['total_completed']
                    updated_student.incomplete = lvl_totals['total_incomplete']
                    updated_student.resubmitted = lvl_totals['total_resubmissions']
                    updated_student.below_100 = lvl_totals['total_below']

                    updated_student.save()
