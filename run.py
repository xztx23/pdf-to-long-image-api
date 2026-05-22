import os
import requests
from PIL import Image
from pdf2image import convert_from_path

def main():
    pdf_url = os.environ.get("PDF_URL")
    if not pdf_url:
        print("未获取PDF链接")
        return

    # 1. 下载并转换 PDF
    try:
        res = requests.get(pdf_url, timeout=20)
        with open("input.pdf", "wb") as f:
            f.write(res.content)
        
        pages = convert_from_path("input.pdf", 150)
        total_h = sum(p.height for p in pages)
        max_w = max(p.width for p in pages)
        long_img = Image.new("RGB", (max_w, total_h))
        y = 0
        for page in pages:
            long_img.paste(page, (0, y))
            y += page.height
        
        long_img.save("output.png")
        print("✅ 图片生成成功")
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        return

    # 2. 自动提交图片到仓库
    try:
        # 配置 git 身份
        os.system('git config --global user.name "github-actions[bot]"')
        os.system('git config --global user.email "github-actions[bot]@users.noreply.github.com"')
        
        # 提交并推送
        os.system('git add output.png')
        os.system('git commit -m "Auto update image" || echo "Nothing to commit"')
        os.system('git push')
        
        print("\n✅ 图片已提交到仓库！")
        print("👉 大模型可直接查看的链接：")
        print("https://raw.githubusercontent.com/xztx23/pdf2img-api/main/output.png")
    except Exception as e:
        print(f"❌ 提交失败: {e}")

if __name__ == "__main__":
    main()
