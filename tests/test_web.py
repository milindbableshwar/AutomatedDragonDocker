import pytest
import time

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
  threshold = 0.3
  while True:
    time.sleep(0.2)
    if (abs(stats_reader.roll_error()) < 2):
      maxRate = 0.1
    elif (abs(stats_reader.roll_error()) < 5):
      maxRate = 0.2
    elif (abs(stats_reader.roll_error()) < 10):
      maxRate = 0.3
    else:
      maxRate = 0.4

    if (abs(stats_reader.roll_error()) <= threshold):
      if (abs(stats_reader.roll_error_rate()) > 0.0):
        if (stats_reader.roll_error_rate() < 0):
          controller.roll_right()
        elif (stats_reader.roll_error_rate() > 0):
          controller.roll_left()
      else:
        print ('Success!!!')
        time.sleep(3)

    if (stats_reader.roll_error() > threshold and stats_reader.roll_error_rate() < maxRate):
      print ("Rolling right ...")
      controller.roll_right()
    elif (stats_reader.roll_error() > threshold and stats_reader.roll_error_rate() > maxRate):
      print ("decreasing right rate ...")
      controller.roll_left()
    elif (stats_reader.roll_error() < -threshold and stats_reader.roll_error_rate() > -maxRate):
      print ("Rolling left ...")
      controller.roll_left()
    elif (stats_reader.roll_error() < -threshold and stats_reader.roll_error_rate() < -maxRate):
      print ("decreasing left rate ...")
      controller.roll_right()

    print("Roll: " + str(stats_reader.roll_error()) + " with rate " + str(stats_reader.roll_error_rate()))
