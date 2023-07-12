import pygame as pg


class Event:
    __body: pg.event.Event

    def __init__(self, event: pg.event.Event):
        self.__body = event

    def is_exit(self) -> bool:
        return self.__body.type == pg.QUIT


class EventHandler:
    __events: list

    def __init__(self):
        self.__events = list()

    def update(self):
        self.__events = [Event(event) for event in self.__init_events()]

    @staticmethod
    def __init_events() -> list:
        return pg.event.get()

    def get_events(self) -> list:
        return self.__events