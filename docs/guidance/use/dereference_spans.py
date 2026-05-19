"""
Dereference OFDS spans from a JSON network package and write to GeoJSON.

Usage:
    python dereference_spans.py input.json output.geojson

Reads an OFDS network package JSON file and produces a GeoJSON FeatureCollection
of spans.

Requires: geopandas, shapely
"""

import json
import sys

import geopandas as gpd
from shapely.geometry import shape


def _wayleave_term(w):
    if w.get("term", {}).get("indefinite"):
        return "indefinite"
    years = w.get("term", {}).get("years")
    return f"{years} years" if years is not None else None


def _wayleave_cost(w):
    cost = w.get("cost", {}).get("perMetre", {})
    amount = cost.get("amount")
    currency = cost.get("currency")
    if amount is None or currency is None:
        return None
    recurrence = "annual" if w.get("cost", {}).get("recurring") else "one off"
    return f"{amount} {currency} per metre ({recurrence})"


def dereference_spans(input_path, output_path):
    with open(input_path) as f:
        data = json.load(f)

    networks = data.get("networks", [])

    rows = []
    for network in networks:
        nodes = {n["id"]: n for n in network.get("nodes", [])}
        wayleaves = {w["id"]: w for w in network.get("wayleaves", [])}

        for span in network.get("spans", []):
            si = span.get("supportingInfrastructure", {})
            start_id = span.get("start")
            end_id = span.get("end")
            start_name = nodes.get(start_id, {}).get("name", start_id)
            end_name = nodes.get(end_id, {}).get("name", end_id)

            span_wayleaves = [wayleaves[wid] for wid in span.get("wayleaves", []) if wid in wayleaves]

            rows.append(
                {
                    "geometry": shape(span["route"]) if span.get("route") else None,
                    "network": network.get("name"),
                    "identifier": span.get("id"),
                    "name": span.get("name"),
                    "phase": span.get("phase", {}).get("name"),
                    "status": span.get("status"),
                    "readyForServiceDate": span.get("readyForServiceDate"),
                    "start": f"{start_name} ({start_id})" if start_id else None,
                    "end": f"{end_name} ({end_id})" if end_id else None,
                    "directed": span.get("directed"),
                    "transmissionMediumOwner": span.get("transmissionMediumOwner", {}).get("name"),
                    "supplier": span.get("supplier", {}).get("name"),
                    "supportingInfrastructure__type": si.get("type"),
                    "supportingInfrastructure__description": si.get("description"),
                    "supportingInfrastructure__owner": si.get("owner", {}).get("name"),
                    "supportingInfrastructure__spareCapacity": si.get("spareCapacity"),
                    "codeployment": span.get("codeployment"),
                    "cableType": span.get("cableType"),
                    "darkFibre": span.get("darkFibre"),
                    "fibreType": span.get("fibreType"),
                    "fibreTypeDetails__fibreSubtype": span.get("fibreTypeDetails", {}).get("fibreSubtype"),
                    "fibreTypeDetails__description": span.get("fibreTypeDetails", {}).get("description"),
                    "fibreCount": span.get("fibreCount"),
                    "fibreLength": span.get("fibreLength"),
                    "capacity": span.get("capacity"),
                    "capacityDetails__description": span.get("capacityDetails", {}).get("description"),
                    "networkProviders": ";".join(
                        p.get("name", "") for p in span.get("networkProviders", [])
                    ),
                    "transmissionMedium": ";".join(span.get("transmissionMedium", [])),
                    "deployment": ";".join(span.get("deployment", [])),
                    "technologies": ";".join(span.get("technologies", [])),
                    "wayleave_grantor": ";".join(
                        w.get("grantor", {}).get("name", "") for w in span_wayleaves
                    ),
                    "wayleave_term": ";".join(
                        filter(None, (_wayleave_term(w) for w in span_wayleaves))
                    ),
                    "wayleave_cost": ";".join(
                        filter(None, (_wayleave_cost(w) for w in span_wayleaves))
                    ),
                    "countries": ";".join(span.get("countries", []))
                }
            )

    gdf = gpd.GeoDataFrame(rows)
    gdf.to_file(output_path, driver="GeoJSON")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input.json output.geojson")
        sys.exit(1)
    dereference_spans(sys.argv[1], sys.argv[2])
