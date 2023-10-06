import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        lines = f.readlines()
    percent = float(lines[6].split()[4][1:-1]) # maaagic constants)
    if percent > 90:
        print(f"GOOD")
    else:
        print(f"BAD")