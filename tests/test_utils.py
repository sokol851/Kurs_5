import psycopg2
from config import config
from utils.utils import create_database, create_tables, choice_menu


def test_choice_menu(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '9')
    assert choice_menu() == print('Работа завершена!')
