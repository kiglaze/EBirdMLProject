
class RegionClass:
    def __init__(self, lat_range: tuple, lon_range: tuple):
        self.lat_range = lat_range
        self.lon_range = lon_range
    def get_min_lat(self):
        return self.lat_range[0]
    def get_max_lat(self):
        return self.lat_range[1]
    def get_min_lon(self):
        return self.lon_range[0]
    def get_max_lon(self):
        return self.lon_range[1]
    def get_top_left(self):
        return (self.get_max_lat(), self.get_min_lon())
    def get_bottom_right(self):
        return (self.get_min_lat(), self.get_max_lon())
