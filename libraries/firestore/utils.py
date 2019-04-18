__author__ = ['Shayan Fazeli']
__email__ = ['shayan@cs.ucla.edu']

from google.cloud import datastore
import google.auth
import warnings
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import _pickle as pickle
import os
import sys
import json
warnings.filterwarnings('ignore')


def get_yesterday_date():
    now = datetime.datetime.now()
    return '{:2d}-{:02d}-{:02d}'.format(now.year, now.month, now.day-1)


def build_client(google_key_path):
    credentials, project = google.auth.default()
    client = datastore.Client.from_service_account_json(google_key_path)
    return client


def query_id_data_for_date(db, collection_id, date, temporary_output_storage=None):
    ref = db.collection(collection_id)
    ref = ref.where(u'StartDate', u'==', get_yesterday_date())
    docs = list(ref.get())
    docs = [doc.to_dict() for doc in docs]
    if temporary_output_storage is None:
        return docs
    else:
        if not os.path.isdir(os.path.join(temporary_output_storage, date.replace('-', '_'))):
            os.makedirs(os.path.join(temporary_output_storage, date.replace('-', '_')))
        with open(os.path.join(temporary_output_storage, date.replace('-', '_'), collection_id + '.pkl'), 'wb') as fid_pkl:
            pickle.dump(docs, fid_pkl)
        with open(os.path.join(temporary_output_storage, date.replace('-', '_'), collection_id + '.json'), 'w') as fid_json:
            json.dump(docs, fid_json)
        return docs


def build_db(google_key_path):
    cred = credentials.Certificate(google_key_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db


def prune_temporary_output_storage(folder_path, start_date, end_date):
    start_int = int(start_date.replace('-', ''))
    end_int = int(end_date.replace('-', ''))
    subfolders = os.listdir(folder_path)
    for subfolder in subfolders:
        current_int = int(subfolder.replace('_', ''))
        if not (current_int >= start_int and current_int <= end_int):
            os.system('rm -rf ' + os.path.abspath(
                os.path.join(folder_path, subfolder)
            ))