from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
from plyer import notification

if __name__ == "__main__":
    empty_rooms_before = []
    while(True):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://www.devapp.it.tum.de/iris/app/')
        time.sleep(1)
        dropdown = Select(driver.find_element(By.XPATH, '/html/body/app-root/app-home/div/div[1]/select[2]'))
        dropdown.select_by_index(1)
        rooms = driver.find_element(By.XPATH, '/html/body/app-root/app-home/div/div[2]')
        rooms_list = rooms.find_elements(By.TAG_NAME, 'div')
        rooms_list = [room for room in rooms_list if room.get_attribute("class") == 'room green']
        empty_rooms = []
        rooms_diff = []
        message = 'Rooms '
        for room in rooms_list:
            if room.find_element(By.TAG_NAME, 'b').text == 'Einzelarbeitsraum':
                empty_rooms.append(room.find_element(By.TAG_NAME, 'p').text.split('.')[2])
                if not room.find_element(By.TAG_NAME, 'p').text.split('.')[2] in empty_rooms_before:
                    message += room.find_element(By.TAG_NAME, 'p').text.split('.')[2] + ' '
                    rooms_diff.append(room.find_element(By.TAG_NAME, 'p').text.split('.')[2])
        message += 'are empty.'
        empty_rooms_before = empty_rooms
        if len(rooms_diff) != 0:
            notification.notify(
                title='Room',
                message=message,
                app_icon='tum.ico',
                timeout=15,
            )
        time.sleep(30)
        driver.close()