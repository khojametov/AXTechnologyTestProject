from typing import Generic, Literal, Type

from sqlmodel import Session, select
from sqlmodel.sql.expression import SelectOfScalar

from common.types import DataDict, ModelType


class BaseCRUDService(Generic[ModelType]):
    model: Type[ModelType]
    create_fields: set[str]
    update_fields: set[str]

    def __init__(
        self,
        model: Type[ModelType],
    ):
        self.model = model
        self._set_field_sets()

    def _set_field_sets(self) -> None:
        model_fields = set(self.model.__fields__.keys())
        for field_set in ["create_fields", "update_fields"]:
            if not hasattr(self, field_set):
                setattr(self, field_set, model_fields)

    def base_query(self) -> SelectOfScalar[ModelType]:
        """
        Base query for retrieving model. Used in all methods
        """
        return select(self.model)

    def get_query(self) -> SelectOfScalar[ModelType]:
        """
        Return query for retrieving single objects
        """
        return self.base_query()

    def get(self, session: Session, id: str | int) -> ModelType:
        """
        Retrieve single instance by id
        """
        return session.exec(self.get_query().filter(self.model.id == id)).one()

    def exists_by_id(self, session: Session, id: str | int) -> bool:
        """
        Retrieve single instance by id
        """
        return bool(
            session.exec(
                select(1).select_from(self.model).filter(self.model.id == id)
            ).one_or_none()
        )

    def list_query(self) -> SelectOfScalar[ModelType]:
        """
        Return query for retrieving objects list
        """
        return self.base_query()

    def list(self, session: Session) -> list[ModelType]:
        """
        Retrieve all objects from database
        """
        return session.exec(self.list_query()).all()

    def _verify_data_keys(
        self, data: DataDict, field_set: Literal["create_fields", "update_fields"]
    ) -> None:
        fields = getattr(self, field_set)
        for key in data.keys():
            if key not in fields:
                raise ValueError(f"Key {key} is not allowed in {field_set}")

    def create(
        self, session: Session, data: DataDict, commit: bool = True
    ) -> ModelType:
        self._verify_data_keys(data, "create_fields")
        data = self.before_create(session, data)
        model = self.perform_create(session, data, commit=commit)
        self.after_create(session, model)
        return model

    def perform_create(
        self, session: Session, data: DataDict, commit: bool = True
    ) -> ModelType:
        """
        Create model from input data
        Overwrite this if you need custom creation logic
        """
        model = self.model(**data)
        session.add(model)

        if commit:
            session.commit()

        return model

    def before_create(self, session: Session, data: DataDict) -> DataDict:
        """
        Hook called before creating model
        Overwrite this to define custom validation or data modification logic
        """
        return data

    def after_create(self, session: Session, model: ModelType) -> None:
        """
        Hook called after model was created and session committed
        """
        pass

    def update(
        self, session: Session, instance: ModelType, data: DataDict, commit: bool = True
    ) -> ModelType:
        self._verify_data_keys(data, "update_fields")
        data = self.before_update(session, instance, data)
        updated = self.perform_update(session, instance, data, commit=commit)
        self.after_update(session, updated)
        return updated

    def perform_update(
        self, session: Session, instance: ModelType, data: DataDict, commit: bool = True
    ) -> ModelType:
        """
        Update model from input data
        Overwrite this if you need custom update logic
        """
        for field, value in data.items():
            setattr(instance, field, value)

        session.add(instance)

        if commit:
            session.commit()

        return instance

    def before_update(
        self, session: Session, instance: ModelType, data: DataDict
    ) -> DataDict:
        """
        Hook called before updating model
        Overwrite this to define custom validation or data modification logic
        """
        return data

    def after_update(self, session: Session, instance: ModelType) -> None:
        """
        Hook called after model was updated and session committed
        """
        pass

    def delete(
        self, session: Session, instance: ModelType, commit: bool = True
    ) -> None:
        self.before_delete(session, instance)
        self.perform_delete(session, instance, commit=commit)
        self.after_delete(session, instance)

    def perform_delete(
        self, session: Session, instance: ModelType, commit: bool = True
    ) -> None:
        """
        Delete model from database
        Overwrite this if you need custom deletion logic (you probably don't)
        """
        session.delete(instance)
        if commit:
            session.commit()

    def before_delete(self, session: Session, instance: ModelType) -> None:
        """
        Hook called before deleting model
        """
        pass

    def after_delete(self, session: Session, instance: ModelType) -> None:
        """
        Hook called after model was deleted and session committed
        """
        pass
