#!/usr/bin/env python3
import sys
import os
import subprocess
import math
import csv
import datetime
from tempfile import NamedTemporaryFile
import shutil
from gcoder import GCode

# CONSTANTS
USAGE = f"Usage: {sys.argv[0]} | [--create-project]"
FILAMENT_WIDTH = 1.75  # mm
FILAMENT_SECTION_AREA = math.pi * math.pow((FILAMENT_WIDTH / 2), 2)  # mm2
FILAMENT_DENSITY = 1.24  # g/cm3
outputfile = "./output.csv"

# Create project file
def create_project():
    with open(outputfile, "w") as csvfile:
        fieldnames = [
            "Model",
            "Quantity",
            "Duration",
            "Used_Filament_length",
            "Used_Filament_weight",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for filename in os.listdir("./"):
            writer.writerow({"Model": filename}) if ".stl" in filename else None


# for each file in csv generate the gcode
def generate_gcode():
    options = "--solid-infill-speed 140 --infill-speed 140 --external-perimeter-speed 40 --perimeter-speed 50 --skirt-height 3 --external-perimeter-extrusion-width 0.45 --extrusion-width 0.45 --fill-pattern grid --perimeters 2 --top-solid-layers 5 --bottom-solid-layers 4 --fill-density 20 --filament-diameter 1.75 --nozzle-diameter 0.4 --first-layer-height 0.2 --layer-height 0.2".split()
    with open(outputfile, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            filename = [row["Model"]]
            args = ["slic3r"] + options + filename
            subprocess.run(args)


def process_gcode():
    tempfile = NamedTemporaryFile("w+t", newline="", delete=False)
    outputfile = "./output.csv"
    total_duration = datetime.timedelta(0)
    total_length = 0
    total_weight = 0
    # for each file in csv process the corresponding gcode
    with open(outputfile, "r") as csvfile, tempfile:
        fieldnames = [
            "Model",
            "Quantity",
            "Duration",
            "Used_Filament_length",
            "Used_Filament_weight",
        ]
        reader = csv.DictReader(csvfile)
        writer = csv.DictWriter(tempfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            filename = row["Model"].replace("stl", "gcode")
            quantity = int(row["Quantity"])
            gcode = GCode(open(filename, "r"))
            used_filament_length = gcode.filament_length
            total_length += used_filament_length * quantity
            print_time = gcode.duration  # datetime.timedelta(seconds)
            total_duration += print_time * quantity
            used_filament_weight = (
                FILAMENT_DENSITY * (used_filament_length * FILAMENT_SECTION_AREA) / 1000
            )
            total_weight += used_filament_weight * quantity
            writer.writerow(
                {
                    "Model": row["Model"],
                    "Quantity": row["Quantity"],
                    "Duration": print_time,
                    "Used_Filament_length": round(used_filament_length / 1000, 2),
                    "Used_Filament_weight": round(used_filament_weight, 2),
                }
            )
        writer.writerow(
            {
                "Model": "Total",
                "Quantity": "",
                "Duration": total_duration,
                "Used_Filament_length": round(total_length / 1000, 2),
                "Used_Filament_weight": round(total_weight, 2),
            }
        )
    shutil.move(tempfile.name, outputfile)


# finally sum the total weight, length and duration for the project and calculate the total cost


def main():
    args = sys.argv[1:]
    if not args:
        print("HELLO")
        generate_gcode()
        print("GCODE DONE!")
        process_gcode()
        print("GCODE Processed!")
    elif args[0] == "--create-project":
        create_project()
        print("Project file created")
    else:
        print(USAGE)


if __name__ == "__main__":
    main()
