import json
import os
from json.encoder import JSONEncoder

from .dialogs import DialogsManager, View, Choice
from .data_reader import get_raw_game_data

ENTRY_DIALOG_NAME = 'entry'


def get_built_dialogs() -> DialogsManager:
    try:
        raw_data = get_raw_game_data()
        if raw_data is None:
            raise Exception
    except Exception:
        return get_default_dialogs()
    else:
        data = {}
        for key, val in raw_data.items():
            data[key] = View(
                id_=key,
                header=val['header'],
                content=val['content'],
                choices=[Choice(
                    header=ch['header'],
                    to_dialog_id=ch['to_dialog_id']
                ) for ch in val['choices']]
            )
        return DialogsManager(data)


def get_default_dialogs() -> DialogsManager:
    dialogs = DialogsManager() \
        .add('entry', View(
            id_='entry',
            header='Сон',
            content='Ты во сне, что будешь делать?',
            choices=[
                Choice(header='Пойти прямо', to_dialog_id='still_sleep'),
                Choice(header='Пойти обратно', to_dialog_id='still_sleep')
            ]
        )
    ) \
        .add('still_sleep', View(
            id_='still_sleep',
            header='Все еще сон',
            content='Ты все еще во сне, что будешь делать?',
            choices=[
                Choice(header='Пойти прямо', to_dialog_id='still_sleep'),
                Choice(header='Пойти обратно', to_dialog_id='still_sleep')
            ]
        )
    )
    return dialogs


# --------------
#  Test Section
# --------------

def main():
    class _MyEncoder(JSONEncoder):
        def default(self, o):
            if hasattr(o, '__dict__'):
                return o.__dict__
            else:
                return o

    manager = get_built_dialogs()

    dialogs = manager.get_all_dialogs()

    json_dialog = json.dumps(dialogs, cls=_MyEncoder, ensure_ascii=False)
    print(json_dialog)

    # game = Game(dialogs, ENTRY_DIALOG_NAME)


if __name__ == '__main__':
    main()
