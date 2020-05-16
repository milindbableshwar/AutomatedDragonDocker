from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class DragonIssDockerLoader:
  URL = 'https://iss-sim.spacex.com/'

  BEGIN_BUTTON = (By.ID, 'begin-button')

  def __init__(self, browser):
    self.browser = browser

  def load(self):
    self.browser.get(self.URL)

  def begin(self):
    begin_button = self.browser.find_element(*self.BEGIN_BUTTON)
    begin_button.click()
