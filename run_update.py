__author__ = ['Shayan Fazeli']
__email__ = ['shayan@cs.ucla.edu']

import json
import argparse
from libraries.firestore.utils import *
import os
from libraries.post_processing.post_processing import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Firebase Integration')
    parser.add_argument('-c', '--config', default=None, type=str,
                        help='config file path (default: None)')
    args = parser.parse_args()

    with open(args.config) as handle:
        config = json.load(handle)

    db = build_db(google_key_path=config['paths']['google_key_path'])

    collection_ids = [e['collection_id'] for e in config['collection_ids']]

    if config['dates'] is None:
        dates = [get_yesterday_date()]
    else:
        dates = [e['date'] for e in config['dates']]

    temporary_output_storage_folder = os.path.abspath(config['paths']['temporary_output_storage_folder'])
    if not os.path.isdir(temporary_output_storage_folder):
        os.makedirs(temporary_output_storage_folder)

    if config['prune_temporary_output_storage_folder'] is not None:
        prune_temporary_output_storage(
            folder_path=temporary_output_storage_folder,
            start_date=config['prune_temporary_output_storage_folder']['start_date'],
            end_date=config['prune_temporary_output_storage_folder']['end_date']
        )

    for collection_id in collection_ids:
        for date in dates:
            _ = query_id_data_for_date(
                db=db,
                collection_id=collection_id,
                date=date,
                temporary_output_storage=os.path.abspath(temporary_output_storage_folder)
            )

    post_process_all(temporary_output_storage_folder)

    print('\nFetching procedure is now complete and the folder is refreshed.\n')