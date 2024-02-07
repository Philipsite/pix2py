import numpy as np

from pix2py import PixelMap
from pathlib import Path


def test_read_pixinfo():
    # Test the read_pixinfo method
    # Create a PixelMap object
    pixelmap_dir = Path("tests/test_data/test_pixelmaps")
    endmember_dict = {}
    pixelmap = PixelMap(pixelmap_dir, endmember_dict)

    assert pixelmap.T_limits[0] == 400
    assert pixelmap.T_limits[1] == 700
    assert pixelmap.P_limits[0] == 1000
    assert pixelmap.P_limits[1] == 10000
    assert pixelmap.T_noSteps == 50
    assert pixelmap.P_noSteps == 50
    assert pixelmap.bulk == "SI(22.84)TI(0.24)AL(7.78)FE(2.04)MN(0.02)MG(1.28)CA(0.25)NA(0.95)K(1.79)H(30)O(?)O(0.235)"


def test_read_pixelmap_file():
    file = Path("tests", "test_data", "test_pixelmap")
    read_file = PixelMap.read_pixelmap_file(file, (2, 2))

    expeacted_pixelmap = np.array([[0.0, 0.0], [0.0, 0.0]])

    assert np.array_equal(read_file, expeacted_pixelmap)
