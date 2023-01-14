#!/usr/bin/env python3

from warpath_unity import WarpathUnity


if __name__ == '__main__':
    src, dst = 'obb/assets', 'obb'
    warpath_unity = WarpathUnity(src, dst)
    warpath_unity.export_textasset()
    # warpath_unity.export_sprite()
    # warpath_unity.export_texture2d()
    # warpath_unity.export_monobehaviour()
