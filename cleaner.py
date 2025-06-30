""" Parse and clean up html code 

run demo:
cleaner.py --demo
or
cleaner.py -f "./demo/sourceA.html"

run program:
cleaner.py -f "./inputfile.html" -o "./outputfile.html"

-f: relative path to input file
-o: relative path to output file (optional)
    if no output is specified, the new file is created in running directory
    as "new_inputfilename.html"
"""

from parsers.html_cleaner import HTMLCleaner


def _argparser(*args) -> list:
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

def _demo():
    demoA = ["./demo/sourceA.html", "./demo/demoA.html"]
    demoB = ["./demo/sourceB.html", "./demo/demoB.html"]
    cleanup(*demoA)
    cleanup(*demoB)


def cleanup(html_doc: str, newname: str = ""):
    """
    html_doc: path to html document
    newname: (optional) path to new file
    """
    if not newname:
        newname = "new_" + html_doc.split('/')[-1]

    with open(html_doc, 'r') as f:
        html_str = f.read()

    cleaner = HTMLCleaner(newname)
    cleaner.fill_the_void(html_str)
    cleaner.feed(html_str)
    cleaner.close()


if __name__ == "__main__":
    import sys

    args = _argparser(*sys.argv[1:])
    if args[0]:
        cleanup(*args)
    else:
        print("No input file. Try running: cleaner.py --help")

    print(f"\N{goat}")