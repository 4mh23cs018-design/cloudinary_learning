import cloudinary
import cloudinary.uploader
import cloudinary.api
import os

# ===== CONFIGURATION =====
cloudinary.config(
    cloud_name="YOUR_CLOUD_NAME",
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET"
)

def upload_file(file_path):
    """
    Uploads image, video, or audio to Cloudinary
    """

    if not os.path.exists(file_path):
        print("❌ File not found")
        return

    # Determine resource type automatically
    ext = file_path.split(".")[-1].lower()

    image_ext = ["jpg", "jpeg", "png", "gif", "webp"]
    video_ext = ["mp4", "mov", "avi", "mkv"]
    audio_ext = ["mp3", "wav", "aac", "flac", "m4a"]

    if ext in image_ext:
        resource_type = "image"
    elif ext in video_ext:
        resource_type = "video"
    elif ext in audio_ext:
        resource_type = "video"  # Cloudinary treats audio as video
    else:
        resource_type = "auto"

    try:
        response = cloudinary.uploader.upload(
            file_path,
            resource_type=resource_type
        )

        print("\n✅ Upload Successful!")
        print("Public ID:", response.get("public_id"))
        print("URL:", response.get("secure_url"))

        return response

    except Exception as e:
        print("❌ Upload failed:", e)


if __name__ == "__main__":
    file_to_upload = input("Enter file path: ").strip()
    upload_file(file_to_upload)