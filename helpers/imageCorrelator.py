import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns
import numpy as np

class ImageCorrelator:

    def __init__(self, corr_list, buffer_dir='./buffer/'):
        """
        @brief Constructor for the ImageCorrelator class.
        @param corr_list A list of tuples, where each tuple contains two lists of image IDs from two different lists that fall within the same time interval.
        @param buffer_dir (Optional) A string representing the directory where the images are stored. Default is './buffer/'.
        """
        self.corr_list = corr_list
        self.buffer_dir = buffer_dir

    def calculate_correlation(self):
        """
        @brief Calculates the average pixel value for each pair of images in the corr_list attribute.
        @return Returns a list of tuples. Each tuple contains the average pixel values for a pair of images.
        """
        corr_avr = []
        for pair in self.corr_list:
            one_pair = []
            for img in pair[0]:
                img = Image.open(f'{self.buffer_dir}{img}.png')
                img = np.asarray(img)
                one_pair.append(np.average(img))

            two_pair = []
            for img in pair[1]:
                img = Image.open(f'{self.buffer_dir}{img}.png')
                img = np.asarray(img)
                two_pair.append(np.average(img))

            one_pair_avg = np.average(one_pair)
            two_pair_avg = np.average(two_pair)
            corr_avr.append((one_pair_avg, two_pair_avg))

        return corr_avr

    @staticmethod
    def plot(corr_avr):
        """
        @brief Plots the correlation of average pixel values for pairs of images.
        @param corr_avr A list of tuples. Each tuple contains the average pixel values for a pair of images.
        """
        x = [i[0] for i in corr_avr]
        y = [i[1] for i in corr_avr]
        sns.scatterplot(x=x, y=y)
        plt.show()