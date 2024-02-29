import unittest
from unittest.mock import patch
from website_fuzzer import WebsiteFuzzer

class TestWebsiteFuzzer(unittest.TestCase):

    def test_fuzz_website(self):
        # Mocking the requests.get method to simulate a response
        with patch('requests.get') as mocked_get:
            mocked_response = type('MockResponse', (), {'status_code': 200, 'text': 'Sample text'})
            mocked_get.return_value = mocked_response

            # Initialize the WebsiteFuzzer object
            fuzzer = WebsiteFuzzer("http://example.com", "payload", "http://example.com/FUZZ")

            # Test fuzz_website method
            result = fuzzer.fuzz_website("directory")
            self.assertEqual(result, "value:directory response:200 word:2 char:11")


    def test_fuzz_multiple(self):
        # Sample directories and number of threads
        directories = ["dir1", "dir2", "dir3"]
        num_threads = 2

        # Initialize the WebsiteFuzzer object
        fuzzer = WebsiteFuzzer("http://example.com", "payload", "http://example.com/FUZZ")

        # Test fuzz_multiple method
        results = fuzzer.fuzz_multiple(directories, num_threads)
        self.assertEqual(len(results), len(directories))  # Expecting results for all directories


if __name__ == '__main__':
    unittest.main()
