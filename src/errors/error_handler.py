from src.http_types.http_response import HttpResponse
from src.errors.error_types.http_conflict import HttpConflictError
from src.errors.error_types.http_not_found import HttpNotFound

def handle_error(error: Exception):
  if isinstance(error, (HttpNotFound, HttpConflictError)):
    return HttpResponse(
      body={
        "errors": [
          {
            "title": error.name,
            "details": error.message
          }
        ]
      },
      status_code=error.status_code
    )

  return HttpResponse(
    body={
      "errors": [
        {
          "title": "error",
          "details": str(error)
        }
      ]
    },
    status_code=400
  )
