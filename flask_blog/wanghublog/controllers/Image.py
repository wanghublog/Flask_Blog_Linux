from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random


# 随机字母:
def rndChar():
    return chr(random.randint(65, 90))


# 随机颜色1:
def rndColor():

    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


# 随机颜色2:
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


def validate_picture():
    # 130 x 50:
    width = 130
    height = 50
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    font = ImageFont.truetype('arial.ttf', 36)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())
    # 输出文字:
    strs = ''
    for t in range(4):
        str = rndChar()
        draw.text((30 * t + 10, 10), str, font=font, fill=rndColor2())
        str = strs + str
    # 模糊:
    im = image.filter(ImageFilter.BLUR)
    
    #root_dir = os.path.abspath('.')
    #img_path = root_dir + '\static' + '\image' + '\code.jpg'
    #image.save('code.jpg', 'jpeg')

    return im,str

if __name__ == '__main__':
    creat_str_image()


