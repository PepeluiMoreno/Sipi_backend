from __future__ import annotations

from sqlalchemy.dialects.postgresql import JSONB
from .base import Base, UUIDPKMixin, AuditMixin

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.ext.mutable import MutableDict

from .base import Base, UUIDPKMixin, AuditMixin

class InmuebleOSMExt(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmuebles_osm_ext"

    # 1:1 con inmueble
    inmueble_id = Column(String(36), ForeignKey("inmuebles.id"), nullable=False, unique=True)

    osm_id = Column(String(50), nullable=True)       # id numérico en texto
    osm_type = Column(String(10), nullable=True)     # node/way/relation
    version = Column(Integer, nullable=True)
    source_updated_at = Column(DateTime, nullable=True)

    # JSONB mutables (sin anotaciones de tipo Python)
    tags = Column(MutableDict.as_mutable(JSONB), nullable=True)
    raw = Column(MutableDict.as_mutable(JSONB), nullable=True)

    inmueble = relationship("Inmueble", backref="osm_ext", uselist=False)

class InmuebleWDExt(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmuebles_wd_ext"

    # 1:1 con inmueble
    inmueble_id = Column(String(36), ForeignKey("inmuebles.id"), nullable=False, unique=True)

    wikidata_qid = Column(String(32), nullable=True, unique=True)
    commons_category = Column(String(255), nullable=True)
    source_updated_at = Column(DateTime, nullable=True)

    claims = Column(MutableDict.as_mutable(JSONB), nullable=True)
    sitelinks = Column(MutableDict.as_mutable(JSONB), nullable=True)
    raw = Column(MutableDict.as_mutable(JSONB), nullable=True)

    inmueble = relationship("Inmueble", backref="wd_ext", uselist=False)
