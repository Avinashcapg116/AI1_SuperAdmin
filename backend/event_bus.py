"""
Ai1 Event Bus - Asynchronous In-Process Pub/Sub for Domain Decoupling
"""

import asyncio
from typing import Callable, Dict, List, Any
import logging

logger = logging.getLogger("ai1.event_bus")


class Event:
    def __init__(self, name: str, data: Dict[str, Any]):
        self.name = name
        self.data = data
        self.timestamp = asyncio.get_event_loop().time() if asyncio.get_event_loop().is_running() else 0


class AsyncEventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Event], Any]]] = {}

    def subscribe(self, event_name: str, handler: Callable[[Event], Any]):
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(handler)

    async def publish(self, event_name: str, data: Dict[str, Any]):
        event = Event(name=event_name, data=data)
        handlers = self._subscribers.get(event_name, [])
        # Also notify wildcard subscribers
        handlers = handlers + self._subscribers.get("*", [])
        
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    asyncio.create_task(handler(event))
                else:
                    handler(event)
            except Exception as e:
                logger.error(f"Error handling event {event_name} in {handler}: {e}")


# Global Event Bus Singleton
event_bus = AsyncEventBus()
