import re

exp = re.compile(
    '(?P<serial>\d+),(?P<second>\d*),(?P<timestamp>\d+),(?P<user>[^,]*),(?P<ip>[\d\.]+),"(?P<data>[^"]*)",(?P<third>[^,]*),(?P<fourth>\d*)\n',
    re.M)

data = open("divmod-wiki-replaced.csv").read()

seen = set()

for m in exp.finditer(data):
    d = m.groupdict()
    f = open("dumped/%03d.txt" % int(d["serial"]), "wb")
    f.write(d["data"])
    f.close()
