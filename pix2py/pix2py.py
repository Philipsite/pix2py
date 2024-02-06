"""
    A python package to plot pixelmaps genrated by Domino (Theriak-Domino: de Capitani and Petrakakis, 2010) in Python.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


class PixelMap:
    def __init__(self, pixelmap_dir=Path.cwd()/"_pixelmaps", endmember_dict=None):
        self.pixelmap_dir = pixelmap_dir

        if isinstance(endmember_dict, str):
            self.endmember_dict = GLOBAL_ENDMEMBER_DICT[endmember_dict]

        elif isinstance(endmember_dict, dict):
            self.endmember_dict = endmember_dict

        else:
            raise ValueError("endmember_dict should be a dictionary or a string \"database name\" for a database in GLOBAL_ENDMEMBER_DICT.")

        # Execute the read_pixinfo method upon initialization
        self.read_pixinfo()

    def read_pixinfo(self):
        """Read the pixinfo.txt from the pixelmap dir

        Save T_grid, P_grid, bulk, pixmap_names to attributes
        """
        file_path = Path(self.pixelmap_dir, "pixinfo")

        pixinfo = open(file_path)
        pixinfo = pixinfo.readlines()
        # strip "\n" and trailing/leading spaces
        pixinfo = [line.strip() for line in pixinfo]

        # ## READ BULK PRESSURE AND TEMPERATURE (GRID) ##
        # extract T min max and P min max
        PT_limits = np.array(pixinfo[2].split(), dtype=float)
        T_limits = PT_limits[0:2]
        P_limits = PT_limits[2:4]

        # read n.o. steps in X and Y
        T_noSteps, P_noSteps = np.array(pixinfo[4].split(), dtype=int)[0:2]

        # calculate grid
        PT_grid = np.meshgrid(np.linspace(T_limits[0], T_limits[1], T_noSteps), np.linspace(P_limits[0], P_limits[1], P_noSteps))

        self.T_limits = T_limits
        self.P_limits = P_limits
        self.T_noSteps = T_noSteps
        self.P_noSteps = P_noSteps
        self.PT_grid = PT_grid

        # ## READ BULK COMPOSITION AND PIXELMAP NAMES (VARIABLES) ##
        # read lines to skip
        temp_idx = np.int16(pixinfo[5])

        # read bulk composition
        temp_idx = 7 + temp_idx
        bulk = pixinfo[temp_idx]

        self.bulk = bulk

        # read composition lines to skip
        comp_lines = np.int16(pixinfo[temp_idx - 1])
        temp_idx = comp_lines + temp_idx

        # read all calculated pixelmaps
        pixmap_names = pixinfo[temp_idx:]

        self.pixmap_names = pixmap_names

    def read_mineral_pixelmap(self, variable: str, mineral: str):
        # pixelmap file changes with dominating endmember in solid solution
        # all pixelmaps for all endmembers must be read and plotted
        endmember_solid_solution = self.endmember_dict[mineral]

        # initialize a zero array to store all pixelmaps
        pix_array = np.zeros((self.T_noSteps, self.P_noSteps))

        if isinstance(endmember_solid_solution, tuple):
            for endmember in endmember_solid_solution:
                filename = f"{variable}_[{endmember}]"

                if filename in self.pixmap_names:
                    pix_array += self.read_pixelmap_file(self.pixelmap_dir / filename, (self.T_noSteps, self.P_noSteps))

                else:
                    print(f"INFO: {filename} not found in {self.pixelmap_dir}. Skipping this endmember.")
        # work around for phases with no solid solution (define a single "endmember" in the endmember_dict) and create a filename without square brackets
        elif isinstance(endmember_solid_solution, str):
            filename = f"{variable}_{endmember_solid_solution}"

            if filename in self.pixmap_names:
                pix_array += self.read_pixelmap_file(self.pixelmap_dir / filename, (self.T_noSteps, self.P_noSteps))

            else:
                print(f"INFO: {filename} not found in {self.pixelmap_dir}. Skipping this endmember.")

        if variable == "vol":
            # read the V_solids pixelmap to calculate the volume fraction as modal volume (volume fraction of solids)
            total_volume = self.read_pixelmap_file(self.pixelmap_dir / "V_solids", (self.T_noSteps, self.P_noSteps))

            pix_array = pix_array / total_volume

        return pix_array

    @staticmethod
    def read_pixelmap_file(path, grid_shape):
        pixelmap_file = pd.read_csv(path, sep=r"\s+", header=None).to_numpy()
        pixelmap_idx = np.array(pixelmap_file[:, 0], dtype=int)
        # adjust index to start from 0
        pixelmap_idx = pixelmap_idx - 1
        pixelmap_values = pixelmap_file[:, 1]

        # insert values in flattened grid, and reshape to grid_shape
        pixelmap_grid = np.zeros(grid_shape[0] * grid_shape[1])
        pixelmap_grid[pixelmap_idx] = pixelmap_values
        pixelmap_grid = pixelmap_grid.reshape(grid_shape[0], grid_shape[1])

        return pixelmap_grid

    def plot_pixelmap(self, variable: str, mineral: str):
        pix_array = self.read_mineral_pixelmap(variable, mineral)

        fig, ax = plt.subplots()
        im = ax.imshow(pix_array, cmap="viridis", origin="lower",
                       extent=[self.T_limits[0], self.T_limits[1], self.P_limits[0], self.P_limits[1]], aspect="auto")
        ax.set_xlabel("Temperature (°C)")
        ax.set_ylabel("Pressure (bar)")

        if variable == "vol":
            label = f"Volume fraction of {mineral}"
        else:
            label = f"{variable} of {mineral}"
        fig.colorbar(im, ax=ax, label=label)

        return fig, ax

    def plot_isolines(self, variable: str, mineral: str):
        pix_array = self.read_mineral_pixelmap(variable, mineral)

        fig, ax = plt.subplots()
        im = ax.contourf(self.PT_grid[0], self.PT_grid[1], pix_array, cmap="viridis", origin="lower",
                         extent=[self.T_limits[0], self.T_limits[1], self.P_limits[0], self.P_limits[1]])
        ax.set_xlabel("Temperature (°C)")
        ax.set_ylabel("Pressure (bar)")

        if variable == "vol":
            label = f"Volume fraction of {mineral}"
        else:
            label = f"{variable} of {mineral}"
        fig.colorbar(im, ax=ax, label=label)

        return fig, ax


GLOBAL_ENDMEMBER_DICT = {}

GLOBAL_ENDMEMBER_DICT["jun92d"] = {}
GLOBAL_ENDMEMBER_DICT["jun92d"]["biotite"] = "Ann", "Phl"
GLOBAL_ENDMEMBER_DICT["jun92d"]["white mica"] = "Ms", "Pg", "MgC", "FeC"
GLOBAL_ENDMEMBER_DICT["jun92d"]["margarite"] = "Mrg"
GLOBAL_ENDMEMBER_DICT["jun92d"]["garnet"] = "Gr", "Py", "Alm", "spf"
GLOBAL_ENDMEMBER_DICT["jun92d"]["chlorite"] = "Ame", "Pen", "FeAm", "FeP"

GLOBAL_ENDMEMBER_DICT["td-ds62-mb50-v07"] = {}
GLOBAL_ENDMEMBER_DICT["td-ds62-mb50-v07"]["garnet"] = "py", "alm", "gr", "kho"
GLOBAL_ENDMEMBER_DICT["td-ds62-mb50-v07"]["epidote"] = "cz", "ep", "fep"
GLOBAL_ENDMEMBER_DICT["td-ds62-mb50-v07"]["calcic amphibole"] = "tr", "tsm", "pargm", "glm", "cumm", "grnm", "a", "b", "mrb", "kprg", "tts"
GLOBAL_ENDMEMBER_DICT["td-ds62-mb50-v07"]["clinopyroxene"] = "jd", "di", "hed", "acmm1", "om", "cfm", "jac"

GLOBAL_ENDMEMBER_DICT["td-d6ax_NCKFMASHTO_JRE"] = {}
GLOBAL_ENDMEMBER_DICT["td-d6ax_NCKFMASHTO_JRE"]["biotite"] = "phl", "ann1", "obi", "east", "tbi", "fbi", "mnbi1"
