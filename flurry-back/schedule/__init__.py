import datetime
import logging
from ..utils.trend_builder import get_trends

import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    
    logging.info(f"Executed Fetch News")
    get_trends()
