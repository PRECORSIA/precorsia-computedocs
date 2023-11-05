from PIL import Image
import numpy as np
import io
import ee

# Modify this so that the system gets the list of images and saves it
# insted of just using the first one in the list

# By saving the date and the image id, it is possible to let
# the class user choose witch one it wants to request

# Doing this may save a lot of API requests

# ALSO: MAKE AN API REQUEST COUNTER

class PrecorsiaGee:
    
    def __init__(self, dataset, band_range, margin=50):
        self.dataset = dataset
        self.band_range = band_range
        self.margin = margin

    @staticmethod
    def init():
        ee.Initialize()

    @staticmethod
    def initLogin():
        ee.Authenticate()
        ee.Initialize()

    def list(self, geolocation, dateset):

        _filter = ee.Filter.And(
            ee.Filter.bounds(ee.Geometry.Point(geolocation, 'EPSG:4326'), self.margin),
            ee.Filter.date(dateset[0], dateset[1])
        )

        _image_collection = ee.ImageCollection(self.dataset).filter(_filter)
        _image_list = _image_collection.toList(0xffff)

        if _image_list.size().getInfo() == 0:
            raise Exception('No images found')
        
        _image_list = _image_list.map(lambda img: ee.Dictionary(
            {'id': ee.Image(img).id(), 'time_start': ee.Image(img).get('system:time_start')})).getInfo()

        return _image_list

    def request(self, image, bands, geolocation):

        _proj = ee.Projection('EPSG:4326').atScale(10).getInfo()
        _scale_x = _proj['transform'][0]
        _scale_y = _proj['transform'][4]

        return {
            'assetId': self.dataset + '/' + image,
            'fileFormat': 'PNG',
            'bandIds': bands,
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
            'visualizationOptions':  {'ranges': [{'min': self.band_range[0], 'max': self.band_range[1]}]},
        }

    def image(self, image, bands, geolocation):

        _image_request = self.request(image, bands, geolocation)
        _image_data = ee.data.getPixels(_image_request)

        _image_pixels = Image.open(io.BytesIO(_image_data))
        _image_p_l = _image_pixels.convert('L')
        _image_array = np.array(_image_p_l)

        return _image_array