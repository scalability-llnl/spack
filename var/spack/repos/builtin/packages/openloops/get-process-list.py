import re
import urllib.request
from html.parser import HTMLParser


class my_html_parser(HTMLParser):
    def error(self, message):
        pass

    def __init__(self):
        super().__init__()
        self.state = 0
        self.processes = []

    def handle_starttag(self, tag, attrs):
        if tag == "tr" and self.state == 2:
            for att in attrs:
                if att[0] == "id":
                    return
            self.state = 3
        if tag == "td" and self.state == 3:
            self.state = 4
        pass

    def handle_endtag(self, tag):
        if tag == "table" and self.state == 1:
            self.state = 2
        pass

    def handle_data(self, data):
        # print("Encountered some data  :", data)
        if data == "Categories" and self.state == 0:
            self.state = 1

        if self.state == 4:
            if re.findall("[^a-z0-9_]", data):
                return
            self.processes.append(data)
            self.state = 2


if __name__ == "__main__":
    url = "https://openloops.hepforge.org/process_library.php?repo=public"
    data = urllib.request.urlopen(url).read()
    parser = my_html_parser()
    parser.feed(data.decode("UTF8"))
    print(parser.processes)
