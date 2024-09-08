import string

hex_string = "abcdef0123456789"
with open("HexHex.txt", 'r') as f:
    lines = f.readlines()
    out = ""
    for line in lines:
        line = line.strip()

        line = line.replace("0x", "")
        line = ''.join(s for s in line if s in hex_string)

        # line = line.replace("\\x", "")
        # line = line.replace(";", "")
        # line = line.replace("%", "")
        # line = line.replace(",0x", "")
        # line = line.replace(",", "")
        # line = line.replace("\\", "")
        # line = line.replace("x", "")
        # line = line.replace("s", "")
        out += line


with open('asdf.txt', 'w') as f:
    asdf = ""
    c = []
    for i in range(0, len(out), 2):
        b = chr(int(out[i:i+2], 16))
        if b not in (string.printable):
            c.append(out[i:i+2])
    d = ''.join(c)
    e = []
    for i in range(1, len(d), 2):
        b = chr(int(d[i:i+2], 16))
        e.append(b)
    print(''.join(e))
    f.write(asdf)
