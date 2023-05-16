
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as exc
from selenium.common.exceptions import NoSuchElementException
from func_timeout import func_set_timeout
import requests
import time
import pytz
from datetime import datetime
import random
import json
import pyautogui
import urllib3

a = "https://www.pixiv.net/artworks/106561394"

print(a[31:])