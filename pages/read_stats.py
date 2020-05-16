import re

from selenium.webdriver.common.by import By


class StatsReader:

  ROLL_ERROR_ID = (By.XPATH, f"//div[@id='hud']//div[@id='roll']//div[@class='error']")
  ROLL_ERROR_RATE_ID = (By.XPATH, f"//div[@id='hud']//div[@id='roll']//div[@class='rate']")
  PITCH_ERROR_ID = (By.XPATH, f"//div[@id='hud']//div[@id='pitch']//div[@class='error']")
  PITCH_ERROR_RATE_ID = (By.XPATH, f"//div[@id='hud']//div[@id='pitch']//div[@class='rate']")
  YAW_ERROR_ID = (By.XPATH, f"//div[@id='hud']//div[@id='yaw']//div[@class='error']")
  YAW_ERROR_RATE_ID = (By.XPATH, f"//div[@id='hud']//div[@id='yaw']//div[@class='rate']")


  def __init__(self, browser):
    self.browser = browser

  def parseFromDom(self, *id):
    text = self.browser.find_element(*id).text
    return float(re.findall(r"[-+]?\d*\.\d+|\d+", text)[0])

  def roll_error(self):
    return self.parseFromDom(*self.ROLL_ERROR_ID)

  def pitch_error(self):
    return self.parseFromDom(*self.PITCH_ERROR_ID)

  def yaw_error(self):
    return self.parseFromDom(*self.YAW_ERROR_ID)

  def roll_error_rate(self):
    return self.parseFromDom(*self.ROLL_ERROR_RATE_ID)

  def pitch_error_rate(self):
    return self.parseFromDom(*self.PITCH_ERROR_RATE_ID)

  def yaw_error_rate(self):
    return self.parseFromDom(*self.YAW_ERROR_RATE_ID)
