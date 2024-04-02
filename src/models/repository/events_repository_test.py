import pytest
from src.models.settings.connection import db_connection_handler
from .events_repository import EventsRepository

db_connection_handler.connect_to_db()

@pytest.mark.skip(reason="New entity on database")
def test_insert_events():
  event = {
    "uuid": "meu-uuid-e-nois3",
    "title": "meu title",
    "maximum_attendees": 20,
    "slug": "meu-slug3"
  }
  events_repository = EventsRepository()
  response = events_repository.insert_event(event)
  print(response)

def test_get_event_by_id():
  event_id = "meu-uuid-e-nois2"
  events_repository = EventsRepository()
  response = events_repository.get_event_by_id(event_id)
  print(response)
