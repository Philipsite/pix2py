# %%
import matplotlib.pyplot as plt
from pathlib import Path
from pix2py.pix2py import PixelMap

# Create a PixelMap object
pixelmap = PixelMap(endmember_dict="jun92d")
fig, ax = pixelmap.plot_pixelmap("Mg#", "biotite")


# pix_array = pixelmap.read_mineral_pixelmap("vol", "garnet")

# pix_array = pixelmap.read_pixelmap_file(pixelmap.pixelmap_dir / "G_tot", (pixelmap.T_noSteps, pixelmap.P_noSteps))

# plt.imshow(pix_array, cmap="viridis", origin="lower", extent=[pixelmap.T_limits[0], pixelmap.T_limits[1], pixelmap.P_limits[0], pixelmap.P_limits[1]], aspect="auto")
# plt.colorbar(label="H_tot")
# %%
fig, ax = pixelmap.plot_isolines("Mg#", "biotite")

# %%
