import pygame as pg
from typing import List

class Event:
    __body: pg.event.Event

    def __init__(self, event: pg.event.Event) -> None:
        self.__body = event
    
    def get_body(self) -> pg.event.Event:
        """Get event."""
        return self.__body


class EventHandler:
    __events: List[Event]

    def __init__(self) -> None:
        self.__events = list()

    def update(self) -> None:
        """Update event handler. Clear old events and upload new ones."""
        self.__events.clear()
        
        for event in pg.event.get():
            self.__events.append(Event(event))

    def get_events(self) -> List[Event]:
        """Get events."""
        return self.__events