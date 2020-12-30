import cv2 as cv
import numpy as np
import os
from app import app
from collections import Counter
import urllib.request
from recognition import E2E
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import  base64

model = E2E()
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
OUTPUT_FOLDER = 'static/output'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img = cv.imread('static/uploads/'+filename)
        (img,so) = model.predict(img)
        filename = 'out_'+filename
        cv.imwrite('static/output/'+filename,img)
        flash('Ảnh Đã Được Tải lên và nhận diện')
        return render_template('index.html', filename=filename,foobar=so)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename = 'output/'+filename) ,code=301)


if __name__ == "__main__":
    app.run()