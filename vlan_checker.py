    # vlan_checker.py

vlan = int(input("Ingrese el número de VLAN: "))

if 1 <= vlan <= 1005:
    print("VLAN dentro del rango normal (1-1005).")
elif 1006 <= vlan <= 4094:
    print("VLAN dentro del rango extendido (1006-4094).")
else:
    print("VLAN fuera de rango válido (1-4094).")
