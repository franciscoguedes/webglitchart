import glob
import json
import os
import time


def generate_folder_id():
    return str(time.time()*10).split('.')[0]

# .json file management


def get_json_content():
    """
    Gets all the data on database.json file
    :return: database.json
    """
    with open(os.path.join('..', 'effects_applied', 'database.json'), 'r') as json_file:
        json_decoded = json.load(json_file)
    return json_decoded


def json_database(folder_id, folder_privacy, filename, effect_number):
    """
    Adds a new entry on database.json file.
    :param folder_id: folder id
    :param filename: final filename
    :param effect_number: effect number
    :return: None
    """
    with open(os.path.join('..', 'effects_applied', 'database.json'), 'r') as json_file:
        json_decoded = json.load(json_file)

    try:
        json_decoded['names'][str(effect_number)]
    except KeyError:
        json_decoded['names'][str(effect_number)] = {}
    json_decoded['names'][str(effect_number)][folder_id] = {'final_file': filename, 'privacy': folder_privacy}

    with open(os.path.join('..', 'effects_applied', 'database.json'), 'w') as json_file:
        json.dump(json_decoded, json_file)


def json_file_setup():
    """
    Checks if database.json already exists, if it doesn't generates a new database.json file
    :return: None
    """
    try:
        open(os.path.join('..', 'effects_applied', 'database.json'), 'r')
    except FileNotFoundError:
        with open(os.path.join('..', 'effects_applied', 'database.json'), 'w') as json_file:
            json.dump({'names': {}}, json_file)


def effect_apply(number, folder_name, filename, dir, form, original_file_name, file_extension):
    """
    Applies an effect to an image a certain number of times. After the final iteration renames the final file to a given
    filename
    :param number: effect number
    :param folder_name: folder name where the image is
    :param filename: image file name
    :param dir: full relative path to image
    :param form: website form input
    :param original_file_name: original image name without the file extension
    :param file_extension: original file extension
    :return: None
    """
    for iteration in range(1, int(form['iterations'])+1):
        #POSSIBLY CAN CHANGE THIS
        working_folder = os.path.join(dir, folder_name, str(number))
        if number == 1:  # japanify
            os.system('python3 ../effects/japanify.py ' + filename +
                      ' --threshold ' + form['density'])
            file_extension = get_last_extension(working_folder)
            filename = os.path.join(dir, folder_name, str(number) + '_' + str(iteration) + '.' + file_extension)
        if number == 2:  # efeito 2
            pass
        if number == 3:  # efeito 3
            pass
        if number == 4:  # efeito 4
            pass

    if form['filename'] != '':
        os.rename(filename, os.path.join(dir, folder_name, form['filename'] + '.' + file_extension))
        return os.path.join(dir, folder_name, form['filename'] + '.' + file_extension)
    else:
        os.rename(filename, os.path.join(dir, folder_name, original_file_name + ' with effect' + '.' + file_extension))
        return os.path.join(dir, folder_name, original_file_name + ' with effect' + '.' + file_extension)


def get_last_extension(folder):
    all_files = []
    for i in glob.glob(os.path.join(folder + '_' + '*')):
        all_files.append(os.path.basename(i))

    all_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
    return get_file_extension(all_files[-1])

def get_number_of_effects():
    """
    Get the number of effects that already are known to the effect_applied folder
    :return: number of effects
    """
    return len(glob.glob(os.path.join('..', 'effects_applied', 'effect*')))


def get_final_images_in_folder(number, id):
    """
    Returns the relative path to the final image from a given folder id
    :param number: effect number to get the final image
    :param id: folder id to get the final image from
    :return: relative path to the final image
    """
    return get_json_content()['names'][str(number)][str(id)]['final_file']


def get_all_effect_images(number):
    """
    Returns a list with all the paths for the final image in a effect folder
    :param number: effect number to get the final images
    :return: list with final images
    """
    database = get_json_content()
    result = {str(number): {}}
    for folder_id in database['names'][str(number)]:
        if database['names'][str(number)][str(folder_id)]['privacy'] == 'y':
            result[str(number)][folder_id] = database['names'][str(number)][str(folder_id)]['final_file']
    return result


def get_folder_privacy_by_id(id):
    """
    Given a folder name returns his privacy
    :param id: folder id
    :return: privacy value
    """
    names = get_json_content()
    for effect_number in range(get_number_of_effects() + 1):
        try:
            return names['names'][effect_number][id]['privacy']
        except KeyError:
            pass


def get_folder_privacy_by_full_path(path):
    """
    Given a full path returns folder's privacy
    :param path: full path to a file inside the folder
    :return: privacy value
    """
    return get_folder_privacy_by_id(path.split(os.sep)[-2])


def get_folder_file_by_id(id):
    """
    Given a folder name returns his final filename
    :param id: folder id
    :return: final image filename
    """
    names = get_json_content()
    for effect_number in range(get_number_of_effects() + 1):
        try:
            return names['names'][effect_number][id]['filename']
        except KeyError:
            pass


def get_file_extension(path):
    return str(os.path.basename(path).split('.')[-1])
