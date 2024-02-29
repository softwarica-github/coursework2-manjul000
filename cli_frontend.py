from website_fuzzer import WebsiteFuzzer

def cli_menu():
    print("Welcome to Website Fuzzer CLI Menu")
    url = input("Enter the URL to fuzz: ")
    payload = input("Enter the list of directories/sub-directories/sub-domains (comma-separated): ").split(',')
    fuzz_position = input("Enter the fuzz position (e.g., FUZZ): ")
    num_threads = int(input("Enter the number of threads: "))

    fuzzer = WebsiteFuzzer(url, payload, fuzz_position)
    directories = fuzzer.payload
    results = fuzzer.fuzz_multiple(directories, num_threads)

    print("Fuzzing results:")
    for result in results:
        print(result)

if __name__ == "__main__":
    cli_menu()
