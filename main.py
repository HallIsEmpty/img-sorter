# Python script using Flask

from flask import Flask, render_template, request, send_file, jsonify, send_from_directory
import os
import shutil
import tkinter as tk
from tkinter import filedialog
import logging
import sys

#app = Flask(__name__)
app = Flask(__name__, static_folder='vueapp/dist')

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def select_folder(message):
    # Create and hide the root window
    root = tk.Tk()
    root.withdraw()

    # Show the folder selection dialog and store the selected folder path
    folder_path = filedialog.askdirectory()

    # Check if a folder was selected
    if folder_path:
        # print(f"Selected folder: {folder_path}")
        return folder_path
        # You can now use folder_path in your script, for example, to list files
    else:
        print("No folder was selected.")
        raise "problem"


def main():

    # image_folder = r'C:\mega\midjourney photoshop etsy\clipart\cats and plants'
    # image_folder = r'/Users/mhall/personal/mega shared everywhere/midjourney photoshop etsy/clipart/forest creatures'
    # image_folder = "C:\\mega\\midjourney photoshop etsy\\clipart\\vintage travel"
    series_name = input("Enter a series name string (e.g. penguins_s1): ")


    images_path = select_folder("select main path to image work")

    image_folder = 'originals'

    @app.route('/')
    def serve_vue_app():
        # return jsonify(app.static_folder)
       print('hi')
       return send_from_directory(app.static_folder, 'index.html')


    # @app.route('/')
    # def index():
    #     images = os.listdir(os.path.join(images_path, image_folder))
    #     for filename in os.listdir(os.path.join(images_path, image_folder)):
    #         print(filename)
        # for filename in os.listdir(IMAGE_DIRS[0]):
        #     image_info = {'filename': filename, 'path1': f'version1/{filename}', 'path2': f'version2/{filename}', 'path3': f'version3/{filename}'}
        #     image_list.append(image_info)

        # return image_list


        # print(images)
        # template_dir = os.path.abspath(os.path.dirname(__file__))
        # print('template_dir', template_dir)
        # template_path = os.path.join(template_dir, 'image_compare.html')
        # print('template_path', template_path)
        # return render_template(template_path, images=images)
        # return render_template('image_sort.html', images=images, series_name=series_name)

    @app.route('/initialfiles')
    def initialfiles():
        print('hi2')
        retval = {'one': [], 'two': []}
        for filename in os.listdir(os.path.join(images_path, 'clipdrop')):
            retval['one'].append({"src": os.path.join('images','clipdrop',filename), "name": filename})
        for filename in os.listdir(os.path.join(images_path, 'upsized')):
            retval['two'].append({"src": os.path.join('images','upsized',filename), "name": filename})
        return jsonify(retval)

    @app.route('/images/<path:folder_name>/<path:image_name>')
    def get_image(folder_name, image_name):
        print('hi3')
        print("image name", image_name)
        print("folder_name", folder_name)
        # global images_path
        # image_path = images_path,  folder_name , image_name
        image_path = os.path.join(images_path,  folder_name , image_name)
        print("image_path", image_path)
        return send_file(image_path)

    @app.route('/<path:path>')
    def serve_vue_assets(path):
        print(f'looking for {path}', flush=True)
        # Add MIME type handling here if necessary
        return send_from_directory(app.static_folder, path)


    @app.route('/submit', methods=['POST'])
    def submit():
        data = request.get_json()
        print(data['imageselection']['one'])
        print(data['imageselection']['two'])

        imagecounter = 1
        for file in data['imageselection']['one']:
            print(f"moving {file["name"]} to {series_name}/{imagecounter}")


            file_name, file_extension = os.path.splitext(os.path.join(images_path,  'clipdrop' , file["name"]))  
            imagecounterstr = f'{imagecounter:03}'
            new_filename = f'{series_name}_{imagecounterstr}{file_extension}'
            print(os.path.join(images_path,  'clipdrop' , file["name"]), f' should go from folder one to clipdrop/{new_filename}')
            os.rename(os.path.join(images_path, 'clipdrop', file["name"]), os.path.join(images_path, 'clipdrop', new_filename))
            imagecounter += 1


        imagecounter = 1
        for file in data['imageselection']['two']:
            print(f"moving {file["name"]} to {series_name}/{imagecounter}")


            file_name, file_extension = os.path.splitext(os.path.join(images_path,  'upsized' , file["name"]))  
            imagecounterstr = f'{imagecounter:03}'
            new_filename = f'{series_name}_{imagecounterstr}{file_extension}'
            print(os.path.join(images_path,  'upsized' , file["name"]), f' should go from folder one to upsized/{new_filename}')
            os.rename(os.path.join(images_path, 'upsized', file["name"]), os.path.join(images_path, 'upsized', new_filename))
            imagecounter += 1



        return {'success': True}
        imageselection3 = request.form.getlist('imageselection[]')
        # print("imageselectionone copy from originals to handcrafted", request.form.getlist('imageselectionone[]'))
        # print("imageselectiontwo copy from photoshop to selected", request.form.getlist('imageselectiontwo[]'))
        # print("imageselectionthree copy from clipdrop to selected", request.form.getlist('imageselectionthree[]'))
        # print("promote bump to front of queue", request.form.getlist('promote[]'))
        # print("imagereworktwo copy from photoshop to handcrafted AND copy from originals to handcrafted with namechange", request.form.getlist('imagereworktwo[]'))
        # print("imagereworkthree copy from clipdrop to handcrafted AND copy from originals to handcrafted with namechange", request.form.getlist('imagereworkthree[]'))
        # selected_image = request.form['selected_image']
        # new_filename = request.form['new_filename']
        
        # # Rename the selected image if the filename is changed
        # if new_filename:
        #     os.rename(selected_image, os.path.join('new_folder', new_filename))
        promotedcount = len(request.form.getlist('promote[]'))
        imagecounter = promotedcount + 1
        # for img in request.form.getlist('imageselectionone[]'):
        #     file_name, file_extension = os.path.splitext(os.path.basename(img))
        #     imagecounterstr = f'{imagecounter:03}'
        #     new_filename = f'{series_name}_{imagecounterstr}{file_extension}'
        #     print( os.path.join(image_folder, 'originals', img), f' should go from folder one to final/{new_filename}')
        #     shutil.copy(os.path.join(image_folder, 'originals', img), os.path.join(image_folder, 'final', img))
        #     os.rename(os.path.join(image_folder, 'final', img), os.path.join(image_folder, 'final', new_filename))
        #     imagecounter += 1
        for img in request.form.getlist('imageselectiontwo[]'):
            file_name, file_extension = os.path.splitext(os.path.basename(img))
            imagecounterstr = f'{imagecounter:03}'
            new_filename = f'{series_name}_{imagecounterstr}{file_extension}'
            print(os.path.join(images_path, 'photoshop', img), f' should go from folder one to ', os.path.join(images_path, 'selected', img))
            shutil.copy(os.path.join(images_path, 'photoshop', img), os.path.join(images_path, 'selected', img))
            os.rename(os.path.join(images_path, 'selected', img), os.path.join(images_path, 'selected', new_filename))
            imagecounter += 1
        for img in request.form.getlist('imageselectionthree[]'):
            file_name, file_extension = os.path.splitext(os.path.basename(img))
            imagecounterstr = f'{imagecounter:03}'
            new_filename = f'{series_name}_{imagecounterstr}{file_extension}'
            print(os.path.join(images_path, 'clipdrop', img), f' should go from folder one to final/{new_filename}')
            shutil.copy(os.path.join(images_path, 'clipdrop', img), os.path.join(images_path, 'selected', img))
            os.rename(os.path.join(images_path, 'selected', img), os.path.join(images_path, 'selected', new_filename))
            imagecounter += 1
        for img in request.form.getlist('imagereworktwo[]'):
            file_name, file_extension = os.path.splitext(os.path.basename(img))
            imagecounterstr = f'{imagecounter:03}'
            new_filename = f'{series_name}_{imagecounterstr}{file_extension}'
            print(os.path.join(images_path, 'photoshop', img), f' should go from folder one to ', os.path.join(images_path, 'handcrafted', img))
            shutil.copy(os.path.join(images_path, 'photoshop', img), os.path.join(images_path, 'handcrafted', img))
            os.rename(os.path.join(images_path, 'handcrafted', img), os.path.join(images_path, 'handcrafted', new_filename))
            shutil.copy(os.path.join(images_path, 'originals', img), os.path.join(images_path, 'handcrafted', img))
            imagecounter += 1
        for img in request.form.getlist('imagereworkthree[]'):
            file_name, file_extension = os.path.splitext(os.path.basename(img))
            imagecounterstr = f'{imagecounter:03}'
            new_filename = f'{series_name}_{imagecounterstr}{file_extension}'
            print(os.path.join(images_path, 'clipdrop', img), f' should go from folder one to ', os.path.join(images_path, 'handcrafted', img))
            shutil.copy(os.path.join(images_path, 'clipdrop', img), os.path.join(images_path, 'handcrafted', img))
            os.rename(os.path.join(images_path, 'handcrafted', img), os.path.join(images_path, 'handcrafted', new_filename))
            shutil.copy(os.path.join(images_path, 'originals', img), os.path.join(images_path, 'handcrafted', img))
            imagecounter += 1

        # Copy the selected image to a new folder
        return 'Image saved successfully!'



    app.run(debug=True, use_reloader=False)


if __name__ == '__main__':
    main()
