import json
import os
from typing import Dict, Optional
from pathlib import Path


def get_raw_game_data() -> Optional[Dict]:
    data_volume_path = os.environ["DATA_VOLUME_PATH"]
    data_file = data_volume_path + '/' + os.environ["DATA_FILE_NAME"]
    if not Path(data_volume_path).is_dir() or not Path(data_file).is_file():
        print('Data is not exists. Attach some data volume')
        return None

    with open(data_file, encoding='utf-8', mode='r') as f:
        try:
            data = json.load(f)
        except Exception as e:
            print('some error occurs:\n', e)
            return None
        else:
            return data
