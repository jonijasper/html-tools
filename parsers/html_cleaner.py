import sys
from html.parser import HTMLParser
from pathlib import Path

from parsers.taglib import TagLib


class HTMLCleaner(HTMLParser):
    MAXFILES = 5    # try filename(n) replacement up to n=MAXFILES
    TAB = 2         # indentation size = " " * TAB
    SAVEPATH = "./"

    def __init__(self, filename: str = "clean.html"):
        HTMLParser.__init__(self)
        
        self.filepath = self.__path_checker(filename)
        self.voidtags = {}
        self.indlvl = 0
        self.script = False
        self.open = False
        self.newline = True

        self.__createfile()

    def __path_checker(self, filename: str) -> str:
        if '/' in filename:
            bar = filename.split('/')
            savepath = "/".join(bar[:-1]) + "/"
            filename = bar[-1]
        else:
            savepath = self.SAVEPATH

        if not Path(savepath).exists():
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
        else:
            self.warning(f"Saving new file as {filepath}")
   
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

    def __strip_attrs(self, attrs) -> str:
        attrlist = []
        for attr,value in attrs:
            if value:
                values = value.split()
                attrlist.append(f" {attr}=\"{" ".join(values)}\"")
            else:
                attrlist.append(f" {attr}=\"\"")

        return "".join(attrlist)

    def fill_the_void(self, content):
        """ run before feed() """
        voidparser = TagLib()
        voidparser.feed(content)
        tags = voidparser.get_voidlist()
        voidparser.close()

        self.voidtags = set(tags)

    # <tag>
    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.script = True

        if tag in self.voidtags:
            self.handle_startendtag(tag, attrs)
        else:
            attrstr = self.__strip_attrs(attrs)

            self.newline = True
            self.__writeline(f"<{tag}{attrstr}>")
            self.newline = False
            self.indlvl += 1
            self.open = True

    # <tag/>
    def handle_startendtag(self, tag, attrs):
        attrstr = self.__strip_attrs(attrs)

        self.newline = True
        self.__writeline(f"<{tag}{attrstr} />")
        self.open = False

    # > data </
    def handle_data(self, data):
        cleandata = []
        datalines = data.splitlines()
        for line in datalines:
            content = line.strip()
            if content:
                cleandata.append(line if self.script else content)

        if cleandata:
            self.newline = True
            for line in cleandata:
                self.__writeline(line)

    # </tag>
    def handle_endtag(self, tag):
        if tag == "script":
            self.script = False

        if tag in self.voidtags:
            return

        if self.indlvl > 0:
            self.indlvl -= 1
        else:
            pos = self.getpos()[0]
            self.warning(f"</{tag}> indentation weirdness, line {pos}")
        
        self.__writeline(f"</{tag}>")
        self.newline = True
        self.open = False

    # <!--comment-->
    def handle_comment(self, data):
        self.newline = True
        self.__writeline(f"<!--{data}-->")

    @staticmethod
    def warning(msg: str, level: str = "INFO"):
        if level == "INFO":
            stream = sys.stdout
        else:
            stream = sys.stderr

        print(f"*** {level}: {msg}", file=stream)


if __name__ == "__main__":
    print('*** \N{goat} Try running: cleaner.py --help')