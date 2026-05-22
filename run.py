import os
import io
import base64
import requests
from PIL import Image
from pdf2image import convert_from_path

def main():
    # 1. 从环境变量获取 PDF 链接
    pdf_url = os.environ.get("PDF_URL")
    if not pdf_url:
        print("::error::未获取到 PDF_URL 环境变量")
        return

    # 2. 下载 PDF 文件
    pdf_path = "input.pdf"
    try:
        res = requests.get(pdf_url, timeout=30)
        res.raise_for_status()
        with open(pdf_path, "wb") as f:
            f.write(res.content)
        print("✅ PDF 下载成功")
    except Exception as e:
        print(f"::error::PDF下载失败: {e}")
        return

    # 3. PDF 转图片并拼接成长图
    try:
        print("开始转换 PDF...")
        pages = convert_from_path(pdf_path, dpi=150)
        print(f"转换完成，共 {len(pages)} 页")

        # 计算长图尺寸
        total_height = sum(page.height for page in pages)
        max_width = max(page.width for page in pages)
        long_img = Image.new("RGB", (max_width, total_height))

        # 拼接图片
        y_pos = 0
        for page in pages:
            long_img.paste(page, (0, y_pos))
            y_pos += page.height

        # 4. 把图片转成 Base64 编码
        print("转换完成，准备编码...")
        img_buffer = io.BytesIO()
        long_img.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        base64_img = base64.b64encode(img_buffer.read()).decode("utf-8")

        # 关键：直接在日志里打印 Base64 图片（大模型能直接识别）
        print(f"\n✅ 图片生成成功！Base64 编码如下：\n")
        print(f"data:image/png;base64,{base64_img}")

    except Exception as e:
        print(f"::error::转换出错: {e}")

if __name__ == "__main__":
    main()
