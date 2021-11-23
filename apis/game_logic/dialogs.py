import json
from json import JSONEncoder
from typing import List, Tuple, Dict, Optional

from pydantic import BaseModel


class Choice:  # (BaseModel):
    def __init__(self, header: str, to_dialog_id: str):
        self.header = header
        self.to_dialog_id = to_dialog_id
        # super().__init__(**{'header': header, 'to_dialog_id': to_dialog_id})

    header: str
    to_dialog_id: str


class View:
    def __init__(self, id_: str, header: str, content: str, choices: List[Choice]):
        self.id = id_
        self.header = header
        self.content = content
        self.choices = choices

    def get_destination_id_list(self):
        return [choice.to_dialog_id for choice in self.choices]

    def get_dialog_dict(self) -> dict:
        return {
            'id': self.id,
            'pre_text': {
                'header': self.header,
                'content': self.content
            },
            'choices': self.choices
        }

    def copy(self) -> "View":
        return View(self.id, self.header, self.content, self.choices)


class DialogsManager:

    def add(self, dialog_id: str, view: View, save_mode: bool = True) -> "DialogsManager":
        if not self._editable:
            raise ValueError('can\'t to add view after application of the check_dialogs methods', {})

        if save_mode and dialog_id in self._dialogs:
            raise ValueError('dialog_id is already stored',
                             {'dialog_id': dialog_id})

        self._dialogs[dialog_id] = view
        return self

    def get_all_dialogs(self) -> Dict[str, View]:
        return self._dialogs.copy()

    def get_all_dialogs_json(self) -> Dict[str, dict]:
        json_dialogs = {}
        for key, view in self._dialogs:
            json_dialogs[key] = view.get_dialog_dict()
        return json_dialogs

    def check_dialogs(self) -> Optional[ValueError]:
        if self._editable is False:
            return None
        else:
            self._editable = False
        # TODO checks ending of every branch
        return None

    def __init__(self, dialogs: Dict[str, View] = None):
        if dialogs is None:
            dialogs = {}

        self._editable: bool = True
        self._dialogs: Dict[str, View] = dialogs

    def __getitem__(self, item) -> View:
        return self._dialogs[item].copy()

    def __contains__(self, item) -> bool:
        return item in self._dialogs


# class Game:
#     @property
#     def current_view(self) -> View:
#         return self._dialogs[self._carriage]
#
#     def next(self, choice_index: int):
#         choices = self.current_view.choices
#         if not 0 <= choice_index < len(choices):
#             raise ValueError(f'choice_index must be in range: [0; len(choices))',
#                              {'choice_index': choice_index, 'len(choices)': len(choices)})
#
#         self._carriage = choices[choice_index].to_dialog_id
#
#     def __init__(self, dialogs: DialogsManager, entry_id: str):
#         if entry_id not in dialogs:
#             raise ValueError('entry_id key is not contains in dialogs.keys()',
#                              {'dialogs': dialogs, 'entry_id': entry_id})
#
#         dialog_errors = dialogs.check_dialogs()
#         if dialog_errors:
#             raise dialog_errors
#
#         self._dialogs = dialogs
#         self._carriage = entry_id




