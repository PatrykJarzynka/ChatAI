from fastapi import HTTPException
import requests

from config import get_settings
from enums.role import Role


class RoleService:
    def __init__(self) -> None:
        self.service_url = get_settings().ROLE_SERVICE_URL

    def save_user_default_role(self, user_id: int) -> None:
        url = self.service_url + '/role/default'
        requests.post(url ,json={user_id})

    def autorize_role(self, role: Role, user_id: int) -> bool:
        try:
            body = {"role": role, "user_id": user_id}
            url = self.service_url + '/role/authorize'

            response =  requests.post(url, json=body)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as http_error:
            detail = http_error.response.json().get("detail", str(http_error))
            raise HTTPException(status_code=http_error.response.status_code, detail=detail)
        
