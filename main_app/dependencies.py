
from fastapi import Header, HTTPException
from fastapi import Depends, FastAPI, Security, status
from fastapi.security.api_key import APIKeyHeader


api_key_header_auth = APIKeyHeader(name="X-API-KEY", auto_error=True)


def get_user_details(api_key_header: str = Security(api_key_header_auth)):
    print("get api details", api_key_header)
    if not api_key_header:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized",
        )
    if api_key_header != "cars-for-test":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized",
        )
    return True

