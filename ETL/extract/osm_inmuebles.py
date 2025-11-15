import requests
import json
import os
import time
import random
from datetime import datetime
from requests.adapters import HTTPAdapter, Retry

# --- Configuration ---
# Valores por defecto. Pueden ser sobrescritos por variables de entorno o argumentos.
DEFAULT_CONFIG = {
    "OVERPASS_URL": "https://overpass-api.de/api/interpreter",
    "WDQS_URL": "https://query.wikidata.org/sparql",
    "WD_BATCH_SIZE": 50,
    "USER_AGENT": "ManusAI/1.0 (https://help.manus.im)",
}

OVERPASS_QUERY = """
[out:json][timeout:1800];
area["ISO3166-1"="ES"]->.es;
(
  // Criterio 1: amenity=place_of_worship + religion=christian + denomination=catholic
  node["amenity"="place_of_worship"]["religion"="christian"]["denomination"="catholic"](area.es);
  way ["amenity"="place_of_worship"]["religion"="christian"]["denomination"="catholic"](area.es);
  rel ["amenity"="place_of_worship"]["religion"="christian"]["denomination"="catholic"](area.es);

  // Criterio 2: building=* (tipos específicos) + denomination=catholic
  node["building"~"^(church|cathedral|chapel|monastery|convent|hermitage|basilica)$"]["denomination"="catholic"](area.es);
  way ["building"~"^(church|cathedral|chapel|monastery|convent|hermitage|basilica)$"]["denomination"="catholic"](area.es);
  rel ["building"~"^(church|cathedral|chapel|monastery|convent|hermitage|basilica)$"]["denomination"="catholic"](area.es);

  // Criterio 3: amenity=place_of_worship + religion=christian (sin denominación específica)
  node["amenity"="place_of_worship"]["religion"="christian"][!"denomination"](area.es);
  way ["amenity"="place_of_worship"]["religion"="christian"][!"denomination"](area.es);
  rel ["amenity"="place_of_worship"]["religion"="christian"][!"denomination"](area.es);

  // Criterio 4: building=* (tipos específicos) + religion=christian (sin denominación específica)
  node["building"~"^(church|cathedral|chapel|monastery|convent|hermitage|basilica)$"]["religion"="christian"][!"denomination"](area.es);
  way ["building"~"^(church|cathedral|chapel|monastery|convent|hermitage|basilica)$"]["religion"="christian"][!"denomination"](area.es);
  rel ["building"~"^(church|cathedral|chapel|monastery|convent|hermitage|basilica)$"]["religion"="christian"][!"denomination"](area.es);

  // Criterio 5: place_of_worship=* (elementos pequeños) + religion=christian
  node["place_of_worship"~"^(cross|wayside_shrine|lourdes_grotto)$"]["religion"="christian"](area.es);
  way ["place_of_worship"~"^(cross|wayside_shrine|lourdes_grotto)$"]["religion"="christian"](area.es);
  rel ["place_of_worship"~"^(cross|wayside_shrine|lourdes_grotto)$"]["religion"="christian"](area.es);
);
out tags center qt;
"""

def get_config():
    """Carga la configuración desde las variables de entorno o usa valores por defecto."""
    config = DEFAULT_CONFIG.copy()
    for key in config:
        config[key] = os.environ.get(key, config[key])
    return config

def extract_osm_data(config):
    """Extrae datos de Overpass API."""
    print("1. Querying Overpass API for Catholic buildings in Spain...")
    try:
        response = requests.post(config["OVERPASS_URL"], data=OVERPASS_QUERY, timeout=1800)
        response.raise_for_status()
        osm_data = response.json()
        osm_elements = osm_data.get('elements', [])
        print(f"   -> Received {len(osm_elements)} elements from OSM.")
        return osm_elements
    except requests.exceptions.RequestException as e:
        print(f"   -> Error querying Overpass: {e}")
        return []

def normalize_and_filter(osm_elements):
    """Normaliza y filtra los datos de OSM, extrayendo QIDs de Wikidata."""
    print("2. Normalizing and filtering OSM data...")
    normalized_items = []
    wikidata_qids = set()

    for e in osm_elements:
        t = e.get('tags', {})
        lat = e.get('center', {}).get('lat') or e.get('lat')
        lon = e.get('center', {}).get('lon') or e.get('lon')
        
        if not (isinstance(lat, (int, float)) and isinstance(lon, (int, float))):
            continue

        name = t.get('name')
        building = t.get('building')
        amenity = t.get('amenity')
        historic = t.get('historic')
        ruins = t.get('ruins') == 'yes'
        heritage = t.get('heritage')
        wd = t.get('wikidata')

        # Simplified filtering logic from n8n workflow
        keep_unnamed = (not name) and (historic or ruins or heritage or building in ['church', 'cathedral', 'chapel', 'monastery', 'convent', 'hermitage', 'basilica'])
        if not name and not keep_unnamed:
            continue
        if not amenity and building not in ['church', 'cathedral', 'chapel', 'monastery', 'convent', 'hermitage', 'basilica']:
            continue

        inferred = 'unknown'
        if building and building.lower() in ['church', 'cathedral', 'chapel', 'monastery', 'convent', 'hermitage', 'basilica']:
            inferred = building.lower()
        if name and any(word in name.lower() for word in ['basílica', 'basilica']):
            inferred = 'basilica'

        item_id = f"{e.get('type')}/{e.get('id')}"
        
        # Simplificamos la estructura de salida para facilitar la carga en SQLAlchemy
        item = {
            "osm_id": item_id,
            "name": name,
            "inferred_type": inferred,
            "denomination": t.get('denomination'),
            "diocese": t.get('diocese'),
            "operator": t.get('operator'),
            "wikidata_qid": wd,
            "heritage_status": heritage,
            "historic": historic,
            "ruins": ruins,
            "has_polygon": 'geometry' in e,
            "qa_flags": [], # Simplificado, se puede rellenar con la lógica de QA
            "source_refs": [{"type": "osm", "id": item_id, "version": e.get('version'), "timestamp": e.get('timestamp')}],
            "geom_wkt": f"POINT({lon} {lat})", # Usamos WKT para GeoAlchemy2
            "address_street": t.get('addr:street'),
            "address_city": t.get('addr:city') or t.get('addr:town') or t.get('addr:village'),
            "address_postcode": t.get('addr:postcode'),
        }

        if wd and wd.startswith('Q'):
            wikidata_qids.add(wd)
        
        normalized_items.append(item)

    print(f"   -> {len(normalized_items)} items after normalization and filtering.")
    print(f"   -> Found {len(wikidata_qids)} unique Wikidata QIDs for enrichment.")
    return normalized_items, wikidata_qids

def enrich_wikidata(normalized_items, wikidata_qids, config):
    """Enriquece los elementos con datos de Wikidata."""
    print("3. Enriching data with Wikidata...")
    
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    qids_list = list(wikidata_qids)
    wd_map = {}

    if not qids_list:
        print("   -> No QIDs to query.")
        return normalized_items

    # Batch processing
    for i in range(0, len(qids_list), config["WD_BATCH_SIZE"]):
        batch_qids = qids_list[i:i + config["WD_BATCH_SIZE"]]
        wd_items_str = " ".join([f"wd:{qid}" for qid in batch_qids])
        
        sparql_query = f"""
        SELECT ?item ?itemLabel ?inception ?heritage ?diocese ?coord ?commonsCat WHERE {{
          VALUES ?item {{ {wd_items_str} }}
          OPTIONAL {{ ?item wdt:P571 ?inception. }}
          OPTIONAL {{ ?item wdt:P1435 ?heritage. }}
          OPTIONAL {{ ?item wdt:P708 ?diocese. }}
          OPTIONAL {{ ?item wdt:P625 ?coord. }}
          OPTIONAL {{ ?item wdt:P373 ?commonsCat. }}
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language 'es,en'. }}
        }}
        """
        
        try:
            # Add a small random delay to respect rate limits
            time.sleep(random.uniform(1, 3))
            
            wd_response = session.post(
                config["WDQS_URL"], 
                data={'query': sparql_query}, 
                headers={'Accept': 'application/sparql-results+json', 'User-Agent': config["USER_AGENT"]},
                timeout=60
            )
            wd_response.raise_for_status()
            wd_bindings = wd_response.json().get('results', {}).get('bindings', [])
            
            for b in wd_bindings:
                qid = b['item']['value'].split('/')[-1]
                wd_map[qid] = {
                    'inception': b.get('inception', {}).get('value'),
                    'heritage': b.get('heritage', {}).get('value'),
                    'diocese_wd': b.get('diocese', {}).get('value'),
                    'commons': b.get('commonsCat', {}).get('value'),
                }
            print(f"   -> Batch {i//config['WD_BATCH_SIZE'] + 1}/{len(qids_list)//config['WD_BATCH_SIZE'] + 1} processed successfully.")
                    
        except requests.exceptions.RequestException as e:
            print(f"   -> Error querying Wikidata (Batch {i//config['WD_BATCH_SIZE'] + 1}): {e}")
            # Continue with the next batch

    # Merge WD data into normalized items
    for item in normalized_items:
        qid = item.get('wikidata_qid')
        if qid in wd_map:
            wd_data = wd_map[qid]
            item['inception'] = wd_data['inception']
            item['heritage_status'] = item['heritage_status'] or wd_data['heritage']
            item['diocese'] = item['diocese'] or wd_data['diocese_wd']
            item['commons_category'] = wd_data['commons']
            item['source_refs'].append({"type": "wd", "qid": qid})
            
    return normalized_items

def run_osm_etl():
    """Función principal para ejecutar el proceso ETL y devolver los datos listos para cargar."""
    config = get_config()
    
    # 1. Extract
    osm_elements = extract_osm_data(config)
    if not osm_elements:
        return []

    # 2. Transform (Normalize & Filter)
    normalized_items, wikidata_qids = normalize_and_filter(osm_elements)
    
    # 3. Enrich
    final_items = enrich_wikidata(normalized_items, wikidata_qids, config)
    
    return final_items

if __name__ == "__main__":
    # Ejemplo de uso independiente (no necesario para la integración)
    data = run_osm_etl()
    print(f"Total items ready for loading: {len(data)}")
    # Guardar en un archivo temporal para inspección si es necesario
    # with open("temp_output.json", "w", encoding="utf-8") as f:
    #     json.dump(data, f, ensure_ascii=False, indent=2)
