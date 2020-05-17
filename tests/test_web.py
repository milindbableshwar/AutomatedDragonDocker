import pytest
import time
import threading

from pages.read_stats import StatsReader
from pages.load_game import DragonIssDockerLoader
from pages.controller import DragonController

from selenium.webdriver import Chrome

# pipenv run python -m pytest -s

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
  # wait for game to initiate and load
  time.sleep(10)

  stats_reader = StatsReader(browser)
  controller = DragonController(browser)

  sleep_duration = 0.2
  Roll_control_thread = threading.Thread(target=control_the_dragon,
   args = ("Roll",
    sleep_duration,
    stats_reader.roll_error,
    stats_reader.roll_error_rate,
    controller.roll_right,
    controller.roll_left))
  Pitch_control_thread = threading.Thread(target=control_the_dragon,
   args = ("Pitch",
    sleep_duration,
    stats_reader.pitch_error,
    stats_reader.pitch_error_rate,
    controller.pitch_down,
    controller.pitch_up))
  Yaw_control_thread = threading.Thread(target=control_the_dragon,
   args = ("Yaw",
    sleep_duration,
    stats_reader.yaw_error,
    stats_reader.yaw_error_rate,
    controller.yaw_right,
    controller.yaw_left))

  stats_reader.start_computing_translation_rates()
  sleep_duration_for_translation = 0.5
  X_control_thread = threading.Thread(target=control_the_dragon,
   args = ("X",
    sleep_duration_for_translation,
    stats_reader.x_range,
    stats_reader.range_rate,
    controller.x_forward,
    controller.x_backward,
    3,
    True))
  Y_control_thread = threading.Thread(target=control_the_dragon,
   args = ("Y",
    sleep_duration_for_translation,
    stats_reader.y_range,
    stats_reader.y_range_rate,
    controller.y_left,
    controller.y_right))
  Z_control_thread = threading.Thread(target=control_the_dragon,
   args = ("Z",
    sleep_duration_for_translation,
    stats_reader.z_range,
    stats_reader.z_range_rate,
    controller.z_down,
    controller.z_up))
  Roll_control_thread.start()
  Pitch_control_thread.start()
  Yaw_control_thread.start()
  X_control_thread.start()
  Y_control_thread.start()
  Z_control_thread.start()

  # wait till all thread throw exceptions that they cannot find certain elements.
  # Need to exit more gracefully, but deal with it for now
  X_control_thread.join()

  # relish the success screen :)
  time.sleep(30)



def control_the_dragon(control, sleep_duration, error_func, error_rate_func, increase_rate, decrease_rate, step_multiplier=1, invert_error_rate=False):
  try:
    threshold = 0.1
    while True:
      time.sleep(sleep_duration)
      error = error_func()
      error_rate = error_rate_func()

      if (abs(error) < 5 * step_multiplier):
        maxRate = 0.1
      elif (abs(error) < 10 * step_multiplier):
        maxRate = 0.2
      elif (abs(error) < 15 * step_multiplier):
        maxRate = 0.3
      else:
        maxRate = 0.4
        if (invert_error_rate):
          maxRate = 1.0

      if (invert_error_rate):
        error_rate = -error_rate
        if (error < 10):
          maxRate = 0.05

      if (abs(error) <= threshold):
        if (abs(error_rate) > 0.0):
          if (error_rate < 0):
            increase_rate()
          elif (error_rate > 0):
            decrease_rate()
        else:
          time.sleep(2)

      # avoid excessing forward/backward control
      if (control == "X" and abs(error_rate - maxRate) < 0.1 and error > 10):
        continue
      if (error > threshold and error_rate < maxRate):
        # Increasing rate within max rate limit because of error
        increase_rate()
      elif (error > threshold and error_rate > maxRate):
        # Decreasing increased rate because of max rate limit
        decrease_rate()
      elif (error < -threshold and error_rate > -maxRate):
        # Decreasing rate within max rate limit because of error
        decrease_rate()
      elif (error < -threshold and error_rate < -maxRate):
        # Increasing decreased rate because of max rate limit
        increase_rate()

      # print(control + ": Error: " + str(error) + " Error rate " + str(error_rate))
  except:
    return
