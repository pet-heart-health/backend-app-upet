from sqlite3 import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from SmartCollar.Domain.Models.smart_colllar_model import SmartCollar
from SmartCollar.Application.Schema.smart_collar_schema import SmartCollarRequest, SmartCollarResponse, SmartCollarUpdateRequest
from SmartCollar.Domain.ValueObject.location_type import LocationType
from models.pet import Pet

class SmartCollarService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_smart_collars(self) -> list[SmartCollarResponse]:
        collars = self.db.query(SmartCollar).all()

        collar_responses = []
        for collar in collars:
            location = LocationType(latitude=collar.latitude, longitude=collar.longitude)
            collar_responses.append(SmartCollarResponse(
                id=collar.id,
                serial_number=collar.serial_number,
                temperature=collar.temperature,
                lpm=collar.lpm,
                battery=collar.battery,
                location=location,
                pet_id=collar.pet_id
            ))

        return collar_responses


    def add_smart_collar(self, collar_data: SmartCollarRequest) -> SmartCollarResponse:
        try:
            location = LocationType(latitude=collar_data.location.latitude, longitude=collar_data.location.longitude)

            new_collar = SmartCollar(
                serial_number=collar_data.serial_number,
                temperature=collar_data.temperature,
                lpm=collar_data.lpm,
                battery=collar_data.battery,
                latitude=location.latitude,
                longitude=location.longitude,
                pet_id=None
            )

            self.db.add(new_collar)
            self.db.commit()
            self.db.refresh(new_collar)

            return SmartCollarResponse(
                id=new_collar.id,
                serial_number=new_collar.serial_number,
                temperature=new_collar.temperature,
                lpm=new_collar.lpm,
                battery=new_collar.battery,
                location=location, 
                pet_id=new_collar.pet_id
            )
        
        except IntegrityError as e:
            self.db.rollback()  # Rollback the transaction
            raise ValueError(f"Duplicate serial number: {collar_data.serial_number}. The collar already exists.") from e

    def delete_smart_collar(self, collar_id: int) -> bool:
        collar_to_delete = self.db.query(SmartCollar).filter(SmartCollar.id == collar_id).first()
        if collar_to_delete:
            self.db.delete(collar_to_delete)
            self.db.commit()
            return True
        return False

    def update_smart_collar(self, collar_id: int, collar_data: SmartCollarUpdateRequest) -> SmartCollarResponse:
            try:
                # Buscar el collar en la base de datos
                collar = self.db.query(SmartCollar).filter(SmartCollar.id == collar_id).first()
                
                if not collar:
                    raise NoResultFound(f"No collar found with ID {collar_id}")

                # Actualizar solo los campos específicos
                if collar_data.temperature is not None:
                    collar.temperature = collar_data.temperature
                if collar_data.lpm is not None:
                    collar.lpm = collar_data.lpm
                if collar_data.battery is not None:
                    collar.battery = collar_data.battery
                if collar_data.location and collar_data.location.latitude is not None and collar_data.location.longitude is not None:
                    collar.latitude = collar_data.location.latitude
                    collar.longitude = collar_data.location.longitude

                self.db.commit()
                self.db.refresh(collar)

                # Crear una respuesta con los datos actualizados
                location = LocationType(latitude=collar.latitude, longitude=collar.longitude)
                return SmartCollarResponse(
                    id=collar.id,
                    serial_number=collar.serial_number,
                    temperature=collar.temperature,
                    lpm=collar.lpm,
                    battery=collar.battery,
                    location=location,
                    pet_id=collar.pet_id
                )
            except NoResultFound:
                raise ValueError(f"No collar found with ID {collar_id}")
            
    def get_by_id(self, collar_id: int):
            try:
                # Buscar el collar por ID
                collar = self.db.query(SmartCollar).filter(SmartCollar.id == collar_id).first()
                
                # Si no se encuentra, lanzar excepción
                if not collar:
                    raise NoResultFound(f"No collar found with ID {collar_id}")
                
                # Crear la respuesta con los datos del collar encontrado
                location = LocationType(latitude=collar.latitude, longitude=collar.longitude)
                return SmartCollarResponse(
                    id=collar.id,
                    serial_number=collar.serial_number,
                    temperature=collar.temperature,
                    lpm=collar.lpm,
                    battery=collar.battery,
                    location=location,
                    pet_id=collar.pet_id

                )
            except NoResultFound:
                raise ValueError(f"No collar found with IDs {collar_id}")
            
    def get_by_pet_id(self, pet_id: int):
            # Buscar los collares asociados al pet_id
            collars = self.db.query(SmartCollar).filter(SmartCollar.pet_id == pet_id).all()

            # Si no se encuentran collares, lanzar excepción
            if not collars:
                raise ValueError(f"No collars found for pet ID {pet_id}")

            # Crear la lista de respuestas con los datos de los collares encontrados
            collar_responses = []
            for collar in collars:
                location = LocationType(latitude=collar.latitude, longitude=collar.longitude)
                collar_responses.append(SmartCollarResponse(
                    id=collar.id,
                    serial_number=collar.serial_number,
                    temperature=collar.temperature,
                    lpm=collar.lpm,
                    battery=collar.battery,
                    location=location,
                    pet_id=collar.pet_id
                ))

            return collar_responses

    def change_pet_association(self, collar_id: int, new_pet_id: int) -> SmartCollarResponse:
        try:
            # Buscar el collar en la base de datos
            collar = self.db.query(SmartCollar).filter(SmartCollar.id == collar_id).first()
            
            if not collar:
                raise NoResultFound(f"No collar found with ID {collar_id}")

            # Actualizar el pet_id del collar
            collar.pet_id = new_pet_id

            self.db.commit()
            self.db.refresh(collar)

            # Crear una respuesta con los datos actualizados
            location = LocationType(latitude=collar.latitude, longitude=collar.longitude)
            return SmartCollarResponse(
                id=collar.id,
                serial_number=collar.serial_number,
                temperature=collar.temperature,
                lpm=collar.lpm,
                battery=collar.battery,
                location=location,
                pet_id=collar.pet_id
            )
        except NoResultFound:
            raise ValueError(f"No collar found with ID {collar_id}")
        
    def disassociate_smart_collar(self, collar_id: int) -> SmartCollarResponse:
        try:
            # Buscar el collar en la base de datos
            collar = self.db.query(SmartCollar).filter(SmartCollar.id == collar_id).first()
            
            if not collar:
                raise NoResultFound(f"No collar found with ID {collar_id}")

            # Desasociar el collar estableciendo pet_id a None
            collar.pet_id = None

            self.db.commit()
            self.db.refresh(collar)

            # Crear una respuesta con los datos actualizados
            location = LocationType(latitude=collar.latitude, longitude=collar.longitude)
            return SmartCollarResponse(
                id=collar.id,
                serial_number=collar.serial_number,
                temperature=collar.temperature,
                lpm=collar.lpm,
                battery=collar.battery,
                location=location,
                pet_id=collar.pet_id  # pet_id ahora será None
            )
        except NoResultFound:
            raise ValueError(f"No collar found with ID {collar_id}")