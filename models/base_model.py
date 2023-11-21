#!/usr/bin/python3
"""Defines the BaseModel class."""
import models
import uuid
from datetime import datetime


class BaseModel:
    """Represents the BaseModel of HBnB project."""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel class."""
        for_mat = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    self.__dict__[key] = datetime.strptime(value, for_mat)
                else:
                    self.__dict__[key] = kwargs[key]
        else:
            models.storage.new(self)

    def __str__(self):
        """Return a string representation of the BaseModel instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Update the updated_at attribute with the current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Convert the BaseModel instance to a dictionary representation.
        Dictionary will contain all keys and values of the instance attribute.
        __class__ key will be added with the class name of the object.
        The created_at and updated_at will be converted to
        string objects in ISO format.
        """
        dicts = self.__dict__.copy()
        dicts["__class__"] = self.__class__.__name__
        dicts["created_at"] = self.created_at.isoformat()
        dicts["updated_at"] = self.updated_at.isoformat()
        return dicts
