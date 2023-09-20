from flask import Flask, request, jsonify
import logging
import traceback
from vertexai.vision_models._vision_models import Image, ImageCaptioningModel, ImageQnAModel
import os
import sys

app = Flask(__name__)

# Exception Handling Setup
def custom_excepthook(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.error("An uncaught exception occurred:")
    logging.error("Type: %s", exc_type)
    logging.error("Value: %s", exc_value)

    if exc_traceback:
        format_exception = traceback.format_tb(exc_traceback)
        for line in format_exception:
            logging.error(repr(line))

sys.excepthook = custom_excepthook

# Initialize Models
model = ImageCaptioningModel.from_pretrained("imagetext@001")
model2 = ImageQnAModel.from_pretrained("imagetext@001")

@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        try:
            image_file = request.files.get('image')
            if not image_file:
                return jsonify({"error": "Image not provided"}), 400

            # Save the image temporarily to process
            filepath = f"/tmp/{image_file.filename}"
            image_file.save(filepath)

            captions = get_captions(filepath)
            objects = get_objects(filepath)
            colors = get_colors(filepath)

            joined_captions = ", and ".join(captions)
            joined_objects = ", and ".join(objects)
            joined_colors = ", and ".join(colors)
            combined_text = f"This image shows {captions}. The colors are {joined_colors}. The visible objects are {joined_objects}."

            return jsonify({"captions": combined_text}), 200
        except Exception as e:
            stack_trace = traceback.format_exc()
            logging.error(f"Error during processing: {e}\n{stack_trace}")
            return jsonify({"error": "Internal server error"}), 500

def get_objects(filename):
    image = Image.load_from_file(filename)
    objects = model2.ask_question(
        image=image,
        question="what objects are in this image?",
        number_of_results=1,
    )
    return objects

def get_colors(filename):
    image = Image.load_from_file(filename)
    colors = model2.ask_question(
        image=image,
        question="what colors are in this image?",
        number_of_results=1,
    )
    return colors

def get_captions(filename):
    image = Image.load_from_file(filename)
    captions = model.get_captions(
        image=image,
        number_of_results=1,
        language="en",
    )
    return captions[0]

if __name__ == '__main__':
    app.run(debug=True, port=5000)
