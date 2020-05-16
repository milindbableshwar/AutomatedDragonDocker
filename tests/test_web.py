import pytest
import time
import _thread

from pages.read_stats import StatsReader
from pages.load_game import DragonIssDockerLoader
from pages.controller import DragonController

from selenium.webdriver import Chrome


@pytest.fixture
def browser():
  # Initialize ChromeDriver
  driver = Chrome()

  # Wait implicitly for elements to be ready before attempting interactions
  driver.implicitly_wait(10)

  # Return the driver object at the end of setup
  yield driver

  # For cleanup, quit the driver
  driver.quit()


def test_basic_simulator_game(browser):
  # Load the game
  game_page = DragonIssDockerLoader(browser)
  game_page.load()
  game_page.begin()

  stats_reader = StatsReader(browser)
  controller = DragonController(browser)
  time.sleep(10)
  _thread.start_new_thread(control_the_dragon,
   ("Roll",
    stats_reader.roll_error,
    stats_reader.roll_error_rate,
    controller.roll_right,
    controller.roll_left))
  _thread.start_new_thread(control_the_dragon,
   ("Pitch",
    stats_reader.pitch_error,
    stats_reader.pitch_error_rate,
    controller.pitch_down,
    controller.pitch_up))
  _thread.start_new_thread(control_the_dragon,
   ("Yaw",
    stats_reader.yaw_error,
    stats_reader.yaw_error_rate,
    controller.yaw_right,
    controller.yaw_left))
  time.sleep(300)

def control_the_dragon(control, error_func, error_rate_func, increase_rate, decrease_rate):
  threshold = 0.1
  while True:
    time.sleep(0.2)
    if (abs(error_func()) < 2):
      maxRate = 0.1
    elif (abs(error_func()) < 5):
      maxRate = 0.2
    elif (abs(error_func()) < 10):
      maxRate = 0.3
    else:
      maxRate = 0.4

    if (abs(error_func()) <= threshold):
      if (abs(error_rate_func()) > 0.0):
        if (error_rate_func() < 0):
          increase_rate()
        elif (error_rate_func() > 0):
          decrease_rate()
      else:
        print (control + ': Equilibrium!!!')
        time.sleep(3)

    if (error_func() > threshold and error_rate_func() < maxRate):
      # Increasing rate within max rate limit because of error
      increase_rate()
    elif (error_func() > threshold and error_rate_func() > maxRate):
      # Decreasing increased rate because of max rate limit
      decrease_rate()
    elif (error_func() < -threshold and error_rate_func() > -maxRate):
      # Decreasing rate within max rate limit because of error
      decrease_rate()
    elif (error_func() < -threshold and error_rate_func() < -maxRate):
      # Increasing decreased rate because of max rate limit
      increase_rate()

    print(control + ": Error: " + str(error_func()) + " Error rate " + str(error_rate_func()))
