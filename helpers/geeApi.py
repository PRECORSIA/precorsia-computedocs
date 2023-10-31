import geemap.core as geemap
import ee

class PrecorsiaGee:
    def __init__(self, dataset):
        self.dataset = dataset

    def init(self):
        ee.Initialize()

    def initLogin(self):
        ee.Authenticate()
        ee.Initialize()

    def image(self, geolocation):
        pass