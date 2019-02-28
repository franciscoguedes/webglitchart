from flask import Flask, request, send_file
from api.aux_functions import *
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
def show_all_downloadable_images():
    result = ''
    number_of_effects = get_number_of_effects()
    for i in range(1, number_of_effects + 1):
        result += 'EFFECT ' + str(i) + '<br>' + get_effect_images(i)
    return result


@app.route('/images/download/<int:id>', methods=['GET'])
def download_image(id):
    pass

if __name__ == "__main__":
    json_file_setup()
    app.run(debug=True, host='0.0.0.0')
