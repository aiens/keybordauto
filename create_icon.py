#!/usr/bin/env python3
"""
创建应用图标
"""

from PIL import Image, ImageDraw
import os


def create_icon():
    """创建应用图标"""
    # 创建256x256的图标
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 背景圆形
    margin = 20
    draw.ellipse([margin, margin, size-margin, size-margin], 
                fill=(70, 130, 180, 255), outline=(30, 90, 140, 255), width=4)
    
    # 键盘图标 - 绘制键盘轮廓
    kb_margin = 60
    kb_width = size - 2 * kb_margin
    kb_height = kb_width * 0.4
    kb_y = (size - kb_height) // 2
    
    # 键盘主体
    draw.rounded_rectangle([kb_margin, kb_y, kb_margin + kb_width, kb_y + kb_height],
                          radius=8, fill=(240, 240, 240, 255), outline=(200, 200, 200, 255), width=2)
    
    # 绘制按键
    key_size = 16
    key_margin = 8
    rows = 3
    cols = 8
    
    start_x = kb_margin + 15
    start_y = kb_y + 15
    
    for row in range(rows):
        for col in range(cols):
            if row == 2 and col >= 6:  # 最后一行少几个键
                break
            
            x = start_x + col * (key_size + key_margin)
            y = start_y + row * (key_size + key_margin)
            
            # 按键
            draw.rounded_rectangle([x, y, x + key_size, y + key_size],
                                 radius=2, fill=(220, 220, 220, 255), outline=(180, 180, 180, 255))
    
    # 空格键
    space_width = key_size * 3
    space_x = start_x + 2 * (key_size + key_margin)
    space_y = start_y + 2 * (key_size + key_margin)
    draw.rounded_rectangle([space_x, space_y, space_x + space_width, space_y + key_size],
                         radius=2, fill=(220, 220, 220, 255), outline=(180, 180, 180, 255))
    
    # 保存不同格式的图标
    assets_dir = 'assets'
    os.makedirs(assets_dir, exist_ok=True)
    
    # PNG格式
    img.save(os.path.join(assets_dir, 'icon.png'), 'PNG')
    print("Created icon.png")
    
    # ICO格式 (Windows)
    try:
        # 创建多尺寸ICO
        sizes = [16, 32, 48, 64, 128, 256]
        ico_images = []
        for s in sizes:
            ico_img = img.resize((s, s), Image.Resampling.LANCZOS)
            ico_images.append(ico_img)
        
        ico_images[0].save(os.path.join(assets_dir, 'icon.ico'),
                          format='ICO', sizes=[(s, s) for s in sizes])
        print("Created icon.ico")
    except Exception as e:
        print(f"Failed to create ICO file: {e}")
    
    # ICNS格式 (macOS) - 需要额外的库
    try:
        # 简单方法：保存为PNG，然后用系统工具转换
        icns_png = img.resize((512, 512), Image.Resampling.LANCZOS)
        icns_png.save(os.path.join(assets_dir, 'icon_512.png'), 'PNG')
        print("Created icon_512.png (can be used to convert to ICNS)")
        
        # 如果有iconutil命令，尝试创建ICNS
        import subprocess
        try:
            # 创建iconset目录结构
            iconset_dir = os.path.join(assets_dir, 'icon.iconset')
            os.makedirs(iconset_dir, exist_ok=True)
            
            # 创建不同尺寸的图标
            icns_sizes = [16, 32, 128, 256, 512]
            for s in icns_sizes:
                icns_img = img.resize((s, s), Image.Resampling.LANCZOS)
                icns_img.save(os.path.join(iconset_dir, f'icon_{s}x{s}.png'), 'PNG')
                # 2x版本
                icns_img_2x = img.resize((s*2, s*2), Image.Resampling.LANCZOS)
                icns_img_2x.save(os.path.join(iconset_dir, f'icon_{s}x{s}@2x.png'), 'PNG')
            
            # 使用iconutil创建ICNS
            subprocess.run(['iconutil', '-c', 'icns', iconset_dir, '-o',
                          os.path.join(assets_dir, 'icon.icns')], check=True)
            print("Created icon.icns")
            
            # 清理临时目录
            import shutil
            shutil.rmtree(iconset_dir)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("iconutil not available, skipping ICNS creation")

    except Exception as e:
        print(f"Failed to create ICNS file: {e}")


if __name__ == "__main__":
    create_icon()
