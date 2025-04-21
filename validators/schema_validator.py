from fastapi import HTTPException, status

class SchemaValidator:

    @staticmethod
    def validate_schema(schema, db):
        required_fields = [field for field in schema.__annotations__.keys() if getattr(schema, field, None)]
        missing_fields = [field for field in required_fields if not getattr(schema, field, None)]
        if missing_fields:
            error_message = f"Los siguientes campos son requeridos: {', '.join(missing_fields)}"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)