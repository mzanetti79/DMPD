from ROOT import TColor

color_codes = {}
color_codes['ColorCombo424'] = {#1001: [126, 181, 214],
                                1001: [45, 57, 86],
                                1002: [42, 117, 169],
                                #1003: [39, 66, 87],
                                1003: [110, 130, 67],
                                1004: [223, 193, 132],
                                1005: [143, 96, 72],
                                1006: [100, 68, 54],
                                
                                }

color_codes['Canna St. and 4th'] = {1001: [75,62,89],
                                    1002: [138,166,63],
                                    1003: [255,248,107],
                                    1004: [255,189,82],
                                    1005: [166,63,63],
                                    1006: [100, 68, 54],
                                    }

color_codes['africa'] = {1001: [236,128,92],
                         1002: [255,244,216],
                         1003: [245,202,134],
                         1004: [100,110,83],
                         1005: [39,49,40],
                         1006: [100, 68, 54],
                         }


def defineColors(color_code='ColorCombo424'):
    colors = {}
    rgb=255.
    for color_number in color_codes[color_code]:
        colors[color_number] = TColor(color_number,
                                      color_codes[color_code][color_number][0]/rgb,
                                      color_codes[color_code][color_number][1]/rgb,
                                      color_codes[color_code][color_number][2]/rgb,)
    return colors
