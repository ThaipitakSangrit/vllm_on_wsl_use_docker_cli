import base64
import mimetypes
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY"
)

def encode_image(image_path):
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        mime_type = "image/png"
    with open(image_path, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded_string}"

image_path = "sample.png"
image_url = encode_image(image_path)

# 1. ลองใช้ chat.completions แบบพิมพ์เช็ค response ตัวเต็ม
try:
    response = client.chat.completions.create(
        model="baidu/Unlimited-OCR",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "OCR:"},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ],
        temperature=0.0,
        max_tokens=1024,
        extra_body={
            "skip_special_tokens": False  # ดูว่าติด Special/Stop Token หรือไม่
        }
    )
    
    choice = response.choices[0]
    # print(f"--- Chat API Response ---")
    # print(f"Finish Reason: {choice.finish_reason}")
    print(choice.message.content.strip())

except Exception as e:
    print(f"Error: {e}")