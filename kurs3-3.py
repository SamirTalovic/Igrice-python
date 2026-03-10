poeni = 0

pitanja = [
    "Koliko je 3 + 3? ",
    "Koliko ima dana u nedelji? "
]

odgovori = [6,7]

for i in range(len(pitanja)):
    odgovor = int(input(pitanja[i]))

    if odgovor == odgovori[i]:
        print("Tacno!")
        poeni = poeni + 1
    else:
        print("Pogresno!")

print("Kraj kviza!")
print("Ukupno poena:", poeni)
