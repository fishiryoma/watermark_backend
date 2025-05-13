from PIL import Image, ImageDraw, ImageFont
from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
from io import BytesIO

app = Flask(__name__)
CORS(app, expose_headers=["Content-Disposition"])

@app.route("/api/watermark", methods=["POST"])
def add_watermarker():
    try:
        # 浮水印設置參數
        text = str(request.form.get("text", "watermark" ))
        p_x = int(request.form.get("x", 10))
        p_y = int(request.form.get("y", 10))
        font_size = int(request.form.get('font', 36))
        color = request.form.get("color", "white")

        if "file" not in request.files:
            return jsonify({"error": "No Image"}), 400

        file = request.files.get("file")
        if file.filename == "":
            return jsonify({"error": "Invalid Image"}), 400

        # 確認文件的 MIME 類型為圖片
        if not file.content_type.startswith("image/"):
            return jsonify({"error": "Invalid file type. Please upload an image format."}), 400

        image = Image.open(file)
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except OSError:
            font = ImageFont.load_default()

        image_width, image_height = image.size
        bbox = draw.textbbox((0,0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        # print(p_y, int(image_height - text_height - text_height/2))
        p_x = min(p_x, int(image_width - text_width))
        p_y = min(p_y, int(image_height - text_height - text_height/2))
        position = (p_x, p_y)
        # print(position)
        draw.text(position, text, font=font, fill=color)

        # 在記憶體中暫存圖片
        img_io = BytesIO()
        output_format = file.content_type.split("/")[-1].upper()
        # print(file.content_type)
        if output_format not in ["JPEG", "PNG"]:
            output_format = "JPEG"
        image.save(img_io, "JPEG")
        img_io.seek(0)
        return send_file(img_io, mimetype=file.content_type, as_attachment=True,
                         download_name=f"watermarker_{file.filename}")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)