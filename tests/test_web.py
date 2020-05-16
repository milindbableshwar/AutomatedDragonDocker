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
  controller.roll_left()
  controller.roll_left()
  controller.roll_right()
  controller.pitch_up()
  controller.pitch_up()
  controller.pitch_down()
  controller.yaw_left()
  controller.yaw_left()
  controller.yaw_right()
  time.sleep(10)
