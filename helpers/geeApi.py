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

    def request(self, image, geolocation, band, band_range):

        _proj = ee.Projection('EPSG:4326').atScale(10).getInfo()
        _scale_x = _proj['transform'][0]
        _scale_y = _proj['transform'][4]

        return {
            'assetId': self.dataset + '/' + image,
            'fileFormat': 'PNG',
            'bandIds': [band],
            'grid': {
                'dimensions': {
                    'width': 512,
                    'height': 512
                },
                'affineTransform': {
                    'scaleX': _scale_x,
                    'shearX': 0,
                    'translateX': geolocation[0],
                    'scaleY': _scale_y,
                    'shearY': 0,
                    'translateY': geolocation[1]
                },
                'crsCode': _proj['crs']
            },
            'visualizationOptions':  {'ranges': [{'min': band_range[0], 'max': band_range[1]}]},
        }

    def image(self, geolocation, dateset, band, band_range):

        _filter = ee.Filter.And(
            ee.Filter.bounds(geolocation, self.margin),
            ee.Filter.date(dateset[0], dateset[1])
        )

        _image_collection = ee.imagecollection(self.dataset).filter(_filter)
        _image_list = _image_collection.toList()

        if len(_image_list) == 0:
            raise Exception('No images found')

        _image = ee.Image(_image_list[0])
        _image_data = self.request(_image, geolocation, band, band_range)

        _image_pixels = Image.open(io.BytesIO(_image_data))
        _image_p_l = _image_pixels.convert('L')
        _image_array = np.array(_image_p_l)

        return _image_array 