from PIL import Image
import numpy as np
import io
import ee

class PrecorsiaGee:
    def __init__(self, dataset, rangeset, margin=50):
        self.dataset = dataset
        self.rangeset = rangeset
        self.margin = margin

    def init(self):
        ee.Initialize()

    def initLogin(self):
        ee.Authenticate()
        ee.Initialize()

    def request(self, image, geolocation):
        pass

    def image(self, geolocation, dateset):

        _filter = ee.Filter.And(
            ee.Filter.bounds(geolocation, self.margin),
            ee.Filter.date(dateset[0], dateset[1])
        )

        _image_collection = ee.imagecollection(self.dataset).filter(_filter)
        _image_list = _image_collection.toList()

        if len(_image_list) == 0:
            raise Exception('No images found')

        _image = ee.Image(_image_list[0])
        _image_data = self.request(_image, geolocation)

        _image_pixels = Image.open(io.BytesIO(_image_data))
        _image_p_l = _image_pixels.convert('L')
        _image_array = np.array(_image_p_l)

        return _image_array 