import logging

FORMAT = "[%(asctime)s] %(message)s"
logging.basicConfig(format=FORMAT,
                    filename="gitbot-log.log", 
                    filemode="a",
                    level=logging.WARN)
mylogger = logging.getLogger()

