import json
from json.encoder import JSONEncoder

from apis.game_logic.dialogs import DialogsManager, View, Choice


ENTRY_DIALOG_NAME = 'entry'


def get_built_dialogs() -> DialogsManager:

    dialogs = DialogsManager() \
        .add('entry', View(
            id_='entry',
            header='Сон',
            content='Ты во сне, что будешь делать?',
            choices=[
                Choice(header='Пойти прямо', to_dialog_id='still_sleep'),
                Choice(header='Пойти обратно', to_dialog_id='still_sleep'),
                Choice(header='Проснуться', to_dialog_id='woke_up')
            ]
        )
    ) \
        .add('still_sleep', View(
            id_='still_sleep',
            header='Все еще сон',
            content='Ты все еще во сне, что будешь делать?',
            choices=[
                Choice(header='Пойти прямо', to_dialog_id='still_sleep'),
                Choice(header='Пойти обратно', to_dialog_id='still_sleep'),
                Choice(header='Проснуться', to_dialog_id='woke_up')
            ]
        )
    ) \
        .add('woke_up', View(
            id_='woke_up',
            header='Пробуждение',
            content='Ну вот ты и проснулся',
            choices=[
                Choice(header='Начать кодить', to_dialog_id='coding_time'),
                Choice(header='Поспать', to_dialog_id='entry')
            ]
        )
    ) \
        .add('coding_time', View(
            id_='coding_time',
            header='Кодинг',
            content='Ну вот ты и покодил',
            choices=[
                Choice(header='Покодить еще', to_dialog_id='coding_time'),
                Choice(header='Поспать', to_dialog_id='entry')
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

    dialogs = get_built_dialogs()

    json_dialog = json.loads(json.dumps(dialogs[ENTRY_DIALOG_NAME], cls=_MyEncoder))
    print('entry:', json_dialog)

    # game = Game(dialogs, ENTRY_DIALOG_NAME)


if __name__ == '__main__':
    main()
