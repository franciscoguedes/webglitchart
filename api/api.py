import glob
import os
import time
from flask import Flask, request, send_file
import json
app = Flask(__name__)

ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg']


@app.route('/effect<int:number>/upload', methods=['GET', 'POST'])
def upload_file(number):
    if request.method == 'POST':
        input = request.form
        file = request.files['file']

        file_extension = file.filename.split(".")[-1]
        original_file_name = os.path.basename(file.filename).replace('.' + file_extension, '')
        dir = os.path.join('..', 'effects_applied', 'effect_' + str(number))

        if file_extension not in ALLOWED_EXTENSIONS:
            return 'file not uploaded - extension error'

        else:
            folder_id = generate_folder_id()

            try:
                folder_name = folder_id + "_" + input['privacy']
            except KeyError:
                folder_name = folder_id + "_n"

            os.makedirs(os.path.join(dir, folder_name))

            filename = os.path.join(dir, folder_name, str(number) + '_' + '0' + '.' + file_extension)
            file.save(filename)

            effect_apply(number, folder_name, filename, dir, input, original_file_name, file_extension)

            json_name_manager(folder_id, input['filename'], number)

            link = '<a href=' + '"http://0.0.0.0:5000/images/download/' + folder_name + '">' + 'Download Image' + '</a>' + '<br>'
            return 'file uploaded with folder id' + folder_id + '\n' + link + '\n' + str(input)


@app.route('/effect<int:number>/images', methods=['GET'])
def get_effect_images(number):
    dict = get_dict_image(number)
    link = ''
    for key in dict:
        link += '<a href="http://0.0.0.0:5000/images/download/' + dict[key] + '">' + str(key) + '</a> <br>'
    return link


@app.route('/images', methods=['GET'])
def get_all_images():
    result = ''
    for i in range(1, 6):
        result += get_effect_images(i)
    return result

@app.route('/images/download', methods=['GET'])
def show_all_downloadable_images():
    result = ""
    for dir in glob.glob('../effects_applied/*'):
        file_id = dir.split("_")[-1].split(".")[0]
        result += ('<a href=' + '"http://193.136.167.233:5000/images/download/' + file_id + '">' + file_id + '</a>' + '<br>')
    return result


#@app.route('/images/download/<int:id>', methods=['GET'])
#def download_image(id):
    #final_dict = {}
    #for effect_number in range(1, get_number_of_effects()+1):
    #return send_file(str(glob.glob('../effects_applied/' + str(id) + '_*')[0]))


def generate_folder_id():
    return str(time.time()*10).split('.')[0]


def get_json_content():
    with open(os.path.join('..', 'effects_applied', 'name_manager.json'), 'r') as json_file:
        json_decoded = json.load(json_file)
    return json_decoded


def json_name_manager(folder_id, filename, effect_number):
    with open(os.path.join('..', 'effects_applied', 'name_manager.json'), 'r') as json_file:
        json_decoded = json.load(json_file)

    json_decoded['names'][folder_id] = [effect_number, filename]

    with open(os.path.join('..', 'effects_applied', 'name_manager.json'), 'w') as json_file:
        json.dump(json_decoded, json_file)


def effect_apply(number, folder_name, filename, dir, form, original_file_name, file_extension):
    for iteration in range(1, int(form['iterations'])+1):
        #POSSIBLY CAN CHANGE THIS
        all_files = []
        for i in glob.glob(os.path.join(dir, folder_name, str(number) + '_' + '*')):
            all_files.append(os.path.basename(i))
        #
        all_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
        file_extension = str(all_files[-1]).split('.')[-1]

        if number == 1:  # japanify
            os.system('python3 ../effects/japanify.py ' + filename +
                      ' --threshold ' + form['density'])

            filename = os.path.join(dir, folder_name, str(number) + '_' + str(iteration) + '.' + file_extension)
        if number == 2:  # efeito 2
            pass
        if number == 3:  # efeito 3
            pass
        if number == 4:  # efeito 4
            pass

    try:
        os.rename(filename, os.path.join(dir, folder_name, form['filename'] + '.' + file_extension))

    except KeyError:
        os.rename(filename, os.path.join(dir, folder_name, original_file_name + '.' + file_extension))


def json_file_setup():
    try:
        open(os.path.join('..', 'effects_applied', 'name_manager.json'), 'r')
    except FileNotFoundError:
        with open(os.path.join('..', 'effects_applied', 'name_manager.json'), 'w') as json_file:
            json.dump({'names': {}}, json_file)


def get_number_of_effects():
    return len(glob.glob(os.path.join('..', 'effects_applied'))) - 1


def get_final_images_in_dir(number):
    all_files = glob.glob(os.path.join('..', 'effects_applied', 'effect_' + str(number), '*' + '_y', '*'))
    names = get_json_content()
    result = []
    for file in all_files:
        for id in names["names"].keys():
            if os.path.basename(file).split('.')[0] in names['names'][id] and file not in result:
                result.append(file)
    return result


def get_dict_image(number):
    images = get_final_images_in_dir(number)
    dict = {}
    for image in images:
        folder_name = image.split(os.sep)[-2]
        folder_privacy = folder_name.split('_')[-1]
        if folder_privacy == 'y':
            dict[os.path.basename(image).split('.')[0]] = str(folder_name)
    return dict

if __name__ == "__main__":
    json_file_setup()
    app.run(debug=True, host='0.0.0.0')
