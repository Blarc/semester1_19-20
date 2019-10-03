t = "Danes je dezeven dan."
s = t.split(" ")
print(s)

for i in range(len(s)):
    b = s[i]

for b in s:
    print()

# range(4) = [0,1,2,3]

bes = []
poj = []

# O(n^2)
for b in s:
    if b in bes:
        i = bes.index(b)
        poj[i] = poj[i] + 1
    else:
        bes.append(b)
        poj.append(1)

for i in range(len(bes)):
    b = bes[i]
    p = poj[i]
    print(b, p)

for b, p in zip(bes, poj):
    print(b, p)

# O(n)
pojd = {}
for b in s:
    if b in bes:
        pojd[b] = pojd[b] + 1
    else:
        pojd[b] = 1

for b, p in pojd.items():
    print(b, p)

# [::2]

# s[2::]

# s[:-1]

# s[2:-1:2] vsak drugi

# s[::2]

from collections import defaultdict

pojdi = defaultdict(int)
for b in s:
    pojdi[b] = pojdi[b] + 1

# pojdij = Counter(s)

imena = ["Jože", "Anica", "Micka"]
priimki = ["Štebih", "Horvat", "Škobrne"]

rez = []
i = 0
for a, b in zip(imena, priimki):
    i += 1
    s = str(i) + ". " + a + " " + b

for i, (a, b) in enumerate(zip(imena, priimki)):
    s = str(i + 1) + ". " + a + " " + b
    rez.append(s)

# rezultat zipa je generator

rez = [str(i + 1) + ". " + a + " " + b for i, (a, b) in enumerate(zip(imena, priimki))]
rez_generator = (str(i + 1) + ". " + a + " " + b for i, (a, b) in
                 enumerate(zip(imena, priimki)))  # vcasih lahko tako dobimo generator

sorted(rez)


# hočemo posortirat po priimkih

def t(arg):
    ba = arg.split(" ")
    ba = ba[::-1]  # obrne seznam
    return " ".join(ba)


k = []
k = [t(a) for a in k]
k = sorted(k)
k = [t(a) for a in k]  # slucajno enako

sorted(k, key=t)
