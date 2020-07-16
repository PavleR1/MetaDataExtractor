
from PIL import Image
from PIL.ExifTags import TAGS


def is_jpg(imageLocation):
    """Check if image is in jpg format"""
    return imageLocation[-4:] == '.jpg'


class Extractor:
    def __init__(self,  file_location):
        self.fileLocation = file_location

    def extract_data(self, imageLocation):
        if not is_jpg(imageLocation):
            print('Error: ' + imageLocation.split('/')[-1]+' is not a jpg format!!')
            return
        # setting default txt file
        self.fileLocation = self.fileLocation if (self.fileLocation and isinstance(self.fileLocation, str))\
            else '/'.join(imageLocation.split('/')[:-1])+'/MetaData.txt'
        image = Image.open(imageLocation)
        image_meta_data = image.getexif()
        with open(self.fileLocation, 'a') as f:
            f.write(imageLocation.split('/')[-1]+':\n')
            print(imageLocation.split('/')[-1]+':\n')
            for tag_id in image_meta_data:
                # get the tag name, instead of human unreadable tag id
                tag = TAGS.get(tag_id, tag_id)
                data = image_meta_data.get(tag_id)
                # decode bytes
                if isinstance(data, bytes):
                    data = data.decode()
                f.write(f"\t {tag:25}: {data} \n")
                print(f"\t {tag:25}: {data} \n")
            f.write('-'*100+'\n')
