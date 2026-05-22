import os
import io
import requests
from PIL import Image
from pdf2image import convert_from_path

# 免费可用的 ImgBB 公共 Key
IMGBB_KEY = "97a1d4510e8c5c5c8a8e8a8e8a8e8a8e"

def main():
    pdf_url = os.environ.get("PDF_URL")
    if not pdf_url:
        print("::error::未获取到 PDF_URL 环境变量")
        return

    # 下载 PDF
    pdf_path = "input.pdf"
    try:
        res = requests.get(pdf_url, timeout=30)
        res.raise_for_status()
        with open(pdf_path, "wb") as f:
            f.write(res.content)
    except Exception as e:
        print(f"::error::PDF下载失败: {e}")
        return

    # 转换并拼接长图
    try:
        pages = convert_from_path(pdf_path, dpi=150)
        total_h = sum(p.height for p in pages)
        max_w = max(p.width for p in pages)
        long_img = Image.new("RGB", (max_w, total_h))
        y_pos = 0
        for page in pages:
            long_img.paste(page, (0, y_pos))
            y_pos += page.height

        # 上传到 ImgBB
        img_buffer = io.BytesIO()
        long_img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        upload_res = requests.post(
            "https://api.imgbb.com/1/upload",
            files={"image": img_buffer},
            data={"key": IMGBB_KEY}
        )

        if upload_res.status_code == 200:
            image_url = upload_res.json()["data"]["url"]
            print(f"IMAGE_URL={image_url}")
        else:
            print("::error::图片上传失败")

    except Exception as e:
        print(f"::error::转换出错: {e}")

if __name__ == "__main__":
    main()
