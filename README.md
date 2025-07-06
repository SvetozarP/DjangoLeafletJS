# Django + LeafletJS - EV Charging Station Map

A simple Django web application demonstrating LeafletJS integration for displaying EV charging stations on an interactive map. Users can click on the map to find the nearest charging station and see the distance.

![Django + LeafletJS Demo](https://github.com/user-attachments/assets/6c31953b-8ae8-4a02-8a95-2e965a4856a6)

## Features

- **Interactive Map**: OpenStreetMap tiles powered by LeafletJS
- **EV Station Markers**: Display charging stations across Connecticut
- **Nearest Station Finder**: Click anywhere on the map to find the closest charging station
- **Distance Calculation**: Shows the distance to the nearest station in kilometers
- **Visual Route**: Draws a line between your clicked location and the nearest station

## Tech Stack

- **Backend**: Django 4.1.4
- **Frontend**: LeafletJS 1.9.4
- **Database**: SQLite3
- **Geospatial**: GeoPy for distance calculations
- **Data**: Connecticut EV charging stations CSV dataset

## Project Structure

```
├── core/                          # Main Django app
│   ├── management/commands/       # Custom management commands
│   │   └── load_stations.py       # CSV data loader
│   ├── templates/                 # HTML templates
│   │   ├── base.html             # Base template with LeafletJS
│   │   └── index.html            # Main map page
│   ├── models.py                 # EVChargingLocation model
│   ├── views.py                  # Map and API views
│   └── urls.py                   # URL routing
├── data/                         # Data files
│   └── EV_Charging_Stations.csv  # Connecticut EV stations dataset
├── folium_project/               # Django project settings
└── manage.py                     # Django management script
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### 1. Clone the Repository
```bash
git clone <repository-url>
cd django-leaflet-ev-map
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install django==4.1.4
pip install django-extensions
pip install geopy
```

### 4. Setup Database
```bash
python manage.py migrate
```

### 5. Load EV Station Data
```bash
python manage.py load_stations
```

### 6. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see the application.

## How It Works

### 1. Data Model
The `EVChargingLocation` model stores:
- Station name
- Latitude and longitude coordinates

### 2. Map Display
- LeafletJS renders an interactive map centered on Connecticut
- Station markers are loaded from the Django backend via JSON
- OpenStreetMap provides the base tile layer

### 3. Nearest Station Logic
When you click on the map:
1. JavaScript captures the click coordinates
2. AJAX request sent to `/get-nearest-station/` endpoint
3. Django calculates distances using GeoPy's geodesic function
4. Returns the nearest station coordinates and distance
5. A polyline is drawn showing the route
6. A popup displays the distance information

### Key Code Components

**Frontend (JavaScript)**:
```javascript
map.on('click', (event) => {
    let lat = event.latlng.lat;
    let longitude = event.latlng.lng;
    
    fetch(`/get-nearest-station?latitude=${lat}&longitude=${longitude}`)
        .then(response => response.json())
        .then(result => {
            // Draw line and show popup
        });
});
```

**Backend (Django)**:
```python
def nearest_station(request):
    user_location = (latitude, longitude)
    
    for station in EVChargingLocation.objects.all():
        distance = geodesic(user_location, station_location).km
        # Find minimum distance
    
    return JsonResponse({
        'coordinates': nearest_coordinates,
        'distance': min_distance
    })
```

## Data Source

The application uses Connecticut EV charging station data with the following key fields:
- **Station Name**: Name of the charging location
- **New Georeferenced Column**: Point coordinates in WKT format
- **Access information**: Hours, restrictions, etc.

## Customization

### Adding More Stations
1. Update the CSV file in `data/EV_Charging_Stations.csv`
2. Run `python manage.py load_stations` again

### Changing Map Center/Zoom
Edit the map initialization in `core/templates/index.html`:
```javascript
let map = L.map("map").setView([latitude, longitude], zoom_level)
```

### Styling the Map
Modify the map container CSS:
```css
#map {
    height: 600px;
    width: 600px;
}
```

## API Endpoints

- `GET /` - Main map page
- `GET /get-nearest-station/?latitude=X&longitude=Y` - Find nearest station

## Performance Notes

- Currently limited to first 100 stations for performance
- Distance calculations run on each request (could be optimized with spatial indexing)
- Frontend uses vanilla JavaScript (no additional frameworks)

## Future Enhancements

- [ ] Add station filtering by charging type/speed
- [ ] Implement route planning with turn-by-turn directions
- [ ] Add station details in popups (hours, pricing, etc.)
- [ ] Mobile-responsive design improvements
- [ ] Real-time availability data integration

## Contributing

This is a demonstration project following the BugBytes tutorial. Feel free to fork and enhance!

## License

This project is for educational purposes. Please check the data source licensing for the EV station dataset.
