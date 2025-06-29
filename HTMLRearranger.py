import sys

from html.parser import HTMLParser
from pathlib import Path


class HTMLRearranger(HTMLParser):
    MAXFILES = 5    # try filename(n) replacement up to n=MAXFILES
    TAB = 2         # indentation size = " " * TAB
    SAVEPATH = "./tests/"

    def __init__(self, filename: str = "newdoc.html", voidtags: set = {}):
        HTMLParser.__init__(self)
        
        self.voidtags = voidtags
        self.filepath = self.__path_checker(filename)
        self.__createfile()
        self.indlvl = 0
        self.newline = True
        self.open = False

    @staticmethod
    def warning(msg: str, level: str = "INFO"):
        if level == "INFO":
            stream = sys.stdout
        else:
            stream = sys.stderr

        print(f"*** {level}: {msg}", file=stream)

    def __path_checker(self, filename: str) -> str:
        if '/' in filename:
            bar = filename.split('/')
            savepath = "/".join(bar[:-1]) + "/"
            filename = bar[-1]
        else:
            savepath = self.SAVEPATH

        if Path(savepath).exists():
            self.warning(f"Saving new file to {savepath}")
        else:
            raise FileNotFoundError(f"Directory not found: {savepath}")

        if '.' not in filename:
            filename = filename + ".html"
            self.warning("File format missing, saving as html-file.")
            
        filepath = Path(savepath + filename)
        i = 1
        foo = filename.split(".")
        while filepath.is_file() and i <= self.MAXFILES:
            newname = f"({i}).".join(foo)
            filepath = Path(savepath + newname)
            i+=1

        if i > self.MAXFILES:
            self.warning(f"Overwriting file: {filepath}", "WARNING")
   
        return filepath

    def __createfile(self):
        with open(self.filepath, 'w') as f:
            f.write("<!DOCTYPE html>\n")

    def __writeline(self, content: str):
        if self.indlvl < 0:
            pos = self.getpos()[0]
            raise IndentationError(f"{content}, line {pos}")

        with open(self.filepath, 'a') as f:
            if self.newline:
                indent = " " * self.TAB * self.indlvl
                f.write("\n" + indent + content)
            else:
                f.write(content)

    def handle_starttag(self, tag, attrs):
        if tag in self.voidtags:
            self.handle_startendtag(tag, attrs)
            return

        self.newline = True
        if self.open:
            self.indlvl += 1

        attrstr = [f" {attr}=\"{value}\"" for attr,value in attrs]
        self.__writeline(f"<{tag}{"".join(attrstr)}>")
        
        self.open = True

    def handle_endtag(self, tag):
        if not self.open:
            self.newline = True
        if self.newline:
            if self.indlvl > 0:
                self.indlvl -= 1
            else:
                pos = self.getpos()[0]
                self.warning(f"</{tag}> indentation weirdness, line {pos}")
        
        self.__writeline(f"</{tag}>")
        self.newline = True
        self.open = False

    def handle_startendtag(self, tag, attrs):
        self.newline = True
        if self.open:
            self.indlvl += 1

        attrstr = [f" {attr}=\"{value}\"" for attr,value in attrs]
        self.__writeline(f"<{tag}{"".join(attrstr)} />")
        self.open = False
        
    def handle_data(self, data):
        cleandata = []
        datalines = data.split("\n")
        for line in datalines:
            if line.strip() != "":
                cleandata.append(line)

        if cleandata:
            if len(cleandata) == 1:
                self.newline = False
                self.__writeline(cleandata[0])
            else:
                self.newline = True
                for line in cleandata:
                    self.__writeline(line)

    def handle_comment(self, data):
        self.newline = True
        self.__writeline(f"<!--{data}-->")


if __name__ == "__main__":
    testdoc = "./tests/html_test_doc.html"
    # newfile = "./pretty.html"
    newfile = "pretty.html"

    parser = HTMLRearranger(newfile)
    with open(testdoc,'r') as f:
        html_doc = f.read()
    
    parser.feed(html_doc)
    parser.close()
    print('*** \N{goat}')