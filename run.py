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

        # 上传到公共图床 **直接返回URL**
        files = {"image": buf}
        r = requests.post(
            "https://api.imgbb.com/1/upload",
            files=files,
            data={"key": "9d24cb2492c4d1855d4c1fa245444292"}
        )

        if r.status_code == 200:
            url = r.json()["data"]["url"]
            print(f"\n✅ 图片URL：{url}\n")
        else:
            print("❌ 上传失败")

    except Exception as e:
        print(f"错误：{e}")

if __name__ == "__main__":
    main()
