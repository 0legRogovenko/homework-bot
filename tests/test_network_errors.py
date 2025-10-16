# import requests
# from unittest import TestCase, mock, main as uni_main

# from homework import main


# JSON_ERROR = {'error': 'testing'}


# class TestRequestErrors(TestCase):
#     """Тесты для проверки обработки сетевых ошибок."""

#     @mock.patch('requests.get')
#     def test_raised(self, mock_get):
#         """Симулирует сбой сети."""
#         mock_get.side_effect = mock.Mock(
#             side_effect=requests.RequestException('testing')
#         )
#         main()

#     @mock.patch('requests.get')
#     def test_error(self, mock_get):
#         """Симулирует отказ сервера."""
#         resp = mock.Mock()
#         resp.json = mock.Mock(return_value=JSON_ERROR)
#         mock_get.return_value = resp
#         main()

#     @mock.patch('requests.get')
#     def test_unexpected_status(self, mock_get):
#         """Симулирует неожиданный статус домашней работы."""
#         resp = mock.Mock()
#         resp.status_code = 333
#         resp.json = mock.Mock(return_value={})
#         mock_get.return_value = resp
#         main()

#     @mock.patch('requests.get')
#     def test_unexpected_homework_status(self, mock_get):
#         """Симулирует неожиданный статус домашней работы."""
#         resp = mock.Mock()
#         resp.status_code = 200
#         resp.json = mock.Mock(return_value={
#             'homeworks': [
#                 {'homework_name': 'test', 'status': 'test'}
#             ],
#         })
#         mock_get.return_value = resp
#         main()

#     @mock.patch('requests.get')
#     def test_invalid_json(self, mock_get):
#         """Симулирует получение некорректного JSON."""
#         resp = mock.Mock()
#         resp.status_code = 200
#         resp.json = mock.Mock(return_value={'homeworks': 1})
#         mock_get.return_value = resp
#         main()


# if __name__ == '__main__':
#     uni_main()
