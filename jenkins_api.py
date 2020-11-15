import configparser
import datetime
import logging


def get_coinfig(chose):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.getcwd(), 'jenkins_server.ini'))
    username = config.get(chose, 'username')
    password = config.get(chose, 'password')
    host = config.get(chose, 'host')
    port = config.get(chose, 'port')
    url = "http://" + host + ":" + port
    return url, username, password



class JenkinDemo:

    def __init__(self, job_name, chose='jenkins'):
        self.job_name = job_name
        config = get_coinfig(chose)
        


