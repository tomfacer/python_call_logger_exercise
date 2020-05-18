from time import sleep
import random


VARIATION_MAX = 1000
VARIATION_MIN = VARIATION_MAX * -1

def work(sleep_val: int):

    calc = (sleep_val + random.randrange(VARIATION_MIN, VARIATION_MAX)) / 1000
    sleep(calc)
