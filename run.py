import os
import io
import requests
from PIL import Image
from pdf2image import convert_from_path

def main():
    pdf_url = os.environ.get("PDF_URL")
    if not pdf_url:
        print("未获取PDF链接")
        return

    # 下载PDF
    try:
        res = requests.get(pdf_url, timeout=20)
        with open("input.pdf", "wb") as f:
            f.write(res.content)
        print("✅ PDF下载成功")
    except:
        print("❌ PDF下载失败")
        return

    # 转换长图
    try:
        pages = convert_from_path("input.pdf", 150)
        total_h = sum(p.height for p in pages)
        max_w = max(p.width for p in pages)
        long_img = Image.new("RGB", (max_w, total_h))
        y = 0
        for page in pages:
            long_img.paste(page, (0, y))
            y += page.height

        # 保存到内存
        buf = io.BytesIO()
        long_img.save(buf, format="PNG")
        buf.seek(0)
        print("✅ 转换完成，准备上传…")

       # 替换掉你 run.py 里的上传代码
        # 上传到 ImgBB，获取公开 URL
        print("正在上传图片到图床...")
        upload_res = requests.post(
            "https://api.imgbb.com/1/upload",
            files={"image": img_buffer},
            data={"key": "36f548047220a38299b9f0e1f0452727"}  # 新的有效Key
        )

        if upload_res.status_code == 200:
            result = upload_res.json()
            image_url = result["data"]["url"]
            print(f"\n✅ 图片URL：{image_url}\n")
        else:
            print(f"❌ 上传失败，错误信息：{upload_res.text}")

    except Exception as e:
        print(f"错误：{e}")

if __name__ == "__main__":
    main()
