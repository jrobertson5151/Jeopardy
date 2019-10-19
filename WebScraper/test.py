import sys
import traceback

from game import *
from season import *

driver = driver_init()
try:
    for i in range(12,36):
        season(i, 'data/season_' + str(i), driver)
except:
    traceback.print_exc(file=sys.stdout)
finally:
    driver.close()
