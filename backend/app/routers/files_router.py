from fastapi import APIRouter, Depends, UploadFile
from tables.file import File
from containers import file_decoder_dependency
from utilities.file_validator import FileValidator
from utilities.file_exception_handler import FileExceptionHandler
from containers import authorize_no_role, user_service_dependency, file_service_dependency


router = APIRouter()

@router.post("/file")
@FileExceptionHandler().handle_file_exceptions
def upload_file(file_decoder: file_decoder_dependency, user_service: user_service_dependency, file_service: file_service_dependency, file: UploadFile = Depends(FileValidator().validate_file), decoded_token = Depends(authorize_no_role)) -> int:
    external_user_id = decoded_token['sub']
    user = user_service.get_user_by_external_user_id(external_user_id)

    file_data = file_decoder.get_file_data(file)
    
    user_file = File(name=file_data.file_name, text=file_data.file_text, extension=file_data.file_extension, user_id=user.id)
    file_service.save_file(user_file)

    return user_file.id
    

   