from fastapi import Header, HTTPException, Depends
from typing import Annotated, Optional


async def verify_api_key(
    x_api_key: Annotated[Optional[str], Header()] = None
) -> str:
    """
    Dependency to verify API key from headers.
    
    This is a placeholder for future API key authentication.
    Currently allows all requests without an API key.
    
    Args:
        x_api_key: Optional API key from request header.
        
    Returns:
        The validated API key or a default value.
    """
    # TODO: Implement actual API key verification
    if x_api_key is not None:
        # Future: Validate against stored keys
        return x_api_key
    return "default-key"


CommonDependencies = Annotated[str, Depends(verify_api_key)]

