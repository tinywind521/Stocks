import csv


def dict2CSV(rows, path, headers):
    # headers = []
    # rows = [{}]

    with open(path, 'w') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(rows)
