from PIL import Image, ImageDraw, ImageFont
from flask import Flask, send_file
from io import BytesIO

app = Flask(__name__)

test_img = "images/icon.jpg"
text = "TESS TEST"

def add_watermarker(input_img):
    image = Image.open(input_img)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 36)

    bbox = draw.textbbox((0,0), text, font=font)
    # text_width = bbox[2] - bbox[0]
    # text_height = bbox[3] - bbox[1]
    position = (10, 10)

    draw.text(position, text, font=font, fill=(255, 255, 255))

    img_io = BytesIO()
    image.save(img_io, "JPEG")
    img_io.seek(0)

    return img_io

# add_watermarker(test_img)

@app.route("/")
def home():
    img_io = add_watermarker(test_img)
    return send_file(img_io, mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(debug=True)