import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import os

class ImageProcessor:

    def __init__(self, image_lists, buffer_dir='./buffer/'):
        """
        @brief Constructor for the ImageProcessor class.
        @param image_lists A list of lists, where each sublist contains dictionaries representing images with 'id' and 'zeros' keys.
        @param buffer_dir (Optional) A string representing the directory where the images are stored. Default is './buffer/'.
        """
        self.image_lists = image_lists
        self.buffer_dir = buffer_dir

    def calculate_zeros(self, image_list):
        """
        @brief Calculates the proportion of zero pixels in each image in a list.
        @param image_list A list of dictionaries representing images. Each dictionary should have an 'id' key.
        @return Returns a list of dictionaries. Each dictionary represents an image and contains 'id' and 'zeros' keys. The 'zeros' key is the proportion of zero pixels in the image.
        """
        _zeros_class = []
        for _image in [image for image in image_list]:
            _id = _image['id']
            _img = Image.open(f'{self.buffer_dir}%s.png' % _id).convert('L')
            _img_arr = np.array(_img)
            _zeros = np.count_nonzero(_img_arr == 0)
            _zeros_class.append({'id': _id, 'time_start': _image['time_start'], 'zeros': (_zeros / np.prod(_img_arr.shape))})
        
        return _zeros_class

    def discard_images(self, zeros_class, clip_amount=0.33):
        """
        @brief Discards images with a proportion of zero pixels above a certain threshold.
        @param zeros_class A list of dictionaries representing images. Each dictionary should have 'id' and 'zeros' keys.
        @param clip_amount (Optional) A float representing the threshold proportion of zero pixels. Default is 0.33.
        @return Returns a list of dictionaries representing the remaining images after discarding.
        """
        _zeros_class = zeros_class
        for _image in _zeros_class:
            if _image['zeros'] > clip_amount:
                os.remove(f'{self.buffer_dir}%s.png' % _image['id'])
                _zeros_class.remove(_image)
        return _zeros_class

    @staticmethod
    def select_best_images(_zeros_class):
        """
        @brief Selects the three best images based on the proportion of zero pixels.
        @param _zeros_class A list of dictionaries representing images. Each dictionary should have 'id' and 'zeros' keys.
        @return Returns a list of dictionaries representing the three best images.
        """
        _sorted_zeros_class = sorted(_zeros_class, key=lambda _z: _z['zeros'])
        return _sorted_zeros_class[:3]

    def calculate_best_image(self, best_class):
        """
        @brief Calculates the average image from the best images.
        @param best_class A list of dictionaries representing the best images. Each dictionary should have an 'id' key.
        @return Returns a numpy array representing the average image.
        """
        _img = Image.open(f'{self.buffer_dir}%s.png' % best_class[0]['id']).convert('L')
        _best_image = np.zeros(np.array(_img).shape)
        for _image in best_class:
            _img = Image.open(f'{self.buffer_dir}%s.png' % _image['id']).convert('L')
            _img_arr = np.array(_img)
            _best_image += _img_arr * 0.3332
        return _best_image

    def replace_and_save(self, best_class, best_image):
        """
        @brief Replaces zero pixels in the best images with the corresponding pixels from the average image and saves the images.
        @param best_class A list of dictionaries representing the best images. Each dictionary should have an 'id' key.
        @param best_image A numpy array representing the average image.
        """
        for _image in best_class:
            _img = Image.open(f'{self.buffer_dir}%s.png' % _image['id']).convert('L')
            _img_arr = np.array(_img)
            _img_mask = _img_arr == 0
            _img_filtered = (best_image * _img_mask) + _img_arr
            plt.imsave(f'{self.buffer_dir}%s.png' % _image['id'], _img_filtered, cmap='gray')

    def zero_counting_filter(self):
        """
        @brief Processes all the images in the image_lists attribute.
        """
        after_delete = []
        for _image_list in self.image_lists:
            _zeros_class = self.calculate_zeros(_image_list)
            _zeros_discad = self.discard_images(_zeros_class)
            _best_class = ImageProcessor.select_best_images(_zeros_discad)
            _best_image = self.calculate_best_image(_best_class)
            self.replace_and_save(_best_class, _best_image)
            after_delete.append(_zeros_class)

        return after_delete