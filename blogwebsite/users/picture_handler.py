#file that allows us to upload pictures to the website
import os
from PIL import Image
from flask import url_for, current_app

def add_profile_pic(pic_upload, username):
    filename = pic_upload.filename  #filename of the picture
    ext_type = filename.split('.')[-1]  #extension type png or jpg
    storage_filename = str(username) + '.' + ext_type  #username.png

    filepath = os.path.join(current_app.root_path, 'static\profile_pics', storage_filename)  #filepath to save the picture
    #example filepath: C:\Users\user\Documents\Python\Flask\blogwebsite\static\profile_pics\username.png

    output_size = (200,200)  #size of the picture

    pic = Image.open(pic_upload)  #open the picture
    pic.thumbnail(output_size)  #thumbnail is a PIL method which allows us to resize the picture
    pic.save(filepath)  #save the picture to the filepath
    return storage_filename