import os
import requests
from PIL import Image
from pdf2image import convert_from_path

def main():
    # 1. 从环境变量获取 PDF 链接和仓库信息
    pdf_url = os.environ.get("PDF_URL")
    github_token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    branch = "main"

    if not pdf_url or not github_token or not repo:
        print("::error::环境变量缺失")
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

        total_height = sum(page.height for page in pages)
        max_width = max(page.width for page in pages)
        long_img = Image.new("RGB", (max_width, total_height))

        y_pos = 0
        for page in pages:
            long_img.paste(page, (0, y_pos))
            y_pos += page.height

        # 保存图片到仓库根目录
        img_path = "long_image.png"
        long_img.save(img_path)
        print("✅ 长图生成完成")

        # 4. 直接上传图片到 GitHub 仓库
        with open(img_path, "rb") as f:
            img_data = f.read()

        # 上传接口
        api_url = f"https://api.github.com/repos/{repo}/contents/{img_path}"
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        # 获取文件的 sha（如果文件不存在，第一次上传时不需要）
        get_res = requests.get(api_url, headers=headers)
        sha = get_res.json().get("sha") if get_res.status_code == 200 else None

        # 上传文件
        data = {
            "message": "Update long image",
            "content": img_data.hex(),
            "branch": branch
        }
        if sha:
            data["sha"] = sha

        upload_res = requests.put(api_url, headers=headers, json=data)
        if upload_res.status_code in [200, 201]:
            # 生成图片的 raw.githubusercontent.com 链接
            image_url = f"https://raw.githubusercontent.com/{repo}/{branch}/{img_path}"
            print(f"\n✅ 图片上传成功！\n")
            print(f"![PDF长图]({image_url})")
        else:
            print(f"❌ 上传失败，错误：{upload_res.text}")

    except Exception as e:
        print(f"::error::转换或上传出错: {e}")

if __name__ == "__main__":
    main()
