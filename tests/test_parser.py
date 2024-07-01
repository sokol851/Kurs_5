from src.parser import HHParser
import pytest


@pytest.mark.usefixtures
def create_exemplar():
    return HHParser()


def test_get_request():
    assert len(create_exemplar().get_employers('')) > 0
    assert len(create_exemplar().get_employers('not_found_test_in_employers')) == 0
    assert len(create_exemplar().get_all_vacancies('')) > 0
    assert len(create_exemplar().get_employers('not_found_test_in_vacancies')) == 0
