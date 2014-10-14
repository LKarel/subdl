import argparse
import locale
import sys
from query import Query

if __name__ == "__main__":
    default_lang = locale.getdefaultlocale()[0][:2]

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True, help="Name or file to search")
    parser.add_argument("-c", "--count", type=int, default=1, help="Maximum number of files to download")
    parser.add_argument("-l", "--lang", default=default_lang, help="Language of the subtitles")

    args = parser.parse_args()
    query = None

    if False:
        # If query is file, extract the query info from there
        pass
    else:
        query = Query.parse(args.file)

    print(query.name)
