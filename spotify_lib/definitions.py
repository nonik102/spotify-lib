from __future__ import annotations
from dataclasses import dataclass
from abc import ABC
from argparse import ArgumentParser, Namespace
from asyncio import Queue
from typing import Awaitable, Protocol


class Playable(Protocol):
    def play(self) -> None:
        ...

@dataclass
class PlayerResult:
    pass


class Player(ABC):
    @staticmethod
    def add_arguments(parser: ArgumentParser) -> None:
        ...
    @classmethod
    def from_namespace(cls, args: Namespace) -> Player:
        ...
    def add(self, playable: Playable) -> PlayerResult:
        ...


class Provider(ABC):

    @staticmethod
    def add_arguments(parser: ArgumentParser) -> None:
        ...
    @classmethod
    def from_namespace(cls, args: Namespace) -> Provider:
        ...
    def get_next(self) -> Playable:
        ...


class Dispatcher(ABC):

    @staticmethod
    def add_arguments(parser: ArgumentParser) -> None:
        ...
    @classmethod
    def from_namespace(cls, args: Namespace) -> Dispatcher:
        ...
    async def wait(self, result: PlayerResult | None) -> None:
        ...
