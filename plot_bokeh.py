#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

PLOT BOKEH

This module shows some basic plotting techniques with Bokeh.

@author         Nicolas Jeanmonod
@date           2020-12-20

"""


import logging
import os

import bokeh
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Legend, NumeralTickFormatter, Title
from bokeh.models.widgets import Div
from bokeh.plotting import figure, output_file, save, show


class PlotBokeh():
    """ ___ """

    def __init__(self, settings, data):
        """ ___ """

        self.__settings = settings
        self.__data = data
        self.__html_elems = []
        self.__plot_margin = (20, 100, 20, 100)

        # ID of the plot that is used for common x_range.
        self.__master_x_range = 1

        self.__logger = logging.getLogger(__name__)
        self.__logger.debug("bokeh %s", bokeh.__version__)

    def title(self):
        """ ___ """

        title = Div(
            text=f"""
                <h1>{self.__data["lt_name"]} Measurements</h1>
                <h2>Bokeh plots</h2>
                """,
            style={
                "width": "100%",
                "height": "100px",
                "text-align": "center",
                "text-transform": "uppercase"
            },
            margin=self.__plot_margin
        )
        self.__html_elems.append(title)

    def plot_current_vs_time(self):
        """ ___ """

        #
        # Create figure, prepare data source and plot data.
        #
        plt = figure(tools=self.__settings["BOKEH"]["TOOLS"])
        legend_labels = []

        for level in range(self.__data["level_count"]):
            _t = self.__data["lt_data"]["KeithleyTimeStamp"][level]
            _y = self.__data["lt_data"]["Current_A"][level]
            data_source = ColumnDataSource(data=dict(t=_t, y=_y))

            pl = plt.line("t", "y", source=data_source,
                          color=self.__settings["GENERAL"]["COLORS"][level],
                          alpha=self.__settings["BOKEH"]["ALPHA_1"])
            pc = plt.circle("t", "y", source=data_source,
                            color=self.__settings["GENERAL"]["COLORS"][level],
                            size=self.__settings["BOKEH"]["CIRCLE_SIZE"],
                            alpha=self.__settings["BOKEH"]["ALPHA_6"])

            level_val = self.__data["lt_data"]["Level_mm"][level][0]
            legend_label = f"I(t) @ L{level_val:0.0f}mm"
            legend_labels.append((legend_label, [pl, pc]))

        #
        # Format plot.
        #
        plt.toolbar.logo = None
        plt.plot_width = self.__settings["GENERAL"]["PLOT_WIDTH"]
        plt.plot_height = self.__settings["GENERAL"]["PLOT_HEIGHT"]
        plt.add_layout(
            Title(
                text=f'{self.__data["lt_name"]} — Current vs time',
                text_font_style="normal",
                align="center"),
            "above")
        plt.xaxis.axis_label = "Time (s)"
        plt.yaxis.axis_label = "Current (A)"
        plt.yaxis.formatter = NumeralTickFormatter(format="0.000")
        plt.margin = self.__plot_margin
        legend = Legend(items=legend_labels, location="top_center")
        plt.add_layout(legend, "right")
        plt.legend.click_policy = "hide"

        #
        # Append plot to HTML elements for final report.
        #
        self.__html_elems.append(plt)

    def plot_resistance_vs_time(self):
        """ ___ """

        #
        # Create figure, prepare data source and plot data.
        #
        plt = figure(tools=self.__settings["BOKEH"]["TOOLS"])
        legend_labels = []

        for level in range(self.__data["level_count"]):
            _t = self.__data["lt_data"]["KeithleyTimeStamp"][level]
            _y = self.__data["lt_data"]["Resistance_ohm"][level]
            data_source = ColumnDataSource(data=dict(t=_t, y=_y))

            pl = plt.line("t", "y", source=data_source,
                          color=self.__settings["GENERAL"]["COLORS"][level],
                          alpha=self.__settings["BOKEH"]["ALPHA_1"])
            pc = plt.circle("t", "y", source=data_source,
                            color=self.__settings["GENERAL"]["COLORS"][level],
                            size=self.__settings["BOKEH"]["CIRCLE_SIZE"],
                            alpha=self.__settings["BOKEH"]["ALPHA_6"])

            level_val = self.__data["lt_data"]["Level_mm"][level][0]
            legend_label = f"R(t) @ L{level_val:0.0f}mm"
            legend_labels.append((legend_label, [pl, pc]))

        #
        # Format plot.
        #
        plt.toolbar.logo = None
        plt.plot_width = self.__settings["GENERAL"]["PLOT_WIDTH"]
        plt.plot_height = self.__settings["GENERAL"]["PLOT_HEIGHT"]
        plt.add_layout(
            Title(
                text=f'{self.__data["lt_name"]} — Resistance vs time',
                text_font_style="normal",
                align="center"),
            "above")
        plt.xaxis.axis_label = "Time (s)"
        plt.yaxis.axis_label = "Resistance (Ω)"
        plt.yaxis.formatter = NumeralTickFormatter(format="0")
        plt.x_range = self.__html_elems[self.__master_x_range].x_range
        plt.margin = self.__plot_margin
        legend = Legend(items=legend_labels, location="top_center")
        plt.add_layout(legend, "right")
        plt.legend.click_policy = "hide"

        #
        # Append plot to HTML elements for final report.
        #
        self.__html_elems.append(plt)

    def plot_level_vs_time(self):
        """ ___ """

        #
        # Create figure, prepare data source and plot data.
        #
        plt = figure(tools=self.__settings["BOKEH"]["TOOLS"])
        legend_labels = []

        for level in range(self.__data["level_count"]):
            _t = self.__data["lt_data"]["KeithleyTimeStamp"][level]
            _y = self.__data["lt_data"]["Level_mm"][level]
            data_source = ColumnDataSource(data=dict(t=_t, y=_y))

            pl = plt.line("t", "y", source=data_source,
                          color=self.__settings["GENERAL"]["COLORS"][level],
                          alpha=self.__settings["BOKEH"]["ALPHA_1"])
            pc = plt.circle("t", "y", source=data_source,
                            color=self.__settings["GENERAL"]["COLORS"][level],
                            size=self.__settings["BOKEH"]["CIRCLE_SIZE"],
                            alpha=self.__settings["BOKEH"]["ALPHA_6"])

            level_val = self.__data["lt_data"]["Level_mm"][level][0]
            legend_label = f"L(t) @ L{level_val:0.0f}mm"
            legend_labels.append((legend_label, [pl, pc]))

        #
        # Format plot.
        #
        plt.toolbar.logo = None
        plt.plot_width = self.__settings["GENERAL"]["PLOT_WIDTH"]
        plt.plot_height = self.__settings["GENERAL"]["PLOT_HEIGHT"]
        plt.add_layout(
            Title(
                text=f'{self.__data["lt_name"]} — Level vs time',
                text_font_style="normal",
                align="center"),
            "above")
        plt.xaxis.axis_label = "Time (s)"
        plt.yaxis.axis_label = "Level (mm)"
        plt.yaxis.formatter = NumeralTickFormatter(format="0")
        plt.x_range = self.__html_elems[self.__master_x_range].x_range
        plt.margin = self.__plot_margin
        legend = Legend(items=legend_labels, location="top_center")
        plt.add_layout(legend, "right")
        plt.legend.click_policy = "hide"

        #
        # Append plot to HTML elements for final report.
        #
        self.__html_elems.append(plt)

    def plot_resistivity_vs_time(self):
        """ ___ """

        #
        # Create figure, prepare data source and plot data.
        #
        plt = figure(tools=self.__settings["BOKEH"]["TOOLS"])
        legend_labels = []

        for level in range(self.__data["level_count"]):
            _t = self.__data["lt_data"]["KeithleyTimeStamp"][level]
            _y = self.__data["lt_data"]["resistivity"][level]
            data_source = ColumnDataSource(data=dict(t=_t, y=_y))

            pl = plt.line("t", "y", source=data_source,
                          color=self.__settings["GENERAL"]["COLORS"][level],
                          alpha=self.__settings["BOKEH"]["ALPHA_1"])
            pc = plt.circle("t", "y", source=data_source,
                            color=self.__settings["GENERAL"]["COLORS"][level],
                            size=self.__settings["BOKEH"]["CIRCLE_SIZE"],
                            alpha=self.__settings["BOKEH"]["ALPHA_6"])

            level_val = self.__data["lt_data"]["Level_mm"][level][0]
            legend_label = f"ϱ(t) @ L{level_val:0.0f}mm"
            legend_labels.append((legend_label, [pl, pc]))

        #
        # Format plot.
        #
        plt.toolbar.logo = None
        plt.plot_width = self.__settings["GENERAL"]["PLOT_WIDTH"]
        plt.plot_height = self.__settings["GENERAL"]["PLOT_HEIGHT"]
        plt.add_layout(
            Title(
                text=f'{self.__data["lt_name"]} — Resistivity vs time',
                text_font_style="normal",
                align="center"),
            "above")
        plt.xaxis.axis_label = "Time (s)"
        plt.yaxis.axis_label = "Resistivity (Ω/mm)"
        plt.yaxis.formatter = NumeralTickFormatter(format="0.000")
        plt.x_range = self.__html_elems[self.__master_x_range].x_range
        plt.margin = self.__plot_margin
        legend = Legend(items=legend_labels, location="top_center")
        plt.add_layout(legend, "right")
        plt.legend.click_policy = "hide"

        #
        # Append plot to HTML elements for final report.
        #
        self.__html_elems.append(plt)

    def plot_resistance_vs_current(self):
        """ ___ """

        #
        # Create figure, prepare data source and plot data.
        #
        plt = figure(tools=self.__settings["BOKEH"]["TOOLS"])
        legend_labels = []

        for level in range(self.__data["level_count"]):
            _i = self.__data["lt_data"]["Current_A"][level]
            _r = self.__data["lt_data"]["Resistance_ohm"][level]
            data_source = ColumnDataSource(data=dict(i=_i, r=_r))

            pl = plt.line("i", "r", source=data_source,
                          color=self.__settings["GENERAL"]["COLORS"][level],
                          alpha=self.__settings["BOKEH"]["ALPHA_6"])
            pc = plt.circle("i", "r", source=data_source,
                            color=self.__settings["GENERAL"]["COLORS"][level],
                            size=self.__settings["BOKEH"]["CIRCLE_SIZE"],
                            alpha=self.__settings["BOKEH"]["ALPHA_1"])

            level_val = self.__data["lt_data"]["Level_mm"][level][0]
            legend_label = f"R(I) @ L{level_val:0.0f}mm"
            legend_labels.append((legend_label, [pl, pc]))

        #
        # Format plot.
        #
        plt.toolbar.logo = None
        plt.plot_width = self.__settings["GENERAL"]["PLOT_WIDTH"]
        plt.plot_height = self.__settings["GENERAL"]["PLOT_WIDTH"]
        plt.add_layout(
            Title(
                text=f'{self.__data["lt_name"]} — Resistance vs current',
                text_font_style="normal",
                align="center"),
            "above")
        plt.xaxis.axis_label = "Current (A)"
        plt.yaxis.axis_label = "Resistance (Ω)"
        plt.yaxis.formatter = NumeralTickFormatter(format="0")
        plt.margin = self.__plot_margin
        legend = Legend(items=legend_labels, location="top_center")
        plt.add_layout(legend, "right")
        plt.legend.click_policy = "hide"

        #
        # Append plot to HTML elements for final report.
        #
        self.__html_elems.append(plt)

    def write_to_html_file(self):
        """ ___ """

        #
        # Create output dir if it does not exist.
        #
        if not os.path.isdir(self.__settings["BOKEH"]["OUT_DIR"]):
            self.__logger.debug("Creating output dir %s",
                                self.__settings["BOKEH"]["OUT_DIR"])
            os.mkdir(self.__settings["BOKEH"]["OUT_DIR"])

        file_name = self.__settings["BOKEH"]["OUT_DIR"] + \
            self.__data["lt_name"] + ".html"
        output_file(file_name, title=f'{self.__data["lt_name"]} • Bokeh')

        html_out = column(children=self.__html_elems,
                          sizing_mode="stretch_width")

        # show and save are very slow (> 1 s).
        if self.__settings["GENERAL"]["SHOW_HTML"]:
            show(html_out)
        else:
            save(html_out)
