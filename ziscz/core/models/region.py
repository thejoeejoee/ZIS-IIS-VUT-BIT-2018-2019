# coding=utf-8
from .base import BaseTypeModel


class TypeRegion(BaseTypeModel):
    """
    Oblast výskytu.
    """
    pass


class TypeCountry(BaseTypeModel):
    """
    Země pro původ zvířat.
    """
    pass


__all__ = ["TypeCountry", "TypeCountry"]
