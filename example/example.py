from pix2py import PixelMap
from pathlib import Path

pixelmap_dir = Path("example", "_pixelmaps")

LOCAL_ENDMEMBER_DICT = {}
LOCAL_ENDMEMBER_DICT["biotite"] = "phl", "annm", "obi", "east", "tbi", "fbi", "mnbi"
LOCAL_ENDMEMBER_DICT["LIQtc6"] = "q4L", "abL", "kspL", "anL", "slL", "fo2L", "fa2L", "h2oL"

pixmap = PixelMap(pixelmap_dir, LOCAL_ENDMEMBER_DICT)

fig, ax = pixmap.plot_pixelmap("vol", mineral="LIQtc6")
fig.savefig("LIQtc6_vol.png", dpi=300)

fig, ax = pixmap.plot_isolines("vol", mineral="LIQtc6")
fig.savefig("LIQtc6_vol_isolines.png", dpi=300)

fig, ax = pixmap.plot_pixelmap("Mg#", mineral="biotite")
fig.savefig("Biotite_Mg.png", dpi=300)