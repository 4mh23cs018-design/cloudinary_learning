import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from dotenv import load_dotenv

load_dotenv()

# ===== CONFIGURATION =====
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def upload_file(file_path):
    """
    Uploads image, video, or audio to Cloudinary
    """

    if not os.path.exists(file_path):
        print("[ERROR] File not found")
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

        print("\n[SUCCESS] Upload Successful!")
        print("Public ID:", response.get("public_id"))
        print("URL:", response.get("secure_url"))

        return response

    except Exception as e:
        print("[ERROR] Upload failed:", e)


def generate_html(image_url, video_url):
    """
    Generates index.html with the uploaded image and video
    """
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloudinary Media Gallery</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
            text-align: center;
        }}
        h1 {{
            color: #3448c5;
        }}
        h2 {{
            color: #555;
            margin-top: 30px;
        }}
        img {{
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        video {{
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <h1>Cloudinary Media Gallery</h1>

    <h2>Uploaded Image</h2>
    <img width="400" src="{image_url}" alt="Uploaded Image">

    <h2>Uploaded Video</h2>
    <video width="500" controls autoplay muted>
        <source src="{video_url}" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</body>
</html>"""

    output_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("\n[DONE] index.html generated! Open it in your browser to view.")


if __name__ == "__main__":
    # Upload image
    image_path = r"C:\Users\STUDENT\Documents\cloudinary_learning\image.png"
    print("[IMAGE] Uploading image...")
    image_response = upload_file(image_path)

    # Upload video
    video_path = r"C:\Users\STUDENT\Downloads\dream.mp4"
    print("\n[VIDEO] Uploading video...")
    video_response = upload_file(video_path)

    # Generate HTML page with both media
    if image_response and video_response:
        generate_html(
            image_response.get("secure_url"),
            video_response.get("secure_url")
        )
    else:
        print("\n[WARNING] Could not generate HTML - one or more uploads failed.")