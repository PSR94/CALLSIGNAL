from fastapi import HTTPException


def bad_request(message: str) -> HTTPException:
    return HTTPException(status_code=400, detail={"error": "bad_request", "message": message})


def not_found(message: str) -> HTTPException:
    return HTTPException(status_code=404, detail={"error": "not_found", "message": message})


def conflict(message: str) -> HTTPException:
    return HTTPException(status_code=409, detail={"error": "conflict", "message": message})
