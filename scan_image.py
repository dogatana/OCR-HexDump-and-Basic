import json
import os.path
import sys

reader = None


def main(files):
    for file in files:
        if not os.path.exists(file):
            print(f"*** {file} not found")
            continue
        result = scan_file(file)
        with open(json_filename(file), "w") as fp:
            json.dump(result, fp)
        print(f"{file}: write {json_filename(file)}")


def scan_file(file):
    results = get_reader().readtext(file)

    ret = []
    for result in results:
        # ex ([[293, 56], [557, 56], [557, 231], [293, 231]], 'VO', 0.6040728609898799)
        ret.append(
            {
                "points": [[int(x), int(y)] for x, y in result[0]],
                "str": result[1],
                "level": float(result[2]),
            }
        )
    return ret


def get_reader():
    import easyocr

    global reader
    if reader is None:
        reader = easyocr.Reader(["en"])
    return reader


def json_filename(file):
    base, _ = os.path.splitext(file)
    return base + ".json"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f"usage: py {os.path.basename(__file__)} file [file ...]")
        exit()
    main(sys.argv[1:])
