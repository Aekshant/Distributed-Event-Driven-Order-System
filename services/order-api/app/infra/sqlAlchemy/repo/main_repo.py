import logging
from typing import Generic, List, Type, TypeVar, Optional, Any, Dict
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

logger = logging.getLogger(__name__)

# Declare a TypeVar bound to your SQLAlchemy Base if you have one, or just Any object
ModelType = TypeVar("ModelType")


class SqlGenericRepository(Generic[ModelType]):

    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    async def create_one(self, instance: ModelType) -> ModelType:
        try:
            self.session.add(instance)
            await self.session.flush()
            # If you prefer the repo to handle commits directly:
            await self.session.commit()

            # Use getattr so it doesn't crash if a model doesn't use 'id'
            logger.info("Created %s with ID %s", self.model.__name__, getattr(instance, 'id', None))
            return instance
        except SQLAlchemyError as e:
            await self.session.rollback()  # Crucial for async sessions on failure
            logger.error("Failed to create %s: %s", self.model.__name__, e)
            raise InfrastructureError(f"Failed to create {self.model.__name__}") from e

    async def get_by_id(self, id: Any) -> Optional[ModelType]:
        try:
            stmt = select(self.model).where(self.model.id == id)
            result = await self.session.execute(stmt)
            db_data = result.scalar_one_or_none()
            if not db_data:
                logger.warning("%s with ID %s not found", self.model.__name__, id)
                return None
            return db_data
        except SQLAlchemyError as e:
            logger.error("Failed to fetch %s: %s", self.model.__name__, e)
            raise InfrastructureError(f"Failed to fetch {self.model.__name__}") from e

    async def list_all(self) -> List[ModelType]:
        try:
            stmt = select(self.model)
            result = await self.session.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error("Failed to fetch %s list: %s", self.model.__name__, e)
            raise InfrastructureError(f"Failed to fetch {self.model.__name__}") from e

    async def delete_one(self, id: Any) -> bool:
        try:
            stmt = (
                delete(self.model)
                .where(self.model.id == id)
                .returning(self.model.id)
            )
            result = await self.session.execute(stmt)
            deleted_id = result.scalar_one_or_none()

            if deleted_id:
                await self.session.commit()  # Commit the deletion
                logger.info("Deleted %s with ID %s", self.model.__name__, deleted_id)
                return True

            return False
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error("Failed to delete %s: %s", self.model.__name__, e)
            raise InfrastructureError(f"Failed to delete {self.model.__name__}") from e

    async def update_one(self, id: Any, update_data: Dict[str, Any]) -> bool:
        try:
            filtered_data = {k: v for k, v in update_data.items() if v is not None}

            if not filtered_data:
                return False

            stmt = (
                update(self.model)  # Fixed: No longer hardcoded
                .where(self.model.id == id)
                .values(**filtered_data)
                .returning(self.model.id)
            )

            result = await self.session.execute(stmt)
            updated_id = result.scalar_one_or_none()

            if updated_id:
                await self.session.commit()
                logger.info("Updated %s with ID %s", self.model.__name__, updated_id)
                return True

            return False
        except IntegrityError as e:
            await self.session.rollback()
            logger.warning("Integrity constraint violated updating %s: %s", self.model.__name__, e)
            detail = str(e.orig) if e.orig else str(e)
            raise IntegrityConstraintError(detail) from e
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error("Failed to update %s: %s", self.model.__name__, e)
            raise InfrastructureError(f"Failed to update {self.model.__name__}") from e