import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "0731b3ee-9561-447c-8262-2e5d043c1ca6"

def geocoding(location, key):
    while location == "":
        location = input("Ingrese la ubicación nuevamente: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?" 
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    
    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        
        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")
        
        if state and country:
            new_loc = f"{name}, {state}, {country}"
        elif state:
            new_loc = f"{name}, {country}"
        else:
            new_loc = name
        
        print("URL de la API de Geocodificación para " + new_loc + " (Tipo de Ubicación: " + value + ")\n" + url)
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print("Estado de la API de Geocodificación: " + str(json_status) + "\nMensaje de error: " + json_data["message"])
    return json_status, lat, lng, new_loc

def calculate_route(origin, destination, vehicle="car"):
    op = "&point=" + str(origin[1]) + "%2C" + str(origin[2])
    dp = "&point=" + str(destination[1]) + "%2C" + str(destination[2])
    paths_url = route_url + urllib.parse.urlencode({"key": key}) + op + dp + f"&vehicle={vehicle}"
    
    paths_status = requests.get(paths_url).status_code
    paths_data = requests.get(paths_url).json()

    if paths_status == 200:
        print("Estado de la API de Enrutamiento: " + str(paths_status) + "\nURL de la API de Enrutamiento:\n" + paths_url)
        print("=================================================")
        print(f"Indicaciones desde {origin[3]} hasta {destination[3]}")
        print("=================================================")

        distance_meters = paths_data["paths"][0]["distance"]
        distance_miles = distance_meters * 0.000621371
        distance_km = distance_meters / 1000

        print(f"Distancia Recorrida: {distance_miles:.2f} miles / {distance_km:.2f} km")

        travel_time_seconds = paths_data["paths"][0]["time"] / 1000
        travel_hours = int(travel_time_seconds / 3600)
        travel_minutes = int((travel_time_seconds % 3600) / 60)

        print(f"Duración del Viaje: {travel_hours:02d}:{travel_minutes:02d}")

        print("=================================================")
        for step in paths_data["paths"][0]["instructions"]:
            print(f"{step['text']} ({step['distance'] / 1000:.2f} km)")
        print("=================================================")

    else:
        print(f"Estado de la API de Enrutamiento: {paths_status}")
        print(f"Error al calcular la ruta desde {origin[3]} hasta {destination[3]}")

def main():
    print("Bienvenido al Sistema de Enrutamiento")

    while True:
        loc1 = input("Ubicación de Inicio (o 's' para salir): ").strip()
        if loc1.lower() == "s":
            break

        orig = geocoding(loc1, key)

        loc2 = input("Destino (o 's' para salir): ").strip()
        if loc2.lower() == "s":
            break

        dest = geocoding(loc2, key)

        print("=================================================")
        if orig[0] == 200 and dest[0] == 200:
            vehicle = input("Elija el tipo de transporte (car, bike, foot): ").strip().lower()
            calculate_route(orig, dest, vehicle)
        print("=================================================")

if __name__ == "__main__":
    main()
