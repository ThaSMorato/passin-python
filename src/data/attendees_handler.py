import uuid
from src.models.repository.attendees_repository import AttendeesRepository
from src.models.repository.events_repository import EventsRepository
from src.http_types.http_request import HttpRequest
from src.http_types.http_response import HttpResponse
from src.errors.error_types.http_not_found import HttpNotFound
from src.errors.error_types.http_conflict import HttpConflictError

class AttendeesHandler:
  def __init__(self) -> None:
    self.__attendees_repository = AttendeesRepository()
    self.__events_repository = EventsRepository()

  def register(self, http_request: HttpRequest) -> HttpResponse:
    body = http_request.body
    event_id = http_request.param["event_id"]

    event_attendees_count = self.__events_repository.count_event_attendees(event_id)

    if (event_attendees_count["attendeesAmount"] and event_attendees_count["maximumAttendees"] <= event_attendees_count["attendeesAmount"]):
      raise HttpConflictError("Evento lotado")

    body["uuid"] = str(uuid.uuid4())
    body["event_id"] = event_id

    self.__attendees_repository.insert_attendee(body)

    return HttpResponse(body=None, status_code=201)

  def find_attendee_bagde(self, http_request: HttpRequest) -> HttpResponse:
    attendee_id = http_request.param["attendee_id"]

    badge = self.__attendees_repository.get_attendee_badge_by_id(attendee_id)

    if not badge:
      raise HttpNotFound("Participante nao encontrado")

    return HttpResponse(
      body={
        "badge": {
          "name": badge.name,
          "email": badge.email,
          "eventTitle": badge.title,
        }
      },
      status_code=200
    )

  def find_attendees_from_event(self, http_request: HttpRequest) -> HttpResponse:
    event_id = http_request.param["event_id"]
    attendees = self.__attendees_repository.get_attendees_by_event_id(event_id)

    if not attendees:
      raise HttpNotFound("Participantes nao encontrados")

    formatted_attendees = []
    for attendee in attendees:
      formatted_attendees.append(
        {
          "id": attendee.id,
          "name": attendee.name,
          "email": attendee.email,
          "checkedInAt": attendee.checkInAt,
          "createAt": attendee.createdAt,
        }
      )

    return HttpResponse(
      body={
        "attendees": formatted_attendees
      },
      status_code=200
    )


