__author__ = ['Shayan Fazeli']
__email__ = ['shayan@cs.ucla.edu']

import os
from libraries.extra.walking_charts import *


def unit_post_processing(path, folder_name):
    """
    :param path:
    :param folder_name:
    :return: IMPLEMENT THIS FOR YOUR OWN POSTPROCESSING
    """
    subject_id = "TW06NA"
    subject_log_id = "TW06NA_Log"
    data_directory = os.path.join(path, folder_name, subject_id, subject_id + ".json")
    step_counter(data_directory, subject_id, folder_name)


def post_process_all(path='./temporary_output_storage/'):
    path = os.path.abspath(path)
    folders = os.listdir(path)
    for folder_name in folders:
        unit_post_processing(path, folder_name)
