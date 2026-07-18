import requests

api_key = "36412a71-be61-4050-895d-d6d4e42059d4" 

def obtener_coordenadas(ciudad):
    """Convierte el nombre de la ciudad en latitud y longitud."""
    url = f"https://graphhopper.com/api/1/geocode?q={ciudad}&key={api_key}"
    respuesta = requests.get(url)
    datos = respuesta.json()
    
    if datos.get("hits"):
        lat = datos["hits"][0]["point"]["lat"]
        lng = datos["hits"][0]["point"]["lng"]
        return lat, lng
    return None, None

while True:
    print("\n" + "="*50)
    print("PLANIFICADOR DE RUTAS PARA EXAMEN DEVNET")
    print("Para salir de la aplicación, ingrese la letra 'v'")
    print("="*50)
    
    origen = input("Ciudad de Origen: ")
    if origen.lower() == 'v':
        print("Saliendo del programa...")
        break
        
    destino = input("Ciudad de Destino: ")
    if destino.lower() == 'v':
        print("Saliendo del programa...")
        break

    print("\nTipos de medio de transporte disponibles:")
    print(" - car (Auto)")
    print(" - bike (Bicicleta)")
    print(" - foot (A pie)")
    
    vehiculo = input("Ingrese el medio de transporte a utilizar: ")
    if vehiculo.lower() == 'v':
        print("Saliendo del programa...")
        break

    if vehiculo not in ['car', 'bike', 'foot']:
        print("Medio de transporte no válido. Se utilizará 'car' por defecto.")
        vehiculo = 'car'

    lat_origen, lng_origen = obtener_coordenadas(origen)
    lat_destino, lng_destino = obtener_coordenadas(destino)

    if not lat_origen or not lat_destino:
        print("\n❌ Error: No se pudo encontrar una de las ciudades. Intente de nuevo.")
        continue

    url_ruta = f"https://graphhopper.com/api/1/route?point={lat_origen},{lng_origen}&point={lat_destino},{lng_destino}&vehicle={vehiculo}&locale=es&instructions=true&key={api_key}"
    
    respuesta_ruta = requests.get(url_ruta)
    datos_ruta = respuesta_ruta.json()

    if "paths" in datos_ruta:
        ruta = datos_ruta["paths"][0]
        distancia_metros = ruta["distance"]
        tiempo_milisegundos = ruta["time"]
        
        distancia_km = distancia_metros / 1000
        distancia_millas = distancia_km * 0.621371
        
        segundos_tot = int(tiempo_milisegundos / 1000)
        horas = segundos_tot // 3600
        minutos = (segundos_tot % 3600) // 60
        segundos = segundos_tot % 60
        
        print("\n" + "-"*40)
        print("RESUMEN DEL VIAJE")
        print("-"*40)
        print(f"Ruta       : {origen.title()} -> {destino.title()}")
        print(f"Transporte : {vehiculo}")
        print(f"Distancia  : {distancia_km:.2f} kilómetros ({distancia_millas:.2f} millas)")
        print(f"Duración   : {horas:02d} horas, {minutos:02d} minutos, {segundos:02d} segundos")
        
        print("\n" + "-"*40)
        print("NARRATIVA DEL VIAJE (Indicaciones)")
        print("-"*40)
        
        instrucciones = ruta["instructions"]
        for paso in instrucciones:
            distancia_tramo = paso['distance'] / 1000
            print(f" {paso['text']} ({distancia_tramo:.2f} km)")
            
    else:
        print("\n❌ No se pudo calcular una ruta terrestre entre ambas ciudades con el vehículo seleccionado.")