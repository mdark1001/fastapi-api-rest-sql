"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 15/03/22
@name: response
"""
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse


def not_found(message='Not found'):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=message
    )


def bad_request(message='Error to process your request'):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message
    )


def success_request(message='All good'):
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={'message': message})
