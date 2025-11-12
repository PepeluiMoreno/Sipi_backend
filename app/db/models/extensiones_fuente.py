from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from .base import Base, UUIDPKMixin, AuditMixin

class InmuebleOSMExt(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmuebles_osm_ext"
    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id"), nullable=False, unique=True)
    osm_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    osm_type: Mapped[str | None] = mapped_column(String(10), nullable=True)
    version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_updated_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    tags = mapped_column(MutableDict.as_mutable(JSONB), nullable=True)
    raw = mapped_column(MutableDict.as_mutable(JSONB), nullable=True)
    inmueble = relationship("Inmueble", backref="osm_ext", uselist=False)

class InmuebleWDExt(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmuebles_wd_ext"
    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id"), nullable=False, unique=True)
    wikidata_qid: Mapped[str | None] = mapped_column(String(32), nullable=True, unique=True)
    commons_category: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_updated_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    claims = mapped_column(MutableDict.as_mutable(JSONB), nullable=True)
    sitelinks = mapped_column(MutableDict.as_mutable(JSONB), nullable=True)
    raw = mapped_column(MutableDict.as_mutable(JSONB), nullable=True)
    inmueble = relationship("Inmueble", backref="wd_ext", uselist=False)
