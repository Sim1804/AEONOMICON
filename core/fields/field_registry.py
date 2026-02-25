from typing import Dict, Iterable

from core.fields.field_base import Field

class FieldRegistry:

    def __init__(self):
        self._fields: Dict[str, Field] = {}

    def register(self, field: Field) -> None:
        field_id = field.field_id

        if field_id in self._fields:
            raise ValueError(
                f"Field with id '{field_id}' is already registered."
            )
        
        self._fields[field_id] = field

    def get(self, field_id: str) -> Field:

        try:
            return self._fields[field_id]
        except KeyError as exc:
            raise KeyError( 
                f"Field with id '{field_id}' is not registered."
                ) from exc
    
    def all_fields(self) -> Iterable[Field]:
        return self._fields.values()
    
    def has_field(self, field_id: str) -> bool:
        return field_id in self._fields
    
    def __len__(self) -> int:
        return len(self._fields)
    
    def __repr__(self) -> str:
        field_ids = ", ".join(self._fields.keys())
        return f"<FieldRegistry fields=[{field_ids}]>"