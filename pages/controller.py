from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class DragonController:
  ROLL_LEFT_BUTTON = (By.ID, 'roll-left-button')
  ROLL_RIGHT_BUTTON = (By.ID, 'roll-right-button')
  PITCH_UP_BUTTON = (By.ID, 'pitch-up-button')
  PITCH_DOWN_BUTTON = (By.ID, 'pitch-down-button')
  YAW_LEFT_BUTTON = (By.ID, 'yaw-left-button')
  YAW_RIGHT_BUTTON = (By.ID, 'yaw-right-button')

  X_FORWARD_BUTTON = (By.ID, 'translate-forward-button')
  X_BACKWARD_BUTTON = (By.ID, 'translate-backward-button')
  Y_LEFT_BUTTON = (By.ID, 'translate-left-button')
  Y_RIGHT_BUTTON = (By.ID, 'translate-right-button')
  Z_UP_BUTTON = (By.ID, 'translate-up-button')
  Z_DOWN_BUTTON = (By.ID, 'translate-down-button')

  def __init__(self, browser):
    self.browser = browser

  def roll_left(self):
    roll_left_button = self.browser.find_element(*self.ROLL_LEFT_BUTTON)
    roll_left_button.click()

  def roll_right(self):
    roll_right_button = self.browser.find_element(*self.ROLL_RIGHT_BUTTON)
    roll_right_button.click()

  def pitch_up(self):
    pitch_up_button = self.browser.find_element(*self.PITCH_UP_BUTTON)
    pitch_up_button.click()

  def pitch_down(self):
    pitch_down_button = self.browser.find_element(*self.PITCH_DOWN_BUTTON)
    pitch_down_button.click()

  def yaw_left(self):
    yaw_left_button = self.browser.find_element(*self.YAW_LEFT_BUTTON)
    yaw_left_button.click()

  def yaw_right(self):
    yaw_right_button = self.browser.find_element(*self.YAW_RIGHT_BUTTON)
    yaw_right_button.click()

  def x_forward(self):
    yaw_right_button = self.browser.find_element(*self.X_FORWARD_BUTTON)
    yaw_right_button.click()

  def x_backward(self):
    yaw_right_button = self.browser.find_element(*self.X_BACKWARD_BUTTON)
    yaw_right_button.click()

  def y_left(self):
    yaw_right_button = self.browser.find_element(*self.Y_LEFT_BUTTON)
    yaw_right_button.click()

  def y_right(self):
    yaw_right_button = self.browser.find_element(*self.Y_RIGHT_BUTTON)
    yaw_right_button.click()

  def z_up(self):
    yaw_right_button = self.browser.find_element(*self.Z_UP_BUTTON)
    yaw_right_button.click()

  def z_down(self):
    yaw_right_button = self.browser.find_element(*self.Z_DOWN_BUTTON)
    yaw_right_button.click()
