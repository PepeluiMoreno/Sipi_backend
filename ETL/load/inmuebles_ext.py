from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import WKTElement
from app.db.models.inmuebles import Inmueble, BaseModel
from ETL.extract.osm_inmuebles import run_osm_etl
import os

# Simulación de la configuración de la base de datos
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./test.db")

def load_inmuebles_to_db(data):
    """Carga los datos procesados en la base de datos SQLAlchemy."""
    
    engine = create_engine(DATABASE_URL)
    # Asegurarse de que la tabla existe (solo para el ejemplo)
    BaseModel.metadata.create_all(bind=engine) 
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    count = 0
    
    try:
        for item in data:
            # 1. Adaptar el diccionario a los campos del modelo Inmueble
            inmueble_data = {
                "osm_id": item.get("osm_id"),
                "name": item.get("name"),
                "inferred_type": item.get("inferred_type"),
                "denomination": item.get("denomination"),
                "diocese": item.get("diocese"),
                "operator": item.get("operator"),
                "wikidata_qid": item.get("wikidata_qid"),
                "inception": item.get("inception"),
                "commons_category": item.get("commons_category"),
                "heritage_status": item.get("heritage_status"),
                "historic": item.get("historic"),
                "ruins": item.get("ruins"),
                "has_polygon": item.get("has_polygon"),
                "qa_flags": item.get("qa_flags"),
                "source_refs": item.get("source_refs"),
                "address_street": item.get("address_street"),
                "address_city": item.get("address_city"),
                "address_postcode": item.get("address_postcode"),
                # Convertir WKT a objeto GeoAlchemy2
                "geom": WKTElement(item.get("geom_wkt"), srid=4326)
            }
            
            # 2. Comprobar si el inmueble ya existe (por osm_id)
            existing_inmueble = db.query(Inmueble).filter(Inmueble.osm_id == inmueble_data["osm_id"]).first()
            
            if existing_inmueble:
                # Actualizar (simulación de upsert)
                for key, value in inmueble_data.items():
                    setattr(existing_inmueble, key, value)
                db.add(existing_inmueble)
                print(f"   -> Updated Inmueble: {inmueble_data['osm_id']}")
            else:
                # Insertar
                new_inmueble = Inmueble(**inmueble_data)
                db.add(new_inmueble)
                print(f"   -> Inserted Inmueble: {inmueble_data['osm_id']}")
            
            count += 1
            
        db.commit()
        print(f"Successfully loaded/updated {count} records.")
        
    except Exception as e:
        db.rollback()
        print(f"An error occurred during loading: {e}")
    finally:
        db.close()

def run_load_workflow():
    """Flujo de trabajo completo: Extraer -> Cargar."""
    print("--- Starting Full ETL Workflow: Extract and Load ---")
    
    # 1. Extraer y transformar los datos
    data_to_load = run_osm_etl()
    
    if data_to_load:
        # 2. Cargar los datos en la base de datos
        load_inmuebles_to_db(data_to_load)
    else:
        print("No data to load.")

if __name__ == "__main__":
    # Para ejecutar este script, necesitará configurar su entorno con SQLAlchemy y GeoAlchemy2
    # y asegurarse de que la base de datos esté disponible.
    # Ejemplo de ejecución: python ETL/load/inmuebles_ext.py
    run_load_workflow()
