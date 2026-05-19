"""
Dereference OFDS nodes from a JSON network package and write to GeoJSON.

Usage:
    python dereference_nodes.py input.json output.geojson

Reads an OFDS network package JSON file and produces a GeoJSON FeatureCollection
of nodes.

Requires: geopandas, shapely
"""

import json
import sys

import geopandas as gpd
from shapely.geometry import shape


def dereference_nodes(input_path, output_path):
    with open(input_path) as f:
        data = json.load(f)

    networks = data.get("networks", [])

    rows = []
    for network in networks:
        for node in network.get("nodes", []):
            address = node.get("address", {})
            si = node.get("supportingInfrastructure", {})

            rows.append(
                {
                    "geometry": shape(node["location"]) if node.get("location") else None,
                    "network": network.get("name"),
                    "identifier": node.get("id"),
                    "name": node.get("name"),
                    "phase": node.get("phase", {}).get("name"),
                    "status": node.get("status"),
                    "address": ", ".join(
                        filter(
                            None,
                            [
                                address.get("streetAddress"),
                                address.get("locality"),
                                address.get("region"),
                                address.get("postalCode"),
                                address.get("country"),
                            ],
                        )
                    ),
                    "type": ";".join(node.get("type", [])),
                    "supportingInfrastructure__type": si.get("type"),
                    "supportingInfrastructure__description": si.get("description"),
                    "supportingInfrastructure__owner": si.get("owner", {}).get("name"),
                    "supportingInfrastructure__spareCapacity": si.get("spareCapacity"),
                    "accessPoint": node.get("accessPoint"),
                    "power": node.get("power"),
                    "technologies": ";".join(node.get("technologies", [])),
                    "transmissionMediumOwner": node.get("transmissionMediumOwner", {}).get("name"),
                    "networkProviders": ";".join(
                        p.get("name", "") for p in node.get("networkProviders", [])
                    ),
                    "internationalConnections": ";".join(
                        c.get("country", "") for c in node.get("internationalConnections", [])
                    ),
                }
            )

    gdf = gpd.GeoDataFrame(rows)
    gdf.to_file(output_path, driver="GeoJSON")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input.json output.geojson")
        sys.exit(1)
    dereference_nodes(sys.argv[1], sys.argv[2])
