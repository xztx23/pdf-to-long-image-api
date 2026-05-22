import os
import time
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
        max_w = max(img.width for img in pages)
        canvas = Image.new("RGB", (max_w, total_h))
        
        y = 0
        for img in pages:
            canvas.paste(img, (0, y))
            y += img.height

        # 创建 images 文件夹
        os.makedirs("images", exist_ok=True)

        # 时间戳命名
        timestamp = str(int(time.time()))
        img_path = f"images/{timestamp}.png"

        # 保存
        canvas.save(img_path)
        print(f"✅ 新图片已保存：{img_path}")

        # 输出真实URL
        username = "xztx23"
        repo = "pdf2img-api"
        branch = "main"
        final_url = f"https://raw.githubusercontent.com/{username}/{repo}/{branch}/{img_path}"
        
        print("\n=====================================")
        print("✅ 大模型可直接访问的图片URL：")
        print(final_url)
        print("=====================================\n")

    except Exception as e:
        print(f"错误：{e}")

if __name__ == "__main__":
    main()
