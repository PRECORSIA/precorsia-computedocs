# Importing data processing tools
import matplotlib.pyplot as plt
import numpy as np
import json

class PrecorsiaFilter:

    def __init__(self, configuration):

        expected_keys = [
            "startDate", "days", "geolocation", "image_scale", "round_factor",
            "reference_dataset", "comparable_dataset", "reference_band_name",
            "reference_band_range", "reference_band_unit", "comparable_band_name", 
            "comparable_band_range", "comparable_band_unit", "gee", 
            "imageCorrelator", "imageProcessor"
        ]

        if not isinstance(configuration, dict):
            raise TypeError("Configuration must be a dictionary.")

        missing_keys = [key for key in expected_keys if key not in configuration]
        if missing_keys:
            raise ValueError(f"Missing keys in configuration: {missing_keys}")

        self.gee = configuration["gee"]
        self.imageCorrelator = configuration["imageCorrelator"]
        self.imageProcessor = configuration["imageProcessor"]
       
        self.START, self.END = self.gee.date_daily(configuration["startDate"], configuration["days"])
        self.geolocation = configuration["geolocation"]
        self.image_scale = configuration["image_scale"]
        self.round_factor = configuration["round_factor"]

        self.reference_dataset = configuration["reference_dataset"]
        self.comparable_dataset = configuration["comparable_dataset"]

        self.reference_band_name = configuration["reference_band_name"]
        self.reference_band_range = configuration["reference_band_range"]
        self.reference_band_unit = configuration["reference_band_unit"]
        self.comparable_band_name = configuration["comparable_band_name"]
        self.comparable_band_range = configuration["comparable_band_range"]
        self.comparable_band_unit = configuration["comparable_band_unit"]

    @staticmethod
    def initialize(PrecorsiaGee):
        try:
            PrecorsiaGee.init()
        except:
            PrecorsiaGee.initLogin()

    def execute(self):
        self.gds_one = self.gee(self.reference_dataset, self.reference_band_range)
        self.gds_two = self.gee(self.comparable_dataset, self.comparable_band_range)

        self.gds_one_list = self.gds_one.list(self.geolocation, [self.START, self.END])
        self.gds_two_list = self.gds_two.list(self.geolocation, [self.START, self.END])
        self.gds_one_list, self.gds_two_list = self.gee.correlate_dates(self.gds_one_list, self.gds_two_list, self.round_factor)

        self.gee.download_images(self.gds_one_list, self.gds_one, self.reference_band_name, self.geolocation, self.image_scale)
        self.gee.download_images(self.gds_two_list, self.gds_two, self.comparable_band_name, self.geolocation, self.image_scale)

        process = self.imageProcessor([self.gds_one_list, self.gds_two_list])
        [self.gds_one_lz, self.gds_two_lz] = process.zero_counting_filter()

        self.corr_list = self.gee.connected_correlation(self.gds_one_lz, self.gds_two_lz, self.round_factor)

        title = {'title': f'Correlation between {self.gds_one.dataset} and \n{self.gds_two.dataset} at {self.geolocation}',
        'xlabel': f"average {self.reference_band_unit} of {self.reference_band_name} per pixel [{self.gds_one.dataset}]",
        'ylabel': f"average {self.comparable_band_unit} of {self.comparable_band_name} per pixel [{self.gds_two.dataset}]"}

        self.gds_two_dataset_name = self.gds_two.dataset.replace('/', '_')

        self.corr_study = self.imageCorrelator(self.corr_list)
        self.corr_avr = self.corr_study.calculate_correlation()
        self.corr_avr = [(x * (self.reference_band_range[1] / 255), y * (self.comparable_band_range[1] / 255)) for x, y in self.corr_avr]

        self.imageCorrelator.plot(self.corr_avr, title)
        plt.savefig(f'plots/{self.gds_two_dataset_name}_{self.geolocation[0]}_{self.geolocation[1]}_normal.jpg', dpi=150)
        plt.close()

        self.x_values, self.y_values = zip(*self.corr_avr)
        self.best_shifted_corr_avr = []
        self.best_corr = -np.inf
        self.best_shift = 0

        for i in range(int(len(self.x_values)/2)):
            shifted_y_values = self.y_values[:-i] if i != 0 else self.y_values
            shifted_x_values = self.x_values[i:]
            shifted_corr_avr = list(zip(shifted_x_values, shifted_y_values))
            corr = np.corrcoef(shifted_x_values, shifted_y_values)[0, 1]

            if corr > self.best_corr:
                self.best_corr = corr
                self.best_shift = i
                self.best_shifted_corr_avr = shifted_corr_avr

        self.imageCorrelator.plot(self.best_shifted_corr_avr, title)
        plt.savefig(f'plots/{self.gds_two_dataset_name}_{self.geolocation[0]}_{self.geolocation[1]}_shifted.jpg', dpi=150)
        plt.close()
        print(f"Best shift: {self.best_shift}, Best correlation: {self.best_corr}")

        data = {"best_correlation": self.best_corr}
        data["best_shift"] = self.best_shift
        data["correlation_list"] = self.corr_list
        with open(f'data/corr_list_{self.gds_two_dataset_name}.json', 'w') as file:
            json.dump(data, file)