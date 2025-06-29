from html.parser import HTMLParser

class TagLib(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)

        self.taglist = []
        self.voidtags = []
        self.weird = []

    def handle_starttag(self, tag, attrs):
        self.taglist.append(tag)

    def handle_endtag(self, tag):
        if tag in self.taglist:
            while self.taglist[-1] != tag:
                self.voidtags.append(self.taglist.pop())
            self.taglist.pop()

        else:
            pos = self.getpos()[0]
            self.weird.append((tag,pos))

    def handle_startendtag(self, tag, attrs):
        self.voidtags.append(tag)

    def get_voidlist(self) -> list:
        if self.weird:
            print(f"Found end tags without start tag:")
            for tag,pos in self.weird:
                print(f"</{tag}>, line {pos}")

        return self.voidtags


if __name__ == "__main__":
    print('*** \N{goat} Try running: main.py --help')