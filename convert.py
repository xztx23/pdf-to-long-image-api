import os
import requests
from PIL import Image
from pdf2image import convert_from_path

def main():
    pdf_url = os.environ.get("PDF_URL")
    task_id = os.environ.get("TASK_ID")

    if not pdf_url:
        print("ERROR: 未获取PDF链接")
        return
    if not task_id:
        print("ERROR: 未获取任务ID")
        return

    # 下载 PDF
    try:
        res = requests.get(pdf_url, timeout=20)
        with open("input.pdf", "wb") as f:
            f.write(res.content)
    except:
        print("ERROR: PDF下载失败")
        return

    # 转换长图
    try:
        pages = convert_from_path("input.pdf", 150)
        total_h = sum(p.height for p in pages)
        max_w = max(p.width for p in pages)
        long_img = Image.new("RGB", (max_w, total_h))
        
        y = 0
        for img in pages:
            long_img.paste(img, (0, y))
            y += img.height

        # 保存到 images 文件夹，文件名直接用 task_id
        os.makedirs("images", exist_ok=True)
        save_path = f"images/{task_id}.png"
        long_img.save(save_path)

        # 生成真实可访问的 GitHub 图片 URL
        url = f"https://raw.githubusercontent.com/xztx23/pdf-to-long-image-api/main/{save_path}"

        # 输出固定格式，让扣子能读取
        print(f"IMAGE_URL:{url}")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
