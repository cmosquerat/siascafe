from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import numpy as np
import scipy.interpolate as si
import mysql.connector as connection
import pandas as pd
from datetime import date
import datetime
import os
import warnings

warnings.filterwarnings("ignore")

from funciones import execute_orden


execute_orden(pd.read_excel("plantilla.xlsx"))
