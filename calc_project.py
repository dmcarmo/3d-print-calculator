#!/usr/bin/env python3

import os
import math
import csv
import gcoder

# CONSTANTS

FILAMENT_WIDTH = 1.75  # mm
FILAMENT_SECTION_AREA = math.pi * math.pow((FILAMENT_WIDTH / 2), 2)  # mm2
FILAMENT_DENSITY = 1.24  # g/cm3

# Create project file
def createproject():
    with open("./output.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "Model",
                "Quantity",
            ]
        )
        for filename in os.listdir("./"):
            writer.writerow([filename]) if ".stl" in filename else None


# for each file in csv generate the gcode
filename = "'123 x.stl'"
OPTIONS = "-solid-infill-speed 140 --infill-speed 140 --external-perimeter-speed 40 --perimeter-speed 50 --skirt-height 3 --external-perimeter-extrusion-width 0.45 --extrusion-width 0.45 --fill-pattern grid --perimeters 2 --top-solid-layers 5 --bottom-solid-layers 4 --fill-density 20 --filament-diameter 1.75 --nozzle-diameter 0.4 --first-layer-height 0.2 --layer-height 0.2"
command = "slic3r %s %s" % (OPTIONS, filename)

# for each file in csv process the corresponding gcode
gcode_file = "'123 x.gcode'"
gcode = gcoder.GCode(open(gcode_file, "rU"))
used_filament_length = gcode.filament_length
print_time = gcode.duration  # datetime.timedelta(seconds)

used_filament_weight = (
    FILAMENT_DENSITY * (used_filament_length * FILAMENT_SECTION_AREA) / 1000
)
# append values (per part and for the total quantity) to csv row

# finally sum the total weight, length and duration for the project and calculate the total cost


def main():
    print("HELLO")


if __name__ == "__main__":
    main()
