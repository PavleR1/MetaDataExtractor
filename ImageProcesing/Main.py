from ExtractMetaData import Extractor
from GetAllImages import GetImages
import os

if __name__ == '__main__':
    url = input('Enter a website url: ')
    dir_location = input('Enter the path of a directory:  ')
    images = GetImages(url, dir_location)
    images.get_all_images_urls()
    print(images.imagesUrls)
    images.download()
    image = os.listdir(images.imageLocation)
    print('Downloaded images: ' + ','.join(image))
    txt_location = input('Enter the path of a txt file: ')
    extractor = Extractor(txt_location)
    for img in image:
        extractor.extract_data(images.imageLocation+'/'+img)
