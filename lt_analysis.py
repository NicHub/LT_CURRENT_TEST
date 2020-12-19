#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import warnings
import xml.etree.ElementTree as ET

import bokeh
import numpy as np
from bokeh.core.property.color import Color
from bokeh.io import output_file, show
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, NumeralTickFormatter, Title
from bokeh.palettes import Turbo256, linear_palette
from bokeh.plotting import output_file, save, show

# User choices.
TOOLS = "pan, box_zoom, wheel_zoom, save, reset, xzoom_in, xzoom_out"
PLOT_WIDTH = 1600
PLOT_HEIGHT = 400
ALPHA_1 = 1  # 0.1
ALPHA_6 = 1  # 0.6
LOGGING_ENABLED = True
LOGGING_LEVEL = 10
SHOW_HTML = True
XML_DIR = "./data/"
HTML_DIR = "./out_python/"

# Global variables.
COLORS = []
LTDATA = {}
HTML_ELEMS = []
LOGGER = logging.getLogger(__name__)
NB_MEAS = None
NB_HEIGHT = None


def readXML(lt_name):
    """ ___ """

    global NB_MEAS, NB_HEIGHT
    file_name = XML_DIR + lt_name + ".xml"
    tree = ET.parse(file_name)
    root = tree.getroot()
    reshape = True
    for child in root:
        if child.tag in ["ID", "HePressure_mbar"]:
            continue

        #
        # TAGS
        #
        # Level_mm
        # Voltage_V
        # KeithleyTimeStamp
        # Current_A
        # Resistance_ohm
        #
        for _elem in root.iter(child.tag):

            NB_MEAS, NB_HEIGHT = _elem.attrib["size"].split(" ")
            NB_MEAS, NB_HEIGHT = int(NB_MEAS), int(NB_HEIGHT)

            if reshape:
                LTDATA[child.tag] = np.asarray(_elem.text.split(" ")).astype(
                    "float64").reshape(NB_HEIGHT, NB_MEAS)
            else:
                LTDATA[child.tag] = np.asarray(
                    _elem.text.split(" ")).astype("float64")

    if reshape:
        LTDATA["KeithleyTimeStamp"] -= LTDATA["KeithleyTimeStamp"][0][0]
    else:
        LTDATA["KeithleyTimeStamp"] -= LTDATA["KeithleyTimeStamp"][0]

    global COLORS
    better_contrast = False
    if better_contrast:
        COLORS = (
            "#30123b",
            "#c0f233",
            "#3c3285",
            "#dae236",
            "#4353c2",
            "#f0cb3a",
            "#4670e8",
            "#fbb336",
            "#438efd",
            "#fd9229",
            "#34aaf8",
            "#f76e1a",
            "#20c6df",
            "#ea500d",
            "#17debf",
            "#d73606",
            "#27eda3",
            "#c02302",
            "#4df97c",
            "#a01101",
            "#78fe59",
            "#7a0402",
            "#a1fc3d",
        )
    else:
        COLORS = linear_palette(Turbo256, NB_HEIGHT)


def calc_resistivity(lt_name):
    """ ___ """

    max_length = 400

    # Suppress “divide by zero” warning.
    with warnings.catch_warnings(record=True) as _w:
        warnings.simplefilter("always")
        LTDATA["resistivity"] = LTDATA["Resistance_ohm"] / \
            (max_length - LTDATA["Level_mm"])
        if len(_w) == 1 \
                and issubclass(_w[-1].category, RuntimeWarning) \
                and "divide by zero" in str(_w[-1].message):
            LOGGER.debug(
                '%s — Some resistivity values cannot be calculated'
                ' because "Level = Max Height"', lt_name)


def plot_current_vs_time(lt_name):
    """ ___ """

    #
    # Format plot.
    #
    plt = bokeh.plotting.figure(tools=TOOLS)
    plt.toolbar.logo = None
    plt.plot_width = PLOT_WIDTH
    plt.plot_height = PLOT_HEIGHT
    plt.add_layout(
        Title(
            text=f"{lt_name} — Current vs time",
            text_font_style="normal",
            align="center"),
        "above")
    plt.xaxis.axis_label = "Time (s)"
    plt.yaxis.axis_label = "Current (A)"
    plt.yaxis.formatter = NumeralTickFormatter(format="0.000")

    #
    # Prepare data source and plot data.
    #
    for _h in range(NB_HEIGHT):
        _t = LTDATA["KeithleyTimeStamp"][_h]
        _y = LTDATA["Current_A"][_h]
        data_source = ColumnDataSource(data=dict(t=_t, y=_y))

        plt.line("t", "y", source=data_source, color=COLORS[_h],
                 legend_label="Current (A)", alpha=ALPHA_1)
        plt.circle("t", "y", source=data_source, color=COLORS[_h],
                   size=3, alpha=ALPHA_6)

    #
    # Append plot to HTML elements for final report.
    #
    HTML_ELEMS.append(plt)


def plot_resistance_vs_time(lt_name):
    """ ___ """

    #
    # Format plot.
    #
    plt = bokeh.plotting.figure(tools=TOOLS)
    plt.toolbar.logo = None
    plt.plot_width = PLOT_WIDTH
    plt.plot_height = PLOT_HEIGHT
    plt.add_layout(
        Title(
            text=f"{lt_name} — Resistance vs time",
            text_font_style="normal",
            align="center"),
        "above")
    plt.xaxis.axis_label = "Time (s)"
    plt.yaxis.axis_label = "Resistance (Ω)"
    plt.yaxis.formatter = NumeralTickFormatter(format="0")
    plt.x_range = HTML_ELEMS[0].x_range

    #
    # Prepare data source and plot data.
    #
    for _h in range(NB_HEIGHT):
        _t = LTDATA["KeithleyTimeStamp"][_h]
        _y = LTDATA["Resistance_ohm"][_h]
        data_source = ColumnDataSource(data=dict(t=_t, y=_y))

        plt.line("t", "y", source=data_source, color=COLORS[_h],
                 legend_label="Resistance (Ω)", alpha=ALPHA_1)
        plt.circle("t", "y", source=data_source, color=COLORS[_h],
                   size=3, alpha=ALPHA_6)

    #
    # Append plot to HTML elements for final report.
    #
    HTML_ELEMS.append(plt)


def plot_level_vs_time(lt_name):
    """ ___ """

    #
    # Format plot.
    #
    plt = bokeh.plotting.figure(tools=TOOLS)
    plt.toolbar.logo = None
    plt.plot_width = PLOT_WIDTH
    plt.plot_height = PLOT_HEIGHT
    plt.add_layout(
        Title(
            text=f"{lt_name} — Level vs time",
            text_font_style="normal",
            align="center"),
        "above")
    plt.xaxis.axis_label = "Time (s)"
    plt.yaxis.axis_label = "Level (mm)"
    plt.yaxis.formatter = NumeralTickFormatter(format="0")
    plt.x_range = HTML_ELEMS[0].x_range

    #
    # Prepare data source and plot data.
    #
    for _h in range(NB_HEIGHT):
        _t = LTDATA["KeithleyTimeStamp"][_h]
        _y = LTDATA["Level_mm"][_h]
        data_source = ColumnDataSource(data=dict(t=_t, y=_y))

        plt.line("t", "y", source=data_source, color=COLORS[_h],
                 legend_label="Level (mm)", alpha=ALPHA_1)
        plt.circle("t", "y", source=data_source, color=COLORS[_h],
                   size=3, alpha=ALPHA_6)

    #
    # Append plot to HTML elements for final report.
    #
    HTML_ELEMS.append(plt)


def plot_resistivity_vs_time(lt_name):
    """ ___ """

    #
    # Format plot.
    #
    plt = bokeh.plotting.figure(tools=TOOLS)
    plt.toolbar.logo = None
    plt.plot_width = PLOT_WIDTH
    plt.plot_height = PLOT_HEIGHT
    plt.add_layout(
        Title(
            text=f"{lt_name} — Resistivity vs time",
            text_font_style="normal",
            align="center"),
        "above")
    plt.xaxis.axis_label = "Time (s)"
    plt.yaxis.axis_label = "Resistivity (Ω/mm)"
    plt.yaxis.formatter = NumeralTickFormatter(format="0.000")
    plt.x_range = HTML_ELEMS[0].x_range

    #
    # Prepare data source and plot data.
    #
    for _h in range(NB_HEIGHT):
        _t = LTDATA["KeithleyTimeStamp"][_h]
        _y = LTDATA["resistivity"][_h]
        data_source = ColumnDataSource(data=dict(t=_t, y=_y))

        plt.line("t", "y", source=data_source, color=COLORS[_h],
                 legend_label="Resistivity (Ω/mm)", alpha=ALPHA_1)
        plt.circle("t", "y", source=data_source, color=COLORS[_h],
                   size=3, alpha=ALPHA_6)

    #
    # Append plot to HTML elements for final report.
    #
    HTML_ELEMS.append(plt)


def plot_resistance_vs_current(lt_name):
    """ ___ """

    #
    # Format plot.
    #
    plt = bokeh.plotting.figure(tools=TOOLS)
    plt.toolbar.logo = None
    plt.plot_width = PLOT_WIDTH
    plt.plot_height = PLOT_WIDTH
    plt.add_layout(
        Title(
            text=f"{lt_name} — Resistance vs current",
            text_font_style="normal",
            align="center"),
        "above")
    plt.xaxis.axis_label = "Current (A)"
    plt.yaxis.axis_label = "Resistance (Ω)"
    plt.yaxis.formatter = NumeralTickFormatter(format="0")

    #
    # Prepare data source and plot data.
    #
    for _h in range(NB_HEIGHT):
        _i = LTDATA["Current_A"][_h]
        _r = LTDATA["Resistance_ohm"][_h]
        data_source = ColumnDataSource(data=dict(i=_i, r=_r))

        plt.line("i", "r", source=data_source, color=COLORS[_h],
                 legend_label=f'R(I) @ L{LTDATA["Level_mm"][_h][0]:0.0f}mm (Ω)', alpha=ALPHA_6)
        plt.circle("i", "r", source=data_source, color=COLORS[_h],
                   size=3, alpha=ALPHA_1)

    #
    # Append plot to HTML elements for final report.
    #
    HTML_ELEMS.append(plt)


def write_to_html_file(lt_name):
    """ ___ """

    file_name = HTML_DIR + lt_name + ".html"
    output_file(file_name, title=f"{lt_name}")
    _c = column(children=HTML_ELEMS, sizing_mode="scale_width")
    if SHOW_HTML:
        show(_c)
    else:
        save(_c)


def init_logger():
    """
    50 CRITICAL, 40 ERROR, 30 WARNING, 20 INFO, 10 DEBUG, 0 NOTSET

    # To get the names of running loggers:
    loggers = [logging.getLogger(name)
                                 for name in logging.root.manager.loggerDict]
    print(loggers)
    """

    if not LOGGING_ENABLED:
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

    LOGGER.setLevel(LOGGING_LEVEL)

    LOGGER.debug("python %s", sys.version.split(" ")[0])
    LOGGER.debug("bokeh %s", bokeh.__version__)
    LOGGER.debug("numpy %s", np.__version__)


def process_lts(lt_name):
    """ ___ """

    LOGGER.debug("Processing %s", lt_name)
    readXML(lt_name)
    calc_resistivity(lt_name)
    plot_current_vs_time(lt_name)
    plot_resistance_vs_time(lt_name)
    plot_level_vs_time(lt_name)
    plot_resistivity_vs_time(lt_name)
    plot_resistance_vs_current(lt_name)
    write_to_html_file(lt_name)


def main():
    """ ___ """

    init_logger()
    lt_names = ["LT01", "LT30"]
    global HTML_ELEMS
    for _lt_name in lt_names:
        HTML_ELEMS = []
        process_lts(_lt_name)


if __name__ == "__main__":

    main()
