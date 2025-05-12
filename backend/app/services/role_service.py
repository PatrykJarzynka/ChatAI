from fastapi import HTTPException
import requests

from enums.role import Role

class RoleService:
    def save_user_default_role(self, user_id: int) -> None:
        requests.post(f'http://127.0.0.1:8001/role/default',json={user_id})

    def autorize_role(self, role: Role, user_id: int) -> bool:
        try:
            body = {"role": role, "user_id": user_id}

            response =  requests.post(f'http://127.0.0.1:8001/role/authorize', json=body)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as http_error:
            detail = http_error.response.json().get("detail", str(http_error))
            raise HTTPException(status_code=http_error.response.status_code, detail=detail)
        
