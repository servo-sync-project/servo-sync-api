import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException
from core.config import settings

class CloudinaryService:
    def __init__(self):
        cloudinary.config(
            cloud_name=settings.cloudinary_cloud_name,
            api_key=settings.cloudinary_api_key, 
            api_secret=settings.cloudinary_api_secret, 
            secure=settings.cloudinary_secure
        )

    def uploadImage(self,  folder: str, plublic_id: str, image_file: UploadFile) -> str:
        try:
            file_content = image_file.file.read()

            response = cloudinary.uploader.upload(
                file_content,
                folder=folder,
                public_id=plublic_id,
                use_filename=True,
                unique_filename=False,
                overwrite=True
            )

            return response.get("secure_url")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al subir la imagen: {str(e)}")
