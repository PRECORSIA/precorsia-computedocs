from PIL import Image
import numpy as np
import io
import ee

class PrecorsiaGee:

    def __init__(self, dataset, band_range, margin=50):
        """
        @brief Constructor for the class.

        @param dataset The ID of the dataset to use.
        @param band_range A tuple containing the minimum and maximum band values to include in the images.
        @param margin (Optional) The margin to use when creating the bounding box for the image search. Default is 50.

        This constructor initializes a new instance of the class. It sets the dataset ID, 
        the band range, and the margin for the image search. The dataset ID is used to specify 
        which dataset to fetch images from. The band range is used to filter the bands included 
        in the images. The margin is used to create a bounding box around the given geolocation 
        for the image search.
        """

        self.dataset = dataset
        self.band_range = band_range
        self.margin = margin

    @staticmethod
    def init():
        """
        @brief Initializes the Earth Engine API.

        This static method initializes the Earth Engine API by calling the ee.Initialize() function. 
        It is necessary to call this method before making any requests to the Earth Engine servers.
        """

        ee.Initialize()

    @staticmethod
    def initLogin():
        """
        @brief Initializes the Earth Engine API and prompts the user to authenticate.

        This static method initializes the Earth Engine API by calling the ee.Initialize() function. 
        Before initialization, it prompts the user to authenticate with the Earth Engine servers 
        by calling the ee.Authenticate() function. The user will be asked to enter their Google account 
        credentials in a web browser, and then paste the resulting authentication code into the console.
        """

        ee.Authenticate()
        ee.Initialize()

    def list(self, geolocation, dateset):
        """
        @brief Fetches a list of images from a specific dataset that match the given geolocation and date range.

        @param geolocation A tuple containing the longitude and latitude of the location.
        @param dateset A tuple containing the START and END ee object dates for the image search.

        @return Returns a list of images. Each image is represented as a dictionary with 'id' and 'time_start' keys.

        @throws Exception If no images are found, an exception is raised.

        This function uses the Earth Engine (ee) library to fetch images from a specific dataset. 
        It filters the images based on the given geolocation and date range. 
        The geolocation is used to create a bounding box for the image search, 
        and the date range is used to filter the images based on their 'system:time_start' property.
        """
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
        """
        @brief Generates a request for a specific image from the dataset.

        @param image The ID of the image to request.
        @param bands A list of band IDs to include in the request.
        @param geolocation A tuple containing the longitude and latitude of the location.

        @return Returns a dictionary containing the request parameters.

        This function generates a request for a specific image from the dataset. 
        The request includes the asset ID of the image, the file format (PNG), 
        the band IDs to include, the grid dimensions and affine transform for the image, 
        and the visualization options. The affine transform is calculated based on the given geolocation 
        and a fixed scale defined by the EPSG:4326 projection at a scale of 10.
        """

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
        """
        @brief Fetches a specific image from the dataset and converts it to a grayscale numpy array.

        @param image The ID of the image to fetch.
        @param bands A list of band IDs to include in the image.
        @param geolocation A tuple containing the longitude and latitude of the location.

        @return Returns a numpy array representing the grayscale image.

        This function fetches a specific image from the dataset, converts it to grayscale, 
        and then converts it to a numpy array. The image is fetched by generating a request 
        with the given image ID, band IDs, and geolocation, and then sending this request 
        to the Earth Engine API. The returned image data is read into a PIL Image object, 
        converted to grayscale, and then converted to a numpy array.
        """

        _image_request = self.request(image, bands, geolocation)
        _image_data = ee.data.getPixels(_image_request)

        _image_pixels = Image.open(io.BytesIO(_image_data))
        _image_p_l = _image_pixels.convert('L')
        _image_array = np.array(_image_p_l)

        return _image_array

    @staticmethod
    def correlate_dates(list_one, list_two, round_factor):
        """
        @brief Correlates two lists of images based on their 'time_start' values.

        @param list_one First list of images. Each image is a dictionary with 'id' and 'time_start' keys.
        @param list_two Second list of images. Each image is a dictionary with 'id' and 'time_start' keys.
        @param round_factor Number of decimal places to filter to zero when rounding the date.

        @return Returns two lists of images. Each list contains the images from the input lists whose 'time_start' values, when rounded, are found in both lists.

        This function correlates two lists of images based on their 'time_start' values. 
        It first rounds the 'time_start' values of the images in both lists using the given round_factor. 
        It then finds the common rounded 'time_start' values in both lists. 
        Finally, it creates two new lists containing the images from the input lists whose rounded 'time_start' values are found in the common rounded 'time_start' values.
        """

        _one_rounded = [_img['time_start'] // 10**round_factor * 10**round_factor for _img in list_one]
        _two_rounded = [_img['time_start'] // 10**round_factor * 10**round_factor for _img in list_two]

        _common_rounded = np.intersect1d(_one_rounded, _two_rounded)

        _intersected_list_one = [img for img in list_one if img['time_start'] // 10**round_factor * 10**round_factor in _common_rounded]
        _intersected_list_two = [img for img in list_two if img['time_start'] // 10**round_factor * 10**round_factor in _common_rounded]

        return _intersected_list_one, _intersected_list_two