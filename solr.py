# -*- coding: utf-8 -*-

"""
Server Density Solr Monitoring Plugin
"""

import requests
import json

SOLR_URL = "http://localhost:8983/solr/admin/cores?action=STATUS&wt=json"


class Solr(object):

    def __init__(self, agent_config, checks_logger, raw_config):
        self.agent_config = agent_config
        self.logger = checks_logger
        self.raw_config = raw_config

    def run(self):
        try:
            data = {'Active': False}
            solr_status = requests.get(SOLR_URL).content
            solr_status = json.loads(solr_status)
            solr_status = solr_status['status'][''] ## single, unamed core
        except (ValueError, KeyError, requests.RequestException):
            self.logger.error('Unable to access {0}'.format(SOLR_URL))
        except Exception:
            self.logger.exception('Error occurred accessing {0}'.format(SOLR_URL))
        else:
            size_in_mb = solr_status['index']['sizeInBytes'] / 1048576.0
            uptime_in_hours = solr_status['uptime'] / 1000 / 3600
            data = {
                'Active': True,
                'Uptime (mins)': uptime_in_hours,
                'Doc count': solr_status['index']['numDocs'],
                'Size (MB)': size_in_mb
            }
        finally:
            return data
