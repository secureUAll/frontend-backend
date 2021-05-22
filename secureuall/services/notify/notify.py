from __future__ import annotations
from abc import ABC, abstractmethod

"""
This class defines the interface for notification services

The methods (text, olist, ulist and citation) must implement parsing of the following elements:
- Labels: `this is a label`
- Bold: **This is bold text**
- Italic: *This is bold text* 
"""


class Notify(ABC):

    # INSERT methods
    @abstractmethod
    def heading(self, h1: str, end="\n") -> Notify:
        pass

    @abstractmethod
    def text(self, text: str, end="\n") -> Notify:
        pass

    @abstractmethod
    def olist(self, lst: list) -> Notify:
        pass

    @abstractmethod
    def ulist(self, lst: list) -> Notify:
        pass

    @abstractmethod
    def citation(self, citation: str, end="\n") -> Notify:
        pass

    @abstractmethod
    def code(self, block: str) -> Notify:
        pass

    @abstractmethod
    def url(self, url: str, end="\n") -> Notify:
        pass

    @abstractmethod
    def brake(self) -> Notify:
        pass

    # DECORATION methods
    @abstractmethod
    def bold(self, text :str, end="\n") -> Notify:
        pass

    @abstractmethod
    def italic(self, text: str, end="\n") -> Notify:
        pass

    @abstractmethod
    def label(self, text: str, end="\n") -> Notify:
        pass

    # PARSING
    @abstractmethod
    def __str__(self) -> str:
        pass

    # SEND methods
    @abstractmethod
    def send(self, recipient: str) -> int:
        pass
