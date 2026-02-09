---
file_format: mystnb
---

# Leaflet example

This page demonstrates how to use Python, Folium and Leaflet to visualise the example OFDS JSON data.

```{tip}
Download this page as an executable Jupyter Notebook:  {nb-download}`leaflet.ipynb`.
```

```{seealso}
To learn how to convert OFDS data to GeoJSON format and visualise it in Folium (Leaflet), see [How to convert OFDS data to GeoJSON format](geojson).
```

## Get the data

```{code-cell}
import json
import folium
import requests

r = requests.get("https://raw.githubusercontent.com/Open-Telecoms-Data/open-fibre-data-standard/refs/heads/0.3/examples/json/network-package.json")
data = r.json()
network = data['networks'][0]
```

## Create map and add features

```{code-cell}
# Create map
m = folium.Map(location=[6.4363794,-1.547332], zoom_start=8)

## Add nodes
for node in network["nodes"]:
  folium.CircleMarker(
      # Reverse coordinate ordering
      location=node["location"]["coordinates"][::-1],
      radius=5,
      # Style based on accessPoint attribute value
      color="blue" if node.get("accessPoint") else "red",
      fill=True,
      # Create popup with attribute values
      popup=f"Name: {node["name"]}<br><br>Status: {node["status"]}<br><br>Access point: {node["accessPoint"]}"
  ).add_to(m)

## Add spans
for span in network["spans"]:
  folium.PolyLine(
      locations=[coordinates[::-1] for coordinates in span["route"]["coordinates"]],
      popup=f"Name: {span["name"]}<br><br>Status: {span["status"]}"
  ).add_to(m)
```

## Display map

```{code-cell}
m
```
