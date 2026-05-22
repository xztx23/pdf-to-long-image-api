import os
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

        # 直接保存到仓库根目录
        long_img.save("output.png")
        print("✅ 图片生成成功！")
        print("👉 大模型可直接查看：")
        print("https://raw.githubusercontent.com/xztx23/pdf2img-api/main/output.png")

    except Exception as e:
        print(f"错误：{e}")

if __name__ == "__main__":
    main()
