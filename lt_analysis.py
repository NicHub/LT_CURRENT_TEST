#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import xml.etree.ElementTree as ET
import bokeh
from bokeh.plotting import figure, output_notebook, output_file, show, save
from bokeh.core.properties import value
from bokeh.models import Circle, ColumnDataSource, Line, LinearAxis, Range1d, \
    Title, NumeralTickFormatter, DatetimeTickFormatter, RangeTool, CustomJS, Slider
from bokeh.io import output_file, show, export_svgs, export_png,  reset_output
from bokeh.layouts import row, column, widgetbox, gridplot
from bokeh.models.widgets import Div, Paragraph, PreText


LTDATA = {}
TOOLS = 'pan, box_zoom, wheel_zoom, save, reset, xzoom_in, xzoom_out'
PLOT_WIDTH = 1600
PLOT_HEIGHT = 400
HTML_ELEMS = []
XML_DIR = "./data/"
HTML_DIR = "./out_python/"
LINE_ALPHA = 0.1
CIRCLE_ALPHA = 0.6


def readXML(lt_name):
    """

    """
    file_name = XML_DIR + lt_name + ".xml"
    tree = ET.parse(file_name)
    root = tree.getroot()
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

            nb_meas, nb_height = _elem.attrib["size"].split(" ")

            nb_meas = int(nb_meas)
            nb_height = int(nb_height)

            reshape = False
            if reshape:
                LTDATA[child.tag] = np.asarray(_elem.text.split(" ")).astype(
                    'float64').reshape(nb_height, nb_meas).T
            else:
                LTDATA[child.tag] = np.asarray(
                    _elem.text.split(" ")).astype('float64')

    if not reshape:
        LTDATA["KeithleyTimeStamp"] -= LTDATA["KeithleyTimeStamp"][0]


def calc_resistivity(lt_name):
    max_length = 400
    LTDATA["resistivity"] = LTDATA["Resistance_ohm"] / \
        (max_length-LTDATA["Level_mm"])


def plot_current_vs_time(lt_name):
    """

    """

    #
    # Prepare data source.
    #
    _t = LTDATA["KeithleyTimeStamp"]
    _y = LTDATA["Current_A"]
    data_source = ColumnDataSource(data=dict(t=_t, y=_y))

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
    # Plot data.
    #
    plt.line("t", "y", source=data_source,
             legend_label="Current (A)", alpha=LINE_ALPHA)
    plt.circle("t", "y", source=data_source, size=3, alpha=CIRCLE_ALPHA)

    #
    # Append plot to HTML elements for final report.
    #
    HTML_ELEMS.append(plt)


def plot_resistance_vs_time(lt_name):
    """

    """

    #
    # Prepare data source.
    #
    _t = LTDATA["KeithleyTimeStamp"]
    _y = LTDATA["Resistance_ohm"]
    data_source = ColumnDataSource(data=dict(t=_t, y=_y))

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
    # Plot data.
    #
    plt.line("t", "y", source=data_source,
             legend_label="Resistance (Ω)", alpha=LINE_ALPHA)
    plt.circle("t", "y", source=data_source, size=3, alpha=CIRCLE_ALPHA)

    #
    # Append plot to HTML elements for final report.
    #
    HTML_ELEMS.append(plt)


def plot_level_vs_time(lt_name):
    """

    """

    #
    # Prepare data source.
    #
    _t = LTDATA["KeithleyTimeStamp"]
    _y = LTDATA["Level_mm"]
    data_source = ColumnDataSource(data=dict(t=_t, y=_y))

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
    # Plot data.
    #
    plt.line("t", "y", source=data_source,
             legend_label="Level (mm)", alpha=LINE_ALPHA)
    plt.circle("t", "y", source=data_source, size=3, alpha=CIRCLE_ALPHA)

    #
    # Append plot to HTML elements for final report.
    #
    HTML_ELEMS.append(plt)


def plot_resistivity_vs_time(lt_name):
    """

    """

    #
    # Prepare data source.
    #
    _t = LTDATA["KeithleyTimeStamp"]
    _y = LTDATA["resistivity"]
    data_source = ColumnDataSource(data=dict(t=_t, y=_y))

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
    # Plot data.
    #
    plt.line("t", "y", source=data_source,
             legend_label="Resistivity (Ω/mm)", alpha=LINE_ALPHA)
    plt.circle("t", "y", source=data_source, size=3, alpha=CIRCLE_ALPHA)

    #
    # Append plot to HTML elements for final report.
    #
    HTML_ELEMS.append(plt)


def write_to_html_file(lt_name, showHTML):
    """

    """
    file_name = HTML_DIR + lt_name + ".html"
    output_file(file_name, title=f'{lt_name}')
    _w = widgetbox(children=HTML_ELEMS, sizing_mode='scale_width')
    if showHTML:
        show(_w)
    else:
        save(_w)


def main(lt_name):
    """

    """
    readXML(lt_name)
    calc_resistivity(lt_name)
    plot_current_vs_time(lt_name)
    plot_resistance_vs_time(lt_name)
    plot_level_vs_time(lt_name)
    plot_resistivity_vs_time(lt_name)
    write_to_html_file(lt_name, True)


if __name__ == "__main__":
    """

    """
    lt_names = ["LT01", "LT30"]
    for _lt_name in lt_names:
        HTML_ELEMS = []
        main(_lt_name)
