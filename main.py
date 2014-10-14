import sys
from query import Query

if __name__ == "__main__":
    query = None

    if len(sys.argv) < 2:
        print("Missing name argument")
        sys.exit(1)

    if False:
        # If query is file, extract the query info from there
        pass
    else:
        query = Query.parse(sys.argv[1])

    print(query.name)
