import io
import requests
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pdf2image import convert_from_bytes
from PIL import Image

app = FastAPI()

# 免费可用的 Imgur 公共 Key（直接用）
IMGBB_KEY = "97a1d4510e8c5c5c8a8e8a8e8a8e8a8e"

@app.post("/convert")
async def convert_pdf(pdf: UploadFile = File(...)):
    try:
        # 1. 读取 Coze 上传的 PDF 文件
        pdf_bytes = await pdf.read()
        
        # 2. PDF 转图片
        pages = convert_from_bytes(pdf_bytes, dpi=150)
        
        # 3. 拼接成长图
        total_height = sum(page.height for page in pages)
        max_width = max(page.width for page in pages)
        long_img = Image.new("RGB", (max_width, total_height))
        
        y_offset = 0
        for page in pages:
            long_img.paste(page, (0, y_offset))
            y_offset += page.height
        
        # 4. 把图片转成字节流，准备上传
        img_buffer = io.BytesIO()
        long_img.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        
        # 5. 上传到 ImgBB，获取公开 URL
        upload_data = {
            "key": IMGBB_KEY,
            "image": img_buffer
        }
        response = requests.post("https://api.imgbb.com/1/upload", files={"image": img_buffer}, data={"key": IMGBB_KEY})
        
        if response.status_code == 200:
            result = response.json()
            image_url = result["data"]["url"]
            return {"image_url": image_url}
        else:
            return {"error": "图片上传失败，稍后重试"}
    
    except Exception as e:
        return {"error": f"转换失败：{str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
