# app/graphql/types/scalars/__init__.py
import strawberry
from decimal import Decimal
from uuid import UUID
from datetime import date, datetime
from typing import Any, Optional

@strawberry.scalar(name="Decimal")
class DecimalScalar:
    @staticmethod
    def serialize(value: Decimal | None) -> Optional[str]:
        if value is None:
            return None
        return format(value, "f")

    @staticmethod
    def parse_value(value: str) -> Decimal:
        return Decimal(value)

@strawberry.scalar(name="DateTime")
class DateTimeScalar:
    @staticmethod
    def serialize(value: datetime | None) -> Optional[str]:
        if value is None:
            return None
        return value.isoformat()

    @staticmethod
    def parse_value(value: str) -> datetime:
        return datetime.fromisoformat(value)

@strawberry.scalar(name="Date")
class DateScalar:
    @staticmethod
    def serialize(value: date | None) -> Optional[str]:
        if value is None:
            return None
        return value.isoformat()

    @staticmethod
    def parse_value(value: str) -> date:
        return date.fromisoformat(value)

@strawberry.scalar(name="JSON")
class JSONScalar:
    @staticmethod
    def serialize(value: Any | None) -> Any:
        return value

    @staticmethod
    def parse_value(value: Any) -> Any:
        return value

@strawberry.scalar(name="UUID")
class UUIDScalar:
    @staticmethod
    def serialize(value: UUID | None) -> Optional[str]:
        if value is None:
            return None
        return str(value)

    @staticmethod
    def parse_value(value: str) -> UUID:
        return UUID(value)