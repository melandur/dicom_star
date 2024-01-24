import re
from abc import ABC, abstractmethod

from loguru import logger


class Specification(ABC):
    """Abstract class for specifications"""

    @abstractmethod
    def is_satisfied(self, item: dict) -> bool:
        pass

    def __and__(self, other):
        """Overload the & operator to check if all specifications are satisfied"""
        return AndSpecification(self, other)

    def __or__(self, other):
        """Overload the | operator to check if any specification is satisfied"""
        return OrSpecification(self, other)

    def __invert__(self):
        """Overload the ~ operator to check if any specification is satisfied"""
        return NotSpecification(self)


class AndSpecification(Specification):
    """Class for and specifications"""

    def __init__(self, *args) -> None:
        self.args = args

    def is_satisfied(self, item: dict) -> bool:
        """Check if all specifications are satisfied"""
        return all(spec.is_satisfied(item) for spec in self.args)


class OrSpecification(Specification):
    """Class for or specifications"""

    def __init__(self, *args) -> None:
        self.args = args

    def is_satisfied(self, item: dict) -> bool:
        """Check if any specification is satisfied"""
        return any(spec.is_satisfied(item) for spec in self.args)


class NotSpecification(Specification):
    """Class for not specifications"""

    def __init__(self, spec) -> None:
        self.spec = spec

    def is_satisfied(self, item: dict) -> bool:
        """Check if any specification not satisfied"""
        return not self.spec.is_satisfied(item)


class Filter(ABC):
    """Abstract class for filters"""

    @abstractmethod
    def filter(self, item: dict, spec: Specification) -> str:
        """Abstract method for filtering"""
        pass


class ValueFilter(Specification):
    """Search for file name specifications with regex"""

    def __init__(self, *args) -> None:
        self.args = args

    def is_satisfied(self, tag_data: dict) -> bool:
        """Check if any specification for values is satisfied"""
        tag_values = tag_data['value']
        for arg in self.args:
            for tag_value in tag_values:
                try:
                    if bool(re.search(arg, str(tag_value))) and re.search(arg, str(tag_value)).group() != '':
                        return True
                except Exception as e:
                    logger.warning(f'Error in "{tag_value}":  {e}')
                    return False


class DicomFilter(Filter):
    """Subject filter loop"""

    def filter(self, tag_data: dict, spec: Specification) -> bool:
        if spec.is_satisfied(tag_data):
            return True
