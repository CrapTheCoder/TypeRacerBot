import getpass
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import logging

logging.getLogger('WDM').setLevel(logging.NOTSET)


class TypeRacerBot:
    def __init__(self, driver, is_private, link, wpm=70):
        self.driver = driver
        self.is_private = is_private
        self.wpm = wpm

        self.link = link
        self.driver.get(self.link)

        sleep(3)

        if not self.is_private:
            self.enter_public_race()

        else:
            while not self.can_join_race():
                pass

            self.enter_private_race()

        sleep(2)

        while not self.has_started():
            pass

        self.type_text(self.get_text(), self.get_textbox())

    def enter_public_race(self):
        """ Press Ctrl+Alt+I to enter public race """
        self.driver.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.CONTROL + Keys.ALT + 'I')

    def enter_private_race(self):
        """ Press Ctrl+Alt+K to enter private race """
        self.driver.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.CONTROL + Keys.ALT + 'K')

    def race_again(self):
        """ Click the link to race again """
        self.driver.find_element(by=By.CLASS_NAME, value='raceAgainLink').click()

    def has_started(self):
        """ Returns whether the race has started or not """
        return self.driver.find_element(
            by=By.CSS_SELECTOR,
            value='table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > input'
        ).is_enabled()

    def can_join_race(self):
        """ Returns whether the cool-down between private races has ended """
        return len(self.driver.find_elements(by=By.CLASS_NAME, value='raceAgainLink')) > 0

    def get_text(self):
        """ Returns the text you are supposed to type """
        return self.driver.find_element(
            by=By.CSS_SELECTOR,
            value='table > tbody > tr:nth-child(2) > td > table > tbody > '
                  'tr:nth-child(1) > td > table > tbody > tr:nth-child(1) > td > div > div'
        ).text

    def get_textbox(self):
        return self.driver.find_element(
            by=By.CSS_SELECTOR,
            value='table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > input'
        )

    def type_text(self, text, textbox):
        """ Types the text with an average WPM of the parameter words_per_minute. """

        if self.wpm != 0:
            words = text.split()
            pause_time = 60 / self.wpm if self.wpm else 0

            for word in words:
                textbox.send_keys(word + ' ')
                sleep(pause_time)

        else:
            words = text.split()
            for word in words:
                textbox.send_keys(word + ' ')


def main():
    is_private = input('Is the race private? (y/n): ').lower() == 'y'

    if is_private:
        link = input('Please enter the link of the race: ')
    else:
        link = 'https://play.typeracer.com'

    wpm = int(input('Please enter the WPM you would like (0 for max speed): '))

    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument(fr"--user-data-dir=C:\Users\{getpass.getuser()}\AppData\Local\Google\Chrome\test")
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(link)

    input('Press enter when you are ready (you can log in if you would like)')

    while True:
        try:
            TypeRacerBot(driver, is_private, link, wpm)
        except UnexpectedAlertPresentException:
            pass

        print()
        input('Press enter to start new race')
        wpm = int(input('Please enter the WPM you would like (0 for max speed): '))


if __name__ == '__main__':
    main()
