import argparse
import locale
import os
import sys
from query import Query

if __name__ == "__main__":
    default_lang = locale.getdefaultlocale()[0][:2]

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True, help="Name or file to search")
    parser.add_argument("-c", "--count", type=int, default=1, help="Maximum number of files to download")
    parser.add_argument("-l", "--lang", default=default_lang, help="Language of the subtitles")

    args = parser.parse_args()

    name = args.file
    is_file = os.path.isfile(name)

    if is_file:
        name = os.path.basename(name)

    query = Query.parse(name, is_file=is_file)

    if not query:
        print("Could not parse the query")
        sys.exit(1)

    print(query)
