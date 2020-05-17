import re
import _thread
import time

from selenium.webdriver.common.by import By


class StatsReader:

  ROLL_ERROR_ID = (By.XPATH, f"//div[@id='hud']//div[@id='roll']//div[@class='error']")
  ROLL_ERROR_RATE_ID = (By.XPATH, f"//div[@id='hud']//div[@id='roll']//div[@class='rate']")
  PITCH_ERROR_ID = (By.XPATH, f"//div[@id='hud']//div[@id='pitch']//div[@class='error']")
  PITCH_ERROR_RATE_ID = (By.XPATH, f"//div[@id='hud']//div[@id='pitch']//div[@class='rate']")
  YAW_ERROR_ID = (By.XPATH, f"//div[@id='hud']//div[@id='yaw']//div[@class='error']")
  YAW_ERROR_RATE_ID = (By.XPATH, f"//div[@id='hud']//div[@id='yaw']//div[@class='rate']")

  X_RANGE_ID = (By.XPATH, f"//div[@id='hud']//div[@id='pyr']//div[@id='x-range']//div[@class='distance']")
  Y_RANGE_ID = (By.XPATH, f"//div[@id='hud']//div[@id='pyr']//div[@id='y-range']//div[@class='distance']")
  Z_RANGE_ID = (By.XPATH, f"//div[@id='hud']//div[@id='pyr']//div[@id='z-range']//div[@class='distance']")


  def __init__(self, browser):
    self.browser = browser

  def start_computing_translation_rates(self):
    self.old_x_range = self.x_range()
    self.x_rate = 0
    _thread.start_new_thread(self.compute_translation_rate, (self.x_range, self.set_x_rate, self.get_old_x_range, self.set_old_x_range))
    self.old_y_range = self.y_range()
    self.y_rate = 0
    _thread.start_new_thread(self.compute_translation_rate, (self.y_range, self.set_y_rate, self.get_old_y_range, self.set_old_y_range))
    self.old_z_range = self.z_range()
    self.z_rate = 0
    _thread.start_new_thread(self.compute_translation_rate, (self.z_range, self.set_z_rate, self.get_old_z_range, self.set_old_z_range))

  def compute_translation_rate(self, get_range, set_rate, get_old_range, set_old_range):
    while True:
      time.sleep(1)
      current_range = get_range()
      set_rate(get_old_range() - current_range)
      set_old_range(current_range)

  def set_x_rate(self, rate):
    self.x_rate = rate

  def get_old_x_range(self):
    return self.old_x_range

  def set_old_x_range(self, range):
    self.old_x_range = range

  def x_range_rate(self):
    return self.x_rate


  def set_y_rate(self, rate):
    self.y_rate = rate

  def get_old_y_range(self):
    return self.old_y_range

  def set_old_y_range(self, range):
    self.old_y_range = range

  def y_range_rate(self):
    return self.y_rate



  def set_z_rate(self, rate):
    self.z_rate = rate

  def get_old_z_range(self):
    return self.old_z_range

  def set_old_z_range(self, range):
    self.old_z_range = range

  def z_range_rate(self):
    return self.z_rate




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

  def x_range(self):
    return self.parseFromDom(*self.X_RANGE_ID)

  def y_range(self):
    return self.parseFromDom(*self.Y_RANGE_ID)

  def z_range(self):
    return self.parseFromDom(*self.Z_RANGE_ID)
