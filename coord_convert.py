import math
def _test_kp_config(keypad_config):
    # make sure len of keypad_config is 3
    if len(keypad_config) != 3: 
        raise ValueError('length of keypad_config must be 3')
    # make sure len of all sub-lists of keypad_config is 3
    for i in keypad_config:
        if len(i) != 3:
            raise ValueError('length of all keypad_config sub-lists must be 3')
    # make sure there are no repeated values
    all_values = [j for sub in keypad_config for j in sub]
    if len({i:all_values.count(i) for i in all_values}) != 9:
        raise ValueError('there must be no repeated values in keypad_config')
    # make sure all values are between 1 and 9
    for i in all_values:
        if type(i) != int or i < 0 or i > 9:
            raise ValueError('values in keypad_config must be between 1 and 9 (1..9)')

def tkp(len_loc_data: tuple, lod, keypad_config = [[7, 8, 9], [4, 5, 6], [1, 2, 3]]):
    """
    Converts a BCS coordinate to a Keypad Coordinate.

    Parameters
    ----------
    `len_loc_data` : tuple
        a tuple containing the X and Y length of the map and the X and Y coordinates of a given point.
    `lod` : int
        The number of keypad iterations to perform (more iterations = more accurate).
    `keypad_config` : list
        A 2D (3x3) list of integers between 1 and 9 (1..9).

    Raises
    ------
    `ValueError`
        If location is out of bounds or if keypad_config is invalid.
    
    Returns
    -------
    `int`
        The keypad coordinate.
    """
    len_x, len_y, loc_x, loc_y = len_loc_data
    # make sure map_len_x is a positive non-zero integer
    if type(len_x) != int or len_x <= 0:
        raise ValueError('map_len_x must be a positive non-zero integer')
    # make sure map_len_y is a positive non-zero integer
    if type(len_y) != int or len_y <= 0:
        raise ValueError('map_len_y must be a positive non-zero integer')
    _test_kp_config(keypad_config)
    # make sure locations aren't out of bounds
    if loc_x > len_x or loc_x < 0:
        raise ValueError('loc_x is out of bounds')
    elif loc_y > len_y or loc_y < 0:
        raise ValueError('loc_y is out of bounds')
    temp_len_x = len_x
    temp_len_y = len_y
    temp_loc_x = loc_x
    temp_loc_y = loc_y
    keys = []
    for i in range(lod):
        x = math.floor(temp_loc_x / (temp_len_x / 3))
        y = math.floor(temp_loc_y / (temp_len_y / 3))
        keys.append(keypad_config[y][x])
        temp_len_x /= 3
        temp_len_y /= 3
        temp_loc_x -= temp_len_x * x
        temp_loc_y -= temp_len_y * y
    return int(''.join([str(i) for i in keys]))

def fkp(len_data: tuple, keypad_coordinate, keypad_config = [[7, 8, 9], [4, 5, 6], [1, 2, 3]]):
    """
    Converts a Keypad Coordinate to a BCS coordinate.

    Parameters
    ----------
    `len_data` : tuple
        A tuple containing the X and Y length of the map.
    `keypad_config` : list
        A 2D (3x3) list of integers between 1 and 9 (1..9).
    `keypad_coordinate` : int
        The Keypad Coordinate to be converted to an X-Y coordinate.
    
    Raises
    ------
    `ValueError`
        If keypad_coordinate is not a positive non-zero integer or if keypad_config is invalid.
    
    Returns
    -------
    `tuple`
        The UCS coordinate centered to the middle of the lowest key.
    """
    len_x, len_y = len_data
    # make sure coordinate doesn't include non-integers
    for i in str(keypad_coordinate):
        try:
            int(i)
        except:
            raise ValueError('keypad_coordinate must be an integer')
    kpc = [int(i) for i in str(keypad_coordinate)]
    interval_x = len_x / (3 ** len(kpc))
    interval_y = len_y / (3 ** len(kpc))
    loc_x = 0
    loc_y = 0
    kpc_index = {
        keypad_config[0][2] : [2, 0],
        keypad_config[0][1] : [1, 0],
        keypad_config[0][0] : [0, 0],
        keypad_config[1][2] : [2, 1],
        keypad_config[1][1] : [1, 1],
        keypad_config[1][0] : [0, 1],
        keypad_config[2][2] : [2, 2],
        keypad_config[2][1] : [1, 2],
        keypad_config[2][0] : [0, 2]
    }
    level_of_detail = len(kpc)
    for i in range(len(kpc)):
        loc_x += interval_x * (3 ** (level_of_detail - (i + 1))) * kpc_index[kpc[i]][0]
        loc_y += interval_y * (3 ** (level_of_detail - (i + 1))) * kpc_index[kpc[i]][1]
    return (len_x, len_y, loc_x + interval_x / 2, loc_y + interval_y / 2)