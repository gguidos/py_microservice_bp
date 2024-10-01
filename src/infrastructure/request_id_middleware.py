from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Extract request ID from the headers (or generate one if not present)
        request_id = request.headers.get("X-Request-ID", "default-request-id")
        
        # Store it in the request state for further use
        request.state.request_id = request_id

        # Call the next middleware or route handler
        response = await call_next(request)
        return response
