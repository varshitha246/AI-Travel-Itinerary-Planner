from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random
import os

app = Flask(__name__)
CORS(app)

# API Keys


OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")

OPENWEATHER_GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"
OPENWEATHER_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
GEOAPIFY_PLACES_URL = "https://api.geoapify.com/v2/places"
SPOONACULAR_SEARCH_URL = "https://api.spoonacular.com/recipes/complexSearch"
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"


def safe_get_json(url, params=None, timeout=12):
    try:
        response = requests.get(
            url,
            params=params,
            timeout=timeout,
            headers={"User-Agent": "AI-Travel-Planner/1.0 (contact: local-app)"},
        )
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None


def unique_by(items, key_func):
    seen = set()
    output = []
    for item in items:
        key = key_func(item)
        if key not in seen:
            seen.add(key)
            output.append(item)
    return output


def search_cities(query, limit=8):
    query = (query or "").strip()
    if not query:
        return []

    data = safe_get_json(
        OPENWEATHER_GEO_URL,
        params={"q": query, "limit": max(limit, 1), "appid": OPENWEATHER_API_KEY},
    )
    if not data:
        return []

    cities = []
    for item in data:
        city = item.get("name", "").strip()
        state = (item.get("state") or "").strip()
        country = (item.get("country") or "").strip()
        lat = item.get("lat")
        lon = item.get("lon")
        if not city or lat is None or lon is None:
            continue
        display_name = f"{city}, {country}" if not state else f"{city}, {state}, {country}"
        cities.append(
            {
                "city": city,
                "state": state,
                "country": country,
                "lat": lat,
                "lon": lon,
                "display_name": display_name,
            }
        )

    return unique_by(cities, lambda x: x["display_name"])[:limit]


def resolve_city(query):
    matches = search_cities(query, limit=1)
    if matches:
        return matches[0]

    # Last fallback when geocoding fails
    raw = (query or "").strip() or "Paris"
    return {
        "city": raw,
        "state": "",
        "country": "",
        "lat": None,
        "lon": None,
        "display_name": raw,
    }


def get_weather(lat, lon, city_name):
    if lat is not None and lon is not None:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
        }
    else:
        params = {
            "q": city_name,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
        }

    data = safe_get_json(OPENWEATHER_WEATHER_URL, params=params)
    if data:
        main = data.get("main", {})
        weather_list = data.get("weather", [])
        conditions = "Clear"
        if weather_list and isinstance(weather_list, list):
            conditions = weather_list[0].get("description", "Clear")
        return {
            "temperature": round(main.get("temp", 25), 1),
            "conditions": conditions,
            "humidity": main.get("humidity", 60),
        }

    return {
        "temperature": round(random.uniform(15, 32), 1),
        "conditions": random.choice(["Sunny", "Partly Cloudy", "Clear Sky", "Light Rain"]),
        "humidity": random.randint(35, 85),
    }


def map_interest_to_categories(interests):
    category_map = {
        "Adventure": ["entertainment", "leisure.park"],
        "Culture": ["tourism.sights", "entertainment.museum", "heritage"],
        "Nature": ["natural", "leisure.park", "national_park"],
        "Shopping": ["commercial.marketplace", "commercial.shopping_mall"],
        "History": ["heritage", "tourism.sights", "entertainment.museum"],
        "Food": ["catering.restaurant", "catering.cafe"],
        "Relaxation": ["leisure.park", "natural", "beach"],
    }

    selected = []
    for interest in interests or []:
        selected.extend(category_map.get(interest, []))
    if not selected:
        selected = ["tourism.sights", "entertainment.museum", "leisure.park", "natural"]

    return unique_by(selected, lambda x: x)


def _fetch_geoapify_places(lat, lon, categories, limit=20, radius_m=7000):
    if lat is None or lon is None:
        return []

    params = {
        "categories": ",".join(categories),
        "filter": f"circle:{lon},{lat},{radius_m}",
        "bias": f"proximity:{lon},{lat}",
        "limit": limit,
        "apiKey": GEOAPIFY_API_KEY,
    }
    data = safe_get_json(GEOAPIFY_PLACES_URL, params=params)
    if not data:
        return []

    features = data.get("features", [])
    output = []
    for feature in features:
        props = feature.get("properties", {})
        name = (props.get("name") or "").strip()
        if not name:
            continue
        category_list = props.get("categories", [])
        category_name = category_list[0] if category_list else "Attraction"
        output.append(
            {
                "name": name,
                "categories": {"name": category_name.replace(".", " ").title()},
                "address_line2": props.get("address_line2") or props.get("city") or "",
                "formatted": props.get("formatted") or "",
                "distance_m": props.get("distance", 0),
                "place_id": props.get("place_id", ""),
            }
        )
    return output


def get_places(lat, lon, interests=None):
    categories = map_interest_to_categories(interests)
    attractions = _fetch_geoapify_places(lat, lon, categories, limit=24, radius_m=10000)
    attractions = unique_by(attractions, lambda x: x["name"])
    attractions.sort(key=lambda x: x.get("distance_m", 0))
    return attractions[:12]


def get_restaurants(lat, lon, budget="Standard"):
    categories = ["catering.restaurant", "catering.fast_food", "catering.cafe"]
    restaurants = _fetch_geoapify_places(lat, lon, categories, limit=24, radius_m=8000)
    restaurants = unique_by(restaurants, lambda x: x["name"])
    restaurants.sort(key=lambda x: x.get("distance_m", 0))

    if budget == "Economy":
        price_choices = ["$", "$$", "$"]
    elif budget == "Luxury":
        price_choices = ["$$$", "$$$$", "$$$"]
    else:
        price_choices = ["$$", "$$$", "$$"]

    output = []
    for r in restaurants[:8]:
        cat = r.get("categories", {}).get("name", "Restaurant")
        output.append(
            {
                "name": r["name"],
                "address": r.get("formatted") or r.get("address_line2") or "",
                "address_line2": r.get("address_line2") or "",
                "price_range": random.choice(price_choices),
                "specialty": cat,
                "categories": {"name": cat},
                "rating": round(random.uniform(3.7, 4.9), 1),
            }
        )
    return output


def generate_local_specialties(city, country):
    seed_text = f"{city}-{country}".lower()
    pool = [
        "Street Food",
        "Local Bakery",
        "Regional Stew",
        "Traditional BBQ",
        "Seafood Platter",
        "Artisan Coffee",
        "Spiced Rice Dishes",
        "Classic Desserts",
        "Farm-to-Table Cuisine",
        "Night Market Snacks",
    ]
    random.seed(seed_text)
    picks = random.sample(pool, 5)
    random.seed()
    return picks


def get_spoonacular_food(city, country="", number=8):
    query_parts = [city, country, "local cuisine"]
    query = " ".join([x for x in query_parts if x]).strip()
    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "query": query,
        "number": number,
        "instructionsRequired": False,
        "addRecipeInformation": False,
    }
    data = safe_get_json(SPOONACULAR_SEARCH_URL, params=params, timeout=15)
    if not data:
        return []

    results = data.get("results", [])
    foods = []
    for item in results:
        title = (item.get("title") or "").strip()
        image = (item.get("image") or "").strip()
        if not title:
            continue
        foods.append({"name": title, "image": image})
    return foods


def get_wikipedia_thumbnail(query, size=1000):
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": query,
        "gsrlimit": 1,
        "prop": "pageimages",
        "piprop": "thumbnail",
        "pithumbsize": size,
    }
    data = safe_get_json(WIKIPEDIA_API_URL, params=params, timeout=12)
    if not data:
        return ""

    pages = (data.get("query") or {}).get("pages") or {}
    for _, page in pages.items():
        thumb = (page.get("thumbnail") or {}).get("source") or ""
        if thumb:
            return thumb
    return ""


def build_location_images(city, attractions, limit=6):
    names = [a.get("name", "").strip() for a in (attractions or []) if a.get("name")]
    queries = names[:limit]
    if city:
        queries.insert(0, f"{city} skyline landmark")

    urls = []
    for q in queries:
        img = get_wikipedia_thumbnail(q, size=1200)
        if img:
            urls.append(img)

    if not urls:
        urls = [
            "https://images.pexels.com/photos/346885/pexels-photo-346885.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/3155666/pexels-photo-3155666.jpeg?auto=compress&cs=tinysrgb&w=1200",
        ]
    return unique_by(urls, lambda x: x)[:limit]


def generate_daily_activities(day, city, attractions, restaurants, interests):
    themes = ["Landmarks & History", "Culture & Arts", "Food & Markets", "Nature & Relaxation", "Adventure & Exploration"]
    theme = themes[(day - 1) % len(themes)]

    if attractions:
        attraction = attractions[min((day - 1) * 2, len(attractions) - 1)]
        attraction_name = attraction.get("name", f"Top attraction in {city}")
        attraction_category = attraction.get("categories", {}).get("name", "attraction").lower()
        morning = f"Start your day at {attraction_name}, a must-visit {attraction_category}"
        afternoon = f"Explore nearby highlights around {attraction_name} and enjoy local city life"
    else:
        morning = f"Explore the cultural center of {city} and discover iconic local spots"
        afternoon = f"Take a guided walk through neighborhoods and hidden gems in {city}"

    if restaurants:
        lunch_restaurant = restaurants[(day - 1) % len(restaurants)]
        lunch = f"Lunch at {lunch_restaurant.get('name', 'a local restaurant')} with regional flavors"
    else:
        lunch = "Enjoy local cuisine at a highly-rated neighborhood restaurant"

    if "Food" in (interests or []):
        evening = "Join an evening food trail and try signature dishes across popular local eateries"
    elif "Adventure" in (interests or []):
        evening = "Experience adventure activities and end the day at a vibrant nightlife district"
    else:
        evening = f"Relax with a scenic evening walk and cultural performances in {city}"

    return {
        "day": day,
        "morning": f"{morning} ({theme})",
        "lunch": lunch,
        "afternoon": afternoon,
        "evening": evening,
    }


@app.route("/city-search", methods=["GET"])
def city_search():
    query = request.args.get("q", "").strip()
    limit = int(request.args.get("limit", 8))
    return jsonify({"query": query, "cities": search_cities(query, limit=limit)})


@app.route("/itinerary", methods=["POST"])
def generate_itinerary():
    data = request.json or {}
    input_city = (data.get("city", "") or "").strip()
    days = int(data.get("days", 3))
    days = max(1, min(days, 30))
    budget = data.get("budget", "Standard")
    interests = data.get("interests", ["Culture", "Food"])

    resolved = resolve_city(input_city)
    city = resolved["city"]
    country = resolved["country"]
    lat = resolved["lat"]
    lon = resolved["lon"]

    weather = get_weather(lat, lon, city)
    restaurants = get_restaurants(lat, lon, budget)
    attractions = get_places(lat, lon, interests)
    spoonacular_food = get_spoonacular_food(city, country, number=8)

    if attractions:
        for a in attractions:
            q = a.get("name") or city
            a["image"] = get_wikipedia_thumbnail(q, size=1000) or "https://images.pexels.com/photos/346885/pexels-photo-346885.jpeg?auto=compress&cs=tinysrgb&w=1000"

    itinerary = []
    for day in range(1, days + 1):
        itinerary.append(generate_daily_activities(day, city, attractions, restaurants, interests))

    location_bits = [city]
    if resolved.get("state"):
        location_bits.append(resolved["state"])
    if country:
        location_bits.append(country)
    location_label = ", ".join(location_bits)

    description = (
        f"{location_label} is a vibrant destination with unique neighborhoods, local cuisine, "
        f"and attractions tailored to your interests."
    )

    resolved_display_name = resolved.get("display_name", city)
    normalized_input = (input_city or "").strip().lower()
    normalized_city = city.lower()
    normalized_display = resolved_display_name.lower()

    response = {
        "input_city": input_city or city,
        "resolved_city": city,
        "resolved_display_name": resolved_display_name,
        "city_corrected": bool(
            input_city and normalized_input not in {normalized_city, normalized_display}
        ),
        "coordinates": {"lat": lat, "lon": lon},
        "country": country,
        "weather": weather,
        "description": description,
        "restaurants": restaurants,
        "attractions": attractions,
        "itinerary": itinerary,
        "local_specialties": [f["name"] for f in spoonacular_food[:5]] or generate_local_specialties(city, country),
        "food_images": [f["image"] for f in spoonacular_food if f.get("image")][:8] or [
            "https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/958545/pexels-photo-958545.jpeg?auto=compress&cs=tinysrgb&w=1200",
        ],
        "location_images": build_location_images(city, attractions, limit=8),
        "famous_landmarks": [a.get("name") for a in attractions[:5] if a.get("name")] or [f"Popular spots in {city}"],
    }
    return jsonify(response)


@app.route("/test", methods=["GET"])
def test():
    return jsonify({"status": "Server is running!", "message": "Dynamic Travel Itinerary API"})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})


@app.route("/cities", methods=["GET"])
def cities_help():
    return jsonify({"message": "Use /city-search?q=<name> to search cities dynamically."})


if __name__ == "__main__":
    # Keep reloader off to avoid Windows watchdog race conditions and noisy restarts.
    app.run(debug=False, use_reloader=False, port=5000, host="0.0.0.0")
