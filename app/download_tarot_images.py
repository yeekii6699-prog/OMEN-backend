#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载塔罗牌图片到本地
"""
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import os
import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# 路径配置
FRONTEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
PUBLIC_DIR = os.path.join(FRONTEND_DIR, "frontend", "public", "images", "tarot")
TAROT_DATA_FILE = os.path.join(FRONTEND_DIR, "frontend", "src", "constants", "tarotData.js")

# 图片源
BASE_URL = "https://cdn.tarotqa.com/images-optimized/tarot"

def create_directories():
    """创建目录"""
    os.makedirs(PUBLIC_DIR, exist_ok=True)
    print(f"📁 图片目录: {PUBLIC_DIR}")

def get_tarot_data():
    """读取tarotData.js提取所有图片URL"""
    with open(TAROT_DATA_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取所有 image URL
    urls = []
    for line in content.split('\n'):
        if 'image:' in line:
            # 提取URL
            start = line.find('https://')
            end = line.find('.webp') + 5
            if start != -1:
                url = line[start:end]
                # 提取文件名
                filename = url.split('/')[-1]
                urls.append({'url': url, 'filename': filename})
    return urls

def download_image(item):
    """下载单张图片"""
    url, filename = item['url'], item['filename']
    filepath = os.path.join(PUBLIC_DIR, filename)

    # 如果已存在，跳过
    if os.path.exists(filepath):
        print(f"  ⏭️ 已存在: {filename}")
        return filename, True

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"  ✅ 下载成功: {filename}")
        return filename, True
    except Exception as e:
        print(f"  ❌ 下载失败: {filename} - {e}")
        return filename, False

def update_tarot_data():
    """更新tarotData.js使用本地路径"""
    with open(TAROT_DATA_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换URL为本地路径
    old_pattern = 'image: "https://cdn.tarotqa.com/images-optimized/tarot/'
    new_pattern = 'image: "/images/tarot/'
    content = content.replace(old_pattern, new_pattern)
    content = content.replace('.webp"', '.webp"')

    with open(TAROT_DATA_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n🔄 已更新 tarotData.js 使用本地路径")

def main():
    print("=" * 50)
    print("🃏 塔罗牌图片下载器")
    print("=" * 50)

    create_directories()

    # 获取所有图片URL
    urls = get_tarot_data()
    print(f"\n📦 共有 {len(urls)} 张图片需要下载\n")

    # 下载所有图片
    success_count = 0
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(download_image, urls)
        for filename, success in results:
            if success:
                success_count += 1

    print(f"\n✅ 成功下载 {success_count}/{len(urls)} 张图片")

    # 更新数据文件
    update_tarot_data()

    print("\n✨ 完成!")
    print(f"\n📂 图片位置: {PUBLIC_DIR}")
    print("📝 现在使用本地路径，无需外网访问")

if __name__ == "__main__":
    main()
