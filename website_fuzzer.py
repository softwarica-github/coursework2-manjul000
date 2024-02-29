import requests
import concurrent.futures

class WebsiteFuzzer:
    def __init__(self, url, payload, fuzz_position):
        self.url = url
        self.payload = payload
        self.fuzz_position = fuzz_position

    def fuzz_website(self, directory):
        url_to_fuzz = self.fuzz_position.replace("FUZZ", directory)

        try:
            response = requests.get(url_to_fuzz)
            response_code = response.status_code
            word_count = len(response.text.split())
            char_count = len(response.text)
        except requests.exceptions.ConnectionError as e:
            #Set response code to 000 if connection fails
            response_code = 000
            word_count = 0
            char_count = 0

        return f"value:{directory} response:{response_code} word:{word_count} char:{char_count}"

    def filter_results(self, results, response_code=None, word_count=None, char_count=None):
        filtered_results = []
        for result in results:
            values = result.split()
            if (response_code is None or values[1] == str(response_code)) and \
               (word_count is None or int(values[2]) == word_count) and \
               (char_count is None or int(values[3]) == char_count):
                filtered_results.append(result)
        return filtered_results

    def fuzz_multiple(self, directories, num_threads):
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(self.fuzz_website, directory) for directory in directories]
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
        return results
