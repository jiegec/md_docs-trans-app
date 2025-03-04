import unittest
from pathlib import Path
from unittest import mock
from unittest.mock import Mock

import pytest

from md_translate.file_translator import FileTranslator

fixture = Path('tests/test_data/fixture.md')
fixture_translated = Path('tests/test_data/fixture_translated.md')
file_to_test_on = Path('tests/test_data/file_to_test_on.md')


@pytest.fixture()
def temp_test_file():
    file_to_test_on.write_text(fixture.read_text())
    yield
    file_to_test_on.unlink()


class TestFileTranslator:
    @mock.patch('translators.translate_text')
    def test_file_translator(self, translator_mock, temp_test_file):
        class SettingsMock:
            service_name = 'yandex'
            source_lang = 'en'
            target_lang = 'ru'
            api_key = 'TEST_API_KEY'

        translator_mock.return_value = 'Переведенная строка'
        with FileTranslator(SettingsMock(), file_to_test_on) as file_translator:
            assert isinstance(file_translator, FileTranslator)
            file_translator.translate()
        translator_mock.assert_called_with(
            'Some string for translation\n', translator='yandex', from_language='en', to_language='ru')

        assert file_to_test_on.read_text() == fixture_translated.read_text()
