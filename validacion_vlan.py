vlan_input = input("Por favor, ingrese el número de VLAN: ")

try:
    vlan = int(vlan_input)
    
    if 1 <= vlan <= 1005:
        print(f"La VLAN {vlan} corresponde a un rango normal de VLAN.")
    elif 1006 <= vlan <= 4094:
        print(f"La VLAN {vlan} corresponde a un rango extendido de VLAN.")
    else:
        print(f"El número {vlan} no corresponde a una VLAN válida (es un rango reservado o inexistente).")
        
except ValueError:
    print("Error: Debe ingresar un número entero.")