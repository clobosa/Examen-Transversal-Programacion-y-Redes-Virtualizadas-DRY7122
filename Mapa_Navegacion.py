import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
clave = "X98w72XZreYvV2bgI7g3wC4SfaI62xPJ"

while True:
    print("\n--- Consulta de Ruta ---")
    origen = input("Ciudad de origen (o 's' para salir): ")
    if origen.lower() == "s":
        print("¡Hasta pronto!")
        break

    tipo_vehiculo = input("Tipo de vehículo (auto, camioneta, moto, etc.; o 's' para salir): ")
    if tipo_vehiculo.lower() == "s":
        print("¡Hasta pronto!")
        break

    destino = input("Ciudad de destino (o 's' para salir): ")
    if destino.lower() == "s":
        print("¡Hasta pronto!")
        break

    url = main_api + urllib.parse.urlencode({
        "key": clave,
        "from": origen,
        "to": destino
    })

    try:
        response = requests.get(url)
        json_data = response.json()
    except Exception as e:
        print("❌ Error al conectar con la API:", str(e))
        continue

    status_code = json_data["info"]["statuscode"]
    if status_code != 0:
        print("❌ No se pudo calcular la ruta:", json_data["info"]["messages"])
        continue

    route = json_data["route"]
    distancia_km = route["distance"] * 1.60934
    duracion = route["formattedTime"]

    print("\n✅ Ruta encontrada:")
    print(f"Desde: {origen}")
    print(f"Hasta: {destino}")
    print(f"Tipo de vehículo: {tipo_vehiculo}")
    print(f"Distancia: {distancia_km:.2f} km")
    print(f"Duración estimada: {duracion}")

    if "fuelUsed" in route:
        combustible_litros = route["fuelUsed"] * 3.78541
        print(f"Combustible requerido: {combustible_litros:.2f} litros\n")
    else:
        print("Combustible requerido: No disponible\n")

    print("📌 Instrucciones del viaje:")
    for paso in route["legs"][0]["maneuvers"]:
        narrativa = paso["narrative"]
        distancia_paso = paso["distance"] * 1.60934
        print(f" - {narrativa} ({distancia_paso:.2f} km)")

    print("\n-------------------------------------------")

