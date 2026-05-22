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

        # 只保存，不上传
        os.makedirs("output", exist_ok=True)
        long_img.save("output/output.png")
        print("✅ 图片已生成！")
        print("👉 访问地址：https://xztx23.github.io/pdf2img-api/output.png")

    except Exception as e:
        print(f"错误：{e}")

if __name__ == "__main__":
    main()
