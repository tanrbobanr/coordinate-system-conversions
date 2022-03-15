import math
class kpc():
    """
    Converts between an X-Y coordinate system and a Keypad coordinate system.

    Parameters
    ----------
    `max_len_x` : int
        The length of the X-Y coordinate system on the X-axis.
    `max_len_x` : int
        The length of the X-Y coordinate system on the X-axis.
    `keypad_config` : list
        A 2D (3x3) list of integers between 1 and 9 (1..9).
    
    Raises
    ------
    `ValueError`
        If map_len_x or map_len_y are not positive non-zero integers, or if keypad_config is constructed incorrectly.
    """
    def __init__(self, map_len_x, map_len_y, keypad_config = [[7, 8, 9], [4, 5, 6], [1, 2, 3]]):
        self.lenx = map_len_x
        self.leny = map_len_y
        self.keypad_config = keypad_config
        # make sure map_len_x is a positive non-zero integer
        if type(map_len_x) != int or map_len_x <= 0:
            raise ValueError('map_len_x must be a positive non-zero integer')
        # make sure map_len_y is a positive non-zero integer
        if type(map_len_y) != int or map_len_y <= 0:
            raise ValueError('map_len_y must be a positive non-zero integer')
        # make sure len of keypad_config is 3
        if len(self.keypad_config) != 3: 
            raise ValueError('length of keypad_config must be 3')
        # make sure len of all sub-lists of keypad_config is 3
        for i in self.keypad_config:
            if len(i) != 3:
                raise ValueError('length of all keypad_config sub-lists must be 3')
        # make sure there are no repeated values
        all_values = [j for sub in self.keypad_config for j in sub]
        if len({i:all_values.count(i) for i in all_values}) != 9:
            raise ValueError('there must be no repeated values in keypad_config')
        # make sure all values are between 1 and 9
        for i in all_values:
            if type(i) != int or i < 0 or i > 9:
                raise ValueError('values in keypad_config must be between 1 and 9 (1..9)')
    def kpc_from_location(self, location: tuple, level_of_detail: int):
        """
        Converts an X-Y location to a Keypad Coordinate.

        Parameters
        ----------
        `location` : tuple
            The X-Y coordinates of a given location.
        `level_of_detail` : int
            The number of keypad iterations to perform (more iterations = more accurate).
        
        Raises
        ------
        `ValueError`
            If location is out of bounds.
        
        Returns
        -------
        `int`
            The keypad coordinate.
        """
        location_x = location[0]
        location_y = location[1]
        # make sure locations aren't out of bounds
        if location_x > self.lenx or location_x < 0:
            raise ValueError('location_x is out of bounds')
        elif location_y > self.lenx or location_y < 0:
            raise ValueError('location_y is out of bounds')
        temp_len_x = self.lenx
        temp_len_y = self.leny
        temp_loc_x = location_x
        temp_loc_y = location_y
        keys = []
        for lod in range(level_of_detail):
            x = math.floor(temp_loc_x / (temp_len_x / 3))
            y = math.floor(temp_loc_y / (temp_len_y / 3))
            keys.append(self.keypad_config[y][x])
            temp_len_x /= 3
            temp_len_y /= 3
            temp_loc_x -= temp_len_x * x
            temp_loc_y -= temp_len_y * y
        return int(''.join([str(i) for i in keys]))
    def location_from_kpc(self, keypad_coordinate):
        """
        Converts a Keypad Coordinate to an X-Y coordinate.

        Parameters
        ----------
        `keypad_coordinate` : int
            The Keypad Coordinate to be converted to an X-Y coordinate.
        
        Raises
        ------
        `ValueError`
            If keypad_coordinate is not a positive non-zero integer.
        
        Returns
        -------
        `tuple`
            The X-Y coordinate centered to the middle of the lowest key.
        """
        # make sure coordinate doesn't include non-integers
        for i in str(keypad_coordinate):
            try:
                int(i)
            except:
                raise ValueError('keypad_coordinate must be an integer')
        _kpc = [int(i) for i in str(keypad_coordinate)]
        interval_x = self.lenx / (3 ** len(_kpc))
        interval_y = self.leny / (3 ** len(_kpc))
        loc_x = 0
        loc_y = 0
        kpc_index = {
            self.keypad_config[0][2] : [2, 0],
            self.keypad_config[0][1] : [1, 0],
            self.keypad_config[0][0] : [0, 0],
            self.keypad_config[1][2] : [2, 1],
            self.keypad_config[1][1] : [1, 1],
            self.keypad_config[1][0] : [0, 1],
            self.keypad_config[2][2] : [2, 2],
            self.keypad_config[2][1] : [1, 2],
            self.keypad_config[2][0] : [0, 2]
        }
        level_of_detail = len(_kpc)
        for i in range(len(_kpc)):
            loc_x += interval_x * (3 ** (level_of_detail - (i + 1))) * kpc_index[_kpc[i]][0]
            loc_y += interval_y * (3 ** (level_of_detail - (i + 1))) * kpc_index[_kpc[i]][1]
        return (loc_x + interval_x / 2, loc_y + interval_y / 2)
if __name__ == '__main__':
    _kpc = kpc(5000, 5000)
    print(_kpc.kpc_from_location(0, 0, 2))
    print(_kpc.location_from_kpc(333333333))

