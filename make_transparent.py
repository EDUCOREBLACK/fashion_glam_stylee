from PIL import Image

def make_transparent(image_path):
    try:
        img = Image.open(image_path)
        img = img.convert("RGBA")
        datas = img.getdata()

        newData = []
        # Any near-white pixel becomes fully transparent
        for item in datas:
            if item[0] >= 240 and item[1] >= 240 and item[2] >= 240:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        img.putdata(newData)
        img.save(image_path, "PNG")
        print("Logo hecho transparente con exito.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    make_transparent('static/img/logo.png')
