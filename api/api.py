import glob
import os
import time
import json
from flask import Flask, request, send_file

app = Flask(__name__)

ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg']


@app.route('/effect<int:number>/upload', methods=['GET', 'POST'])
def upload_file(number):
    if request.method == 'POST':
        input = request.form
        try:
            form = {'filename': input['filename'], 'iterations': input['iterations'], 'privacy': input['privacy']}
        except:
            form = {'filename': input['filename'], 'iterations': input['iterations'], 'privacy': 'n'}
        f = request.files['file']
        if f is None:
            return 'no upload'
        if f.filename.split(".")[-1] not in ALLOWED_EXTENSIONS:
            return 'file not uploaded - extension error'
        else:
            id = str(time.time()).split('.')[0]
            filename = '../imagedb/effect' + str(number) + '_' + id + '.' + f.filename.split(".")[-1]
            f.save(filename)
            os.system('python3 ../effects/japanify.py ' + filename)
            os.remove(
                os.path.join('..', 'imagedb', 'effect' + str(number) + '_' + id + '.' + f.filename.split(".")[-1]))
            link = '<a href=' + '"http://193.136.167.233:5000/images/download/' + id + '">' + 'Download Image' + '</a>' + '<br>'

            return 'file uploaded with ' + id + '\n' + link + str(form)


@app.route('/effect<int:number>/images', methods=['GET'])
def get_images(number):
    return str(glob.glob('../effects_applied/effect' + str(number) + '*'))


@app.route('/images', methods=['GET'])
def get_all_images():
    return str(glob.glob('../effects_applied/*'))


@app.route('/images/download', methods=['GET'])
def show_all_downloadable_images():
    result = ""
    for dir in glob.glob('../effects_applied/*'):
        file_id = dir.split("_")[-1].split(".")[0]
        result += (
                    '<a href=' + '"http://193.136.167.233:5000/images/download/' + file_id + '">' + file_id + '</a>' + '<br>')
    return result


@app.route('/images/download/<int:id>', methods=['GET'])
def download_image(id):
    return send_file(str(glob.glob('../effects_applied/*' + str(id) + '*')[0]))


@app.route('/images/download/effect<int:number>', methods=['GET'])
def show_all_downloadable_images_by_effect(number):
    result = ""
    for dir in glob.glob('../effects_applied/effect' + str(number) + '*'):
        file_id = dir.split("_")[-1].split(".")[0]
        result += (
                    '<a href=' + '"http://193.136.167.233:5000/images/download/' + file_id + '">' + file_id + '</a>' + '<br>')
    return result


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
