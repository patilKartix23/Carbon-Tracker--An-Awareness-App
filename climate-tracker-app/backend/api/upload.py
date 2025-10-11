"""
File upload API routes with Cloudinary integration
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import JSONResponse
import cloudinary
import cloudinary.uploader
import cloudinary.api
from PIL import Image
import io
import structlog
from typing import Optional

from api.auth import get_current_active_user
from database.models import User
from core.config import settings

logger = structlog.get_logger()
router = APIRouter()

# Configure Cloudinary
if settings.CLOUDINARY_CLOUD_NAME:
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True
    )

def validate_image(file: UploadFile) -> bool:
    """Validate uploaded image"""
    # Check file type
    if not file.content_type.startswith('image/'):
        return False
    
    # Check file size (10MB limit)
    if hasattr(file, 'size') and file.size > 10 * 1024 * 1024:
        return False
    
    return True

def process_image(image_data: bytes) -> bytes:
    """Process and optimize image"""
    try:
        # Open image with PIL
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if necessary
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background
        
        # Resize if too large (max 1920x1920)
        max_size = 1920
        if image.width > max_size or image.height > max_size:
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        # Save optimized image
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=85, optimize=True)
        return output.getvalue()
        
    except Exception as e:
        logger.error("Image processing failed", error=str(e))
        raise

@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    folder: Optional[str] = "climate_posts",
    current_user: User = Depends(get_current_active_user)
):
    """Upload image to Cloudinary"""
    try:
        # Validate image
        if not validate_image(file):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image file. Must be an image under 10MB."
            )
        
        # Read and process image
        image_data = await file.read()
        processed_image = process_image(image_data)
        
        # Upload to Cloudinary
        if not settings.CLOUDINARY_CLOUD_NAME:
            # Mock response for development
            return JSONResponse({
                "status": "success",
                "url": f"https://via.placeholder.com/800x600/4CAF50/white?text=Uploaded+Image",
                "public_id": f"mock_image_{current_user.id}",
                "message": "Mock upload (configure Cloudinary for real uploads)"
            })
        
        # Real Cloudinary upload
        upload_result = cloudinary.uploader.upload(
            processed_image,
            folder=f"climate_tracker/{folder}",
            public_id=f"{current_user.id}_{file.filename.split('.')[0]}",
            overwrite=True,
            resource_type="image",
            transformation=[
                {"width": 800, "height": 600, "crop": "limit"},
                {"quality": "auto", "fetch_format": "auto"}
            ]
        )
        
        logger.info("Image uploaded successfully", 
                   user_id=current_user.id, 
                   public_id=upload_result.get('public_id'))
        
        return JSONResponse({
            "status": "success",
            "url": upload_result['secure_url'],
            "public_id": upload_result['public_id'],
            "width": upload_result.get('width'),
            "height": upload_result.get('height'),
            "format": upload_result.get('format'),
            "bytes": upload_result.get('bytes')
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Image upload failed", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload image"
        )

@router.delete("/image/{public_id}")
async def delete_image(
    public_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete image from Cloudinary"""
    try:
        if not settings.CLOUDINARY_CLOUD_NAME:
            return JSONResponse({
                "status": "success",
                "message": "Mock deletion (configure Cloudinary for real deletions)"
            })
        
        # Delete from Cloudinary
        result = cloudinary.uploader.destroy(public_id)
        
        if result.get('result') == 'ok':
            logger.info("Image deleted successfully", 
                       user_id=current_user.id, 
                       public_id=public_id)
            return JSONResponse({
                "status": "success",
                "message": "Image deleted successfully"
            })
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found or already deleted"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Image deletion failed", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete image"
        )

@router.post("/profile-image")
async def upload_profile_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """Upload user profile image"""
    try:
        # Validate image
        if not validate_image(file):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image file. Must be an image under 10MB."
            )
        
        # Read and process image
        image_data = await file.read()
        processed_image = process_image(image_data)
        
        # Upload to Cloudinary with profile-specific transformations
        if not settings.CLOUDINARY_CLOUD_NAME:
            # Mock response
            mock_url = f"https://via.placeholder.com/200x200/2196F3/white?text={current_user.username[0].upper()}"
            return JSONResponse({
                "status": "success",
                "url": mock_url,
                "public_id": f"profile_mock_{current_user.id}",
                "message": "Mock profile upload (configure Cloudinary for real uploads)"
            })
        
        upload_result = cloudinary.uploader.upload(
            processed_image,
            folder="climate_tracker/profiles",
            public_id=f"profile_{current_user.id}",
            overwrite=True,
            resource_type="image",
            transformation=[
                {"width": 200, "height": 200, "crop": "fill", "gravity": "face"},
                {"quality": "auto", "fetch_format": "auto"}
            ]
        )
        
        logger.info("Profile image uploaded", 
                   user_id=current_user.id, 
                   public_id=upload_result.get('public_id'))
        
        return JSONResponse({
            "status": "success",
            "url": upload_result['secure_url'],
            "public_id": upload_result['public_id']
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Profile image upload failed", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload profile image"
        )
