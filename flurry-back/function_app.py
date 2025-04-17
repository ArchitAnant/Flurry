import azure.functions as func
import datetime
import json
import logging
from utils.trend_builder import get_trends

app = func.FunctionApp()

get_trends()