""" Parse and clean up html code 

run demo:
main.py --demo
or
main.py -f "./demo/sourceA.html"

run program:
main.py -f "./inputfile.html" -o "./outputfile.html"

-f: relative path to input file
-o: relative path to output file (optional)
    if no output is specified, the new file is created in running directory
    as "new_inputfilename.html"
"""

import sys
from parsers.html_cleaner import HTMLCleaner
from parsers.taglib import TagLib


def argparser(*args) -> list:
    argdict = {"-f": None, "-o": None}

    if "-h" in args or "--help" in args:
        print(__doc__)
        exit()
    elif "--demo" in args:
        _demo()
        exit()
    else:
        for i, arg in enumerate(args):
            if arg in argdict:
                argdict[arg] = args[i+1]

    return list(argdict.values())

def cleanup(html_doc: str, newname: str = ""):
    with open(html_doc, 'r') as f:
            html_str = f.read()

    voidparser = TagLib()
    voidparser.feed(html_str)
    tags = voidparser.get_voidlist()
    voidparser.close()

    if not newname:
        newname = "new_" + html_doc.split('/')[-1]

    cleaner = HTMLCleaner(newname, tags)
    cleaner.feed(html_str)
    cleaner.close()

def _demo():
    demoA = ["./demo/sourceA.html", "./demo/demoA.html"]
    demoB = ["./demo/sourceB.html", "./demo/demoB.html"]
    cleanup(*demoA)
    cleanup(*demoB)


if __name__ == "__main__":
    args = argparser(*sys.argv[1:])
    if args[0]:
        cleanup(*args)
    else:
        print("No input file. Try running: main.py --help")

    print(f"\N{goat}")