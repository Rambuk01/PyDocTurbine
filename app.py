import functions
import create_docx
import os
import pprint

TESTING = True

def app():
    # Main flow

    if TESTING: path = os.getcwd()
    else: path = functions.select_folder(initial_folder=os.getcwd())

    # Get all images in the primary folder. Can also use something to find the folder. Perhaps tkinter or alike.
    # Also index all images. Perhaps with dict.
    images = functions.load_images(path)

    # GET ALL INFO FROM THE IMAGES:
    image_info_list = functions.get_image_info_list(images, path)

    # Write text on all images -> Create new images. Keep old images. Create folders for old and new images. Add ID to all images. Perhaps also old images.
    new_image_list = functions.process_images(image_info_list, path=path)
    # Insert images into wordtable or excel table
    # Either load images from a specfic dir. Or Just use new image list.

    # Load template document
    doc = create_docx.load_document(path = f"{path}/report_template/Report_Serration_inspection_replacement_Altenheimer_WTG03_ 000519_30.07.24.docx")
    
    section_data = functions.load_section_data()
    create_docx.add_images_with_captions(doc, new_image_list, section_data = section_data)

    # Insert table into base template.



if __name__ == '__main__':
    app()