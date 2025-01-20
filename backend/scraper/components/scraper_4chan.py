import requests
import pandas as pd
from bs4 import BeautifulSoup


class Scraper_4chan:

    board_list = ["pol"]

    def main(self, max_pages=10):

        for board in self.board_list:

            for page in range(1, max_pages+1):

                base_url = rf"https://boards.4channel.org/{board}/"
                url = f"{base_url}{page}" if page > 1 else base_url

                print(f"Initializing scraper for {board}, page {page}...")
                response = requests.get(url)

                if response.status_code != 200:
                    print(f"Failed to fetch the board. Status code: {response.status_code}")

                    return

                soup = BeautifulSoup(response.content, "html.parser")

                # Find all threads on the board
                threads = soup.find_all("div", class_="thread")

                for thread in threads:

                    thread_id = thread.get("id", "").replace("t", "")  # Extract thread ID
                    op_post = thread.find("div", class_="post op")
                    op_content = op_post.find("blockquote", class_="postMessage").text if op_post else "No content"

                    print(f"Thread ID: {thread_id}")
                    print(f"OP Content: {op_content}")
                    print("------------------------------------------------")

                    """ DATA WITHIN THREAD
                    """



if __name__ == "__main__":
    bot = Scraper_4chan()
    bot.main()