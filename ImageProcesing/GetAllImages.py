import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse


def is_valid(url):
    """ Check if url is valid """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


class GetImages:
    imageNames = list()
    imagesUrls = list()
    buffer_size = 1024

    def __init__(self, web_site_url, image_location):
        # Constructor that initialize Url of a website with Images and path for dir where we will storage this images
        self.webSiteUrl = web_site_url if is_valid(web_site_url) else \
            'http://www.fon.bg.ac.rs/?type=3'
        # Default dir will be Downloads dir on your machine
        self.imageLocation = image_location if (os.path.isdir(image_location) and image_location) \
            else os.path.join(os.environ.get('HOME'), 'Downloads')

    def get_all_images_urls(self):
        soup = bs(requests.get(self.webSiteUrl).content, "html.parser")
        # Run through the every img tag in parsed html file and extracting value of src tag
        for img in tqdm(soup.find_all("img"), "Extracting images"):
            img_url = img.attrs.get("src")
            if not img_url:
                # if img does not contain src attribute, just skip
                continue
            img_url = urljoin(self.webSiteUrl, img_url)
            try:
                pos = img_url.index("?")
                img_url = img_url[:pos]
            except ValueError:
                pass
            if is_valid(img_url):
                self.imagesUrls.append(img_url)
        return self.imagesUrls

    def download(self):
        if not self.imagesUrls:
            print('Error : Access denied or There are no images on this site')
            return
        for url in self.imagesUrls:
            # if path doesn't exist, make that path dir
            if not os.path.isdir(self.imageLocation):
                os.makedirs(self.imageLocation)
            # download the body of response by chunk, not immediately
            response = requests.get(url, stream=True)
            # get the total file size
            file_size = int(response.headers.get("Content-Length", 0))
            # get the file name
            filename = os.path.join(self.imageLocation, url.split("/")[-1])
            self.imageNames.append(filename)  # if filename[-4:] == '.jpg' else filename+'.jpg'
            # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
            progress = tqdm(response.iter_content(self.buffer_size), f"Downloading {filename}", total=file_size,
                            unit="B",  unit_scale=True, unit_divisor=1024)
            with open(filename, "wb") as f:
                for data in progress:
                    # write data read to the file
                    f.write(data)
                    # update the progress bar manually
                    progress.update(len(data))
