import unittest
from handlers.commands.credentials import cmd_credentials, process_email, process_password, process_url
from unittest.mock import MagicMock
from aiogram.dispatcher import FSMContext


class TestCredentialsCommands(unittest.TestCase):
    def setUp(self):
        self.message = MagicMock(text='https://example.com')
        self.storage = MagicMock()
        self.chat = MagicMock()
        self.user = MagicMock()
        self.storage.check_address.return_value = (self.chat, self.user)
        self.state = FSMContext(self.storage, self.chat, self.user)

    def test_cmd_credentials(self):
        # Arrange
        expected_text = "Введите url для hookah.work"

        # Act
        cmd_credentials(self.message)

        # Assert
        self.message.answer.assert_called_with(expected_text)
        self.state.set.assert_called()

    def test_process_url(self):
        # Arrange
        expected_url = 'https://example.com'

        # Act
        process_url(self.message, self.state)

        # Assert
        self.state.next.assert_called()
        self.state.proxy.return_value.__enter__.return_value['url'] == expected_url
