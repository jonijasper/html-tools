import sys

from html.parser import HTMLParser
from pathlib import Path


class HTMLRearranger(HTMLParser):
    MAXFILES = 5    # try filename(n) replacement up to n=MAXFILES
    TAB = 2         # indentation size = " " * TAB
    SAVEPATH = "./tests/"

    def __init__(self, filename: str = "newdoc.html"):
        HTMLParser.__init__(self)
        
        self.filepath = self.__path_checker(filename)
        self.__createfile()
        self.indlvl = 0
        self.newline = True
        self.open = False

    def __path_checker(self, filename: str) -> str:
        dirpath = Path(self.SAVEPATH)
        if not dirpath.exists():
            raise FileNotFoundError(self.SAVEPATH)

        if '.' not in filename:
            filename = filename + ".html"
            print(f"*** INFO: File format missing, saving as html-file.", file=sys.stderr)
            
        filepath = Path(self.SAVEPATH + filename)
        i = 1
        foo = filename.split(".")
        while filepath.is_file() and i <= self.MAXFILES:
            newname = f"({i}).".join(foo)
            filepath = Path(self.SAVEPATH + newname)
            i+=1

        if i > self.MAXFILES:
            print(f"*** WARNING: Overwriting file: {filepath}", file=sys.stderr)
   
        return filepath


    def __createfile(self):
        with open(self.filepath, 'w') as f:
            f.write("<!DOCTYPE html>\n")

    def __writeline(self, content: str):
        if self.indlvl < 0:
            raise IndentationError(content)

        with open(self.filepath, 'a') as f:
            if self.newline:
                indent = " " * self.TAB * self.indlvl
                f.write("\n" + indent + content)
            else:
                f.write(content)

    def handle_starttag(self, tag, attrs):
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
                print(f"*** INFO: </{tag}> indentation weirdness.", file=sys.stderr)
        
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
        datalines = data.split("\n")
        if "" in datalines:
            datalines.remove("")

        if datalines:
            if len(datalines) <= 1:
                self.newline = False
                self.__writeline(datalines[0])
            else:
                self.newline = True
                for line in datalines:
                    if line:
                        self.__writeline(line)

    def handle_comment(self, data):
        self.newline = True
        self.__writeline(f"<!--{data}-->")


if __name__ == "__main__":
    testdoc = "./tests/html_test_doc.html"
    newfile = "pretty.html"

    parser = HTMLRearranger(newfile)
    with open(testdoc,'r') as f:
        html_doc = f.read()
    
    parser.feed(html_doc)
    parser.close()
    print('\N{goat}')