#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

LT ANALYSIS

This module shows some basic plotting techniques with Bokeh and Plotly.

@author         Nicolas Jeanmonod
@date           2020-02-16

"""


import logging
import sys
import time
import warnings
import xml.etree.ElementTree as ET

import numpy as np

from plot_bokeh import PlotBokeh
from plot_plotly import PlotPlotly


# User choices.
SETTINGS = {
    "GENERAL": {
        "DATA_DIR": "./data/",
        "DATA_FILES": ["LT01", "LT30"],
        "REMOVE_DATA_FOR_FASTER_PROCESSING": False,
        "LT_MAX_LEVEL": 400,
        "PLOT_WIDTH": 1200,
        "PLOT_HEIGHT": 650,
        "LOGGING_ENABLED": True,
        "LOGGING_LEVEL": 10,
        "SHOW_HTML": False,
        "COLORS": ("#30123b", "#c0f233", "#3c3285", "#dae236", "#4353c2",
                   "#f0cb3a", "#4670e8", "#fbb336", "#438efd", "#fd9229",
                   "#34aaf8", "#f76e1a", "#20c6df", "#ea500d", "#17debf",
                   "#d73606", "#27eda3", "#c02302", "#4df97c", "#a01101",
                   "#78fe59", "#7a0402", "#a1fc3d"),
    },
    "BOKEH": {
        "DO_IT": True,
        "TOOLS": "pan, box_zoom, wheel_zoom, save, reset, xzoom_in, xzoom_out",
        "ALPHA_1": 1,  # 0.1
        "ALPHA_6": 1,  # 0.6
        "CIRCLE_SIZE": 3,
        "OUT_DIR": "./out_python_bokeh/",
    },
    "PLOTLY": {
        "DO_IT": True,
        "OUT_DIR": "./out_python_plotly/",
    }
}

# Global variables.
LOGGER = logging.getLogger(__name__)


def read_data(data_file, settings):
    """ ___ """

    LOGGER.debug("Processing %s", data_file)

    file_name = settings["GENERAL"]["DATA_DIR"] + data_file + ".xml"
    tree = ET.parse(file_name)
    root = tree.getroot()
    reshape = True
    lt_data = {}
    meas_count = None
    level_count = None
    for child in root:
        if child.tag in ["ID", "HePressure_mbar"]:
            continue

        #
        # XML TAGS
        #
        # Level_mm
        # Voltage_V
        # KeithleyTimeStamp
        # Current_A
        # Resistance_ohm
        #
        for _elem in root.iter(child.tag):

            meas_count, level_count = _elem.attrib["size"].split(" ")
            meas_count, level_count = int(meas_count), int(level_count)

            if reshape:
                lt_data[child.tag] = np.asarray(_elem.text.split(" ")).astype(
                    "float64").reshape(level_count, meas_count)
            else:
                lt_data[child.tag] = np.asarray(
                    _elem.text.split(" ")).astype("float64")

    if reshape:
        lt_data["KeithleyTimeStamp"] -= lt_data["KeithleyTimeStamp"][0][0]
    else:
        lt_data["KeithleyTimeStamp"] -= lt_data["KeithleyTimeStamp"][0]

    data = {
        "lt_data": lt_data,
        "lt_name": data_file,
        "file_name": file_name,
        "meas_count": meas_count,
        "level_count": level_count,
    }

    if SETTINGS["GENERAL"]["REMOVE_DATA_FOR_FASTER_PROCESSING"]:
        data = remove_data_for_faster_processing(data)

    return data


def remove_data_for_faster_processing(data):
    """ ___ """

    for _i in range(3):
        data["lt_data"]["Level_mm"] = \
            np.delete(data["lt_data"]["Level_mm"], np.s_[::2], 1)
        data["lt_data"]["Voltage_V"] = \
            np.delete(data["lt_data"]["Voltage_V"], np.s_[::2], 1)
        data["lt_data"]["KeithleyTimeStamp"] = \
            np.delete(data["lt_data"]["KeithleyTimeStamp"], np.s_[::2], 1)
        data["lt_data"]["Current_A"] = \
            np.delete(data["lt_data"]["Current_A"], np.s_[::2], 1)
        data["lt_data"]["Resistance_ohm"] = \
            np.delete(data["lt_data"]["Resistance_ohm"], np.s_[::2], 1)
    data["meas_count"] = data["lt_data"]["Level_mm"].shape[1]
    return data


def calc_resistivity(data, settings):
    """ ___ """

    # Levels equal to or higher than the LT max level are set to NaN.
    # This is because the resistivity is not defined when `level >= max_level`.
    filt_levels = np.copy(data["lt_data"]["Level_mm"])
    max_level = settings["GENERAL"]["LT_MAX_LEVEL"]
    filt_levels[filt_levels >= max_level] = np.nan

    # Calculate resistivity with filtered levels.
    data["lt_data"]["resistivity"] = data["lt_data"]["Resistance_ohm"] / \
        (settings["GENERAL"]["LT_MAX_LEVEL"] - filt_levels)

    return data


def init_logger(settings):
    """
    50 CRITICAL, 40 ERROR, 30 WARNING, 20 INFO, 10 DEBUG, 0 NOTSET

    # To get the names of running loggers:
    loggers = [logging.getLogger(name)
                                 for name in logging.root.manager.loggerDict]
    print(loggers)
    """

    if not settings["GENERAL"]["LOGGING_ENABLED"]:
        logging.disable(50)
        return

    logging.basicConfig(stream=sys.stdout,
                        format="%(asctime)-s "
                        "%(levelno)-s "
                        "%(module)-14s"
                        "%(funcName)-30s:"
                        "%(lineno)-3s : "
                        "%(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")

    LOGGER.setLevel(settings["GENERAL"]["LOGGING_LEVEL"])
    logging.getLogger("plot_bokeh").setLevel(
        settings["GENERAL"]["LOGGING_LEVEL"])
    logging.getLogger("plot_plotly").setLevel(
        settings["GENERAL"]["LOGGING_LEVEL"])

    LOGGER.debug("python %s", sys.version.split(" ")[0])
    LOGGER.debug("numpy %s", np.__version__)


def plot_with_bokeh(settings, data):
    """ ___ """

    if not settings["PLOTLY"]["DO_IT"]:
        LOGGER.debug("Skipping Plotly plot.")
        return

    start_time = time.time()
    plotb = PlotBokeh(settings, data)
    do_plots(plotb)
    total_time = time.time() - start_time
    LOGGER.debug("Bokeh time for %s : %0.1f s",
                 data["lt_name"], total_time)


def plot_with_plotly(settings, data):
    """ ___ """

    if not settings["BOKEH"]["DO_IT"]:
        LOGGER.debug("Skipping Bokeh plot.")
        return

    start_time = time.time()
    plotp = PlotPlotly(settings, data)
    do_plots(plotp)
    total_time = time.time() - start_time
    LOGGER.debug("Plotly time for %s : %0.1f s",
                 data["lt_name"], total_time)


def do_plots(plt):
    """ ___ """

    plt.title()
    plt.plot_current_vs_time()
    plt.plot_resistance_vs_time()
    plt.plot_level_vs_time()
    plt.plot_resistivity_vs_time()
    plt.plot_resistance_vs_current()
    plt.write_to_html_file()


def read_settings():
    """
    In this simple example, the parameters are stored in this file.
    In a production environment, they would be stored externally.

    TODO: Perform sanity checks.
    """

    settings = SETTINGS
    return settings


def main():
    """ ___ """

    # Init.
    settings = read_settings()
    init_logger(settings)

    # Process data files.
    for data_file in settings["GENERAL"]["DATA_FILES"]:

        # Read data and calculate resistivity.
        data = read_data(data_file, settings)
        data = calc_resistivity(data, settings)

        # Plot with Plotly.
        plot_with_plotly(settings, data)

        # Plot with Bokeh.
        plot_with_bokeh(settings, data)


if __name__ == "__main__":

    main()
