import logging
import os
import time

def get_time():
    return time.strftime("[%H:%M:%S|%b %d, %Y]")
    
logging.basicConfig(filename=os.path.join("code","log","log.txt"), level=logging.DEBUG,format="{} %(message)s".format(get_time()))
logging.debug("Debug logging test...")
