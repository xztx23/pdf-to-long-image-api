import os
import requests
from PIL import Image
from pdf2image import convert_from_path

def main():
    pdf_url = os.environ.get("PDF_URL")
    student_id = os.environ.get("STUDENT_ID")

    if not pdf_url:
        print("ERROR: 未获取PDF链接")
        return
    if not student_id:
        print("ERROR: 未获取学生学号")
        return

    # 下载 PDF
    try:
        res = requests.get(pdf_url, timeout=25)
        with open("input.pdf", "wb") as f:
            f.write(res.content)
    except Exception as e:
        print(f"ERROR: PDF下载失败 {e}")
        return

    # 转换长图
    try:
        pages = convert_from_path("input.pdf", 150)
        total_height = sum(p.height for p in pages)
        max_width = max(p.width for p in pages)
        long_image = Image.new("RGB", (max_width, total_height))

        y_offset = 0
        for page in pages:
            long_image.paste(page, (0, y_offset))
            y_offset += page.height

        # 保存为 学号.png
        os.makedirs("images", exist_ok=True)
        save_path = f"images/{student_id}.png"
        long_image.save(save_path, "PNG")

        # 输出可访问URL
        final_url = f"https://raw.githubusercontent.com/xztx23/pdf-to-long-image-api/main/{save_path}"
        print(f"IMAGE_URL:{final_url}")

    except Exception as e:
        print(f"ERROR: 转换失败 {e}")

if __name__ == "__main__":
    main()
