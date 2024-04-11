import json


FILE = r'tmp/tmp.json'


if __name__ == "__main__":

    with open(FILE, 'r') as fp:
        data = json.load(fp)

    print(data)

    with open(FILE, 'w', newline='') as fp:
        json.dump(data, fp, indent=4)
