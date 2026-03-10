import random

print("🎮 POGODI BROJ 🎮")

ime = input("Kako se zoves? ")
print("Srecno,", ime)

tajni_broj = random.randint(1, 10)
pokusaji = 3

while pokusaji > 0:
    print("Imas", pokusaji, "pokusaja")
    pokusaj = int(input("Unesi broj: "))

    if pokusaj == tajni_broj:
        print("🎉 BRAVO,", ime, "POGODIO SI!")
        break
    else:
        print("❌ Pogresan broj")
        if(pokusaj > tajni_broj):
            print("Pokusaj manji broj")
        else:
            print("Pokusaj veci broj")
        pokusaji = pokusaji - 1

if pokusaji == 0:
    print("😢 Izgubio si. Broj je bio:", tajni_broj)
