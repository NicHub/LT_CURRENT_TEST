#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

PLOT PLOTLY

This module shows some basic plotting techniques with Plotly.

@author         Nicolas Jeanmonod
@date           2020-12-21

Plotly documentation

    - HTML generation:
    https://plotly.github.io/plotly.py-docs/generated/plotly.io.to_html.html

    - Plot format
    https://plot.ly/python-api-reference/generated/plotly.graph_objects.Layout.html

"""

import logging
import os
import subprocess
import sys

import plotly as py
import plotly.graph_objs as go


class PlotPlotly():
    """ ___  """

    def __init__(self, settings, data):

        self.__settings = settings
        self.__data = data
        self.__html_elems = []

        self.__logger = logging.getLogger(__name__)
        self.__logger.debug("plotly %s", py.__version__)

        #
        # Color palette for plot lines
        # http://ksrowell.com/blog-visualizing-data/2012/02/02/optimal-colors-for-graphs/
        #
        self.__COLORS = {
            "background": "#FFF",
            "text": "red",
            "lines": [
                "rgb(57, 106, 177)",
                "rgb(218, 124, 48)",
                "rgb(62, 150, 81)",
                "rgb(204, 37, 41)",
                "rgb(83, 81, 84)",
                "rgb(107, 76, 154)",
                "rgb(146, 36, 40)",
                "rgb(148, 129, 61)",

                "rgb(57, 106, 177)",
                "rgb(218, 124, 48)",
                "rgb(62, 150, 81)",
                "rgb(204, 37, 41)",
                "rgb(83, 81, 84)",
                "rgb(107, 76, 154)",
                "rgb(146, 36, 40)",
                "rgb(148, 129, 61)",

                "rgb(57, 106, 177)",
                "rgb(218, 124, 48)",
                "rgb(62, 150, 81)",
                "rgb(204, 37, 41)",
                "rgb(83, 81, 84)",
                "rgb(107, 76, 154)",
                "rgb(146, 36, 40)",
                "rgb(148, 129, 61)",

                "rgb(57, 106, 177)",
                "rgb(218, 124, 48)",
                "rgb(62, 150, 81)",
                "rgb(204, 37, 41)",
                "rgb(83, 81, 84)",
                "rgb(107, 76, 154)",
                "rgb(146, 36, 40)",
                "rgb(148, 129, 61)",
            ],
            "marker_lines": [
                "rgb(57, 106, 177)",
                "rgb(218, 124, 48)",
                "rgb(62, 150, 81)",
                "rgb(204, 37, 41)",
                "rgb(83, 81, 84)",
                "rgb(107, 76, 154)",
                "rgb(146, 36, 40)",
                "rgb(148, 129, 61)"
            ],
            "marker_bkg": [
                "rgb(57, 106, 177)",
                "rgb(218, 124, 48)",
                "rgb(62, 150, 81)",
                "rgb(204, 37, 41)",
                "rgb(83, 81, 84)",
                "rgb(107, 76, 154)",
                "rgb(146, 36, 40)",
                "rgb(148, 129, 61)"
            ]
        }
        self.__OPACITIES = {
            "lines": 1,
            "markers": 0.5
        }
        self.__WIDTHS = {
            "lines": 1,
            "marker_lines": 1,
        }
        self.__SIZES = {
            "markers": 4,
        }

    def title(self):
        """ ___ """

        title = f"""
<div style="
     margin-bottom:50px;
     text-align: center;
     font-family: 'PT Sans', monospace;
     text-transform: uppercase;">
    <h1>{self.__data["lt_name"]} Measurements</h1>
    <h2>Plotly plots</h2>
</div>
"""
        self.__html_elems.append(title)

    def plot_current_vs_time(self):
        """ ___ """

        #
        # Prepare data source.
        #
        _x = self.__data["lt_data"]["KeithleyTimeStamp"]
        _y = self.__data["lt_data"]["Current_A"]

        #
        # Create plot.
        #
        data = []
        for level in range(self.__data["level_count"]):
            level_val = self.__data["lt_data"]["Level_mm"][level][0]
            legend_label = f"I(t) @ L{level_val:0.0f}mm"
            trace = go.Scatter(
                x=_x[level],
                y=_y[level],
                mode="lines+markers",
                opacity=self.__OPACITIES["lines"],
                line={
                    "color": self.__settings["GENERAL"]["COLORS"][level],
                    "width": self.__WIDTHS["lines"]
                },
                marker={
                    "size": self.__SIZES["markers"],
                    "line": {"width": self.__WIDTHS["marker_lines"],
                             "color": self.__settings["GENERAL"]["COLORS"][level]},
                    "color": self.__settings["GENERAL"]["COLORS"][level],
                    "opacity": self.__OPACITIES["markers"],
                },
                name=legend_label
            )

            data.append(trace)

        #
        # Layout.
        #
        layout = go.Layout(
            title={
                "text":
                f'<span style="font-weight:bold; text-transform:uppercase">'
                f'{self.__data["lt_name"]} — Current vs time',
                "x": 0.5,
                "y": 0.9,
                "xanchor": "center",
                "yanchor": "top",
            },
            plot_bgcolor=self.__COLORS["background"],
            paper_bgcolor=self.__COLORS["background"],
            xaxis={"title": "Time (s)", "ticklen": 5, "zeroline": False, "automargin": True,
                   "showgrid": True, "gridcolor": "rgba(0, 0, 0, 0.1)",
                   "ticks": "inside",  "showline": True, "linewidth": 1,
                   "linecolor": "black", "mirror": True, },
            yaxis={"title": "Current (A)", "ticklen": 5, "zeroline": False, "automargin": True,
                   "showgrid": True, "gridcolor": "rgba(0, 0, 0, 0.1)",
                   "ticks": "inside",  "showline": True, "linewidth": 1,
                   "linecolor": "black", "mirror": True},
            hovermode="closest",
            height=self.__settings["GENERAL"]["PLOT_HEIGHT"],
            width=self.__settings["GENERAL"]["PLOT_WIDTH"],
        )

        #
        # Create figure and append it to the HTML to be displayed.
        #
        fig = go.Figure(data=data, layout=layout).to_html(
            full_html=False,
            include_plotlyjs="cdn",
            include_mathjax=False,
            config={"scrollZoom": False})
        self.__html_elems.append(fig)

    def plot_resistance_vs_time(self):
        """ ___ """

        #
        # Prepare data source.
        #
        _x = self.__data["lt_data"]["KeithleyTimeStamp"]
        _y = self.__data["lt_data"]["Resistance_ohm"]

        #
        # Create plot.
        #
        data = []
        for level in range(self.__data["level_count"]):
            level_val = self.__data["lt_data"]["Level_mm"][level][0]
            legend_label = f"R(t) @ L{level_val:0.0f}mm"
            trace = go.Scatter(
                x=_x[level],
                y=_y[level],
                mode="lines+markers",
                opacity=self.__OPACITIES["lines"],
                line={
                    "color": self.__settings["GENERAL"]["COLORS"][level],
                    "width": self.__WIDTHS["lines"]
                },
                marker={
                    "size": self.__SIZES["markers"],
                    "line": {"width": self.__WIDTHS["marker_lines"],
                             "color": self.__settings["GENERAL"]["COLORS"][level]},
                    "color": self.__settings["GENERAL"]["COLORS"][level],
                    "opacity": self.__OPACITIES["markers"],
                },
                name=legend_label
            )

            data.append(trace)

        #
        # Layout.
        #
        layout = go.Layout(
            title={
                "text":
                f'<span style="font-weight:bold; text-transform:uppercase">'
                f'{self.__data["lt_name"]} — Resistance vs time',
                "x": 0.5,
                "y": 0.9,
                "xanchor": "center",
                "yanchor": "top",
            },
            plot_bgcolor=self.__COLORS["background"],
            paper_bgcolor=self.__COLORS["background"],
            xaxis={"title": "Time (s)", "ticklen": 5, "zeroline": False, "automargin": True,
                   "showgrid": True, "gridcolor": "rgba(0, 0, 0, 0.1)",
                   "ticks": "inside",  "showline": True, "linewidth": 1,
                   "linecolor": "black", "mirror": True, },
            yaxis={"title": "Resistance (Ω)", "ticklen": 5, "zeroline": False, "automargin": True,
                   "showgrid": True, "gridcolor": "rgba(0, 0, 0, 0.1)",
                   "ticks": "inside",  "showline": True, "linewidth": 1,
                   "linecolor": "black", "mirror": True},
            hovermode="closest",
            height=self.__settings["GENERAL"]["PLOT_HEIGHT"],
            width=self.__settings["GENERAL"]["PLOT_WIDTH"],
        )

        #
        # Create figure and append it to the HTML to be displayed.
        #
        fig = go.Figure(data=data, layout=layout).to_html(
            full_html=False,
            include_plotlyjs="cdn",
            include_mathjax=False,
            config={"scrollZoom": False})
        self.__html_elems.append(fig)

    def plot_level_vs_time(self):
        """ ___ """

        #
        # Prepare data source.
        #
        _x = self.__data["lt_data"]["KeithleyTimeStamp"]
        _y = self.__data["lt_data"]["Level_mm"]

        #
        # Create plot.
        #
        data = []
        for level in range(self.__data["level_count"]):
            level_val = self.__data["lt_data"]["Level_mm"][level][0]
            legend_label = f"L(t) @ L{level_val:0.0f}mm"
            trace = go.Scatter(
                x=_x[level],
                y=_y[level],
                mode="lines+markers",
                opacity=self.__OPACITIES["lines"],
                line={
                    "color": self.__settings["GENERAL"]["COLORS"][level],
                    "width": self.__WIDTHS["lines"]
                },
                marker={
                    "size": self.__SIZES["markers"],
                    "line": {"width": self.__WIDTHS["marker_lines"],
                             "color": self.__settings["GENERAL"]["COLORS"][level]},
                    "color": self.__settings["GENERAL"]["COLORS"][level],
                    "opacity": self.__OPACITIES["markers"],
                },
                name=legend_label
            )

            data.append(trace)

        #
        # Layout.
        #
        layout = go.Layout(
            title={
                "text":
                f'<span style="font-weight:bold; text-transform:uppercase">'
                f'{self.__data["lt_name"]} — Level vs time',
                "x": 0.5,
                "y": 0.9,
                "xanchor": "center",
                "yanchor": "top",
            },
            plot_bgcolor=self.__COLORS["background"],
            paper_bgcolor=self.__COLORS["background"],
            xaxis={"title": "Time (s)", "ticklen": 5, "zeroline": False, "automargin": True,
                   "showgrid": True, "gridcolor": "rgba(0, 0, 0, 0.1)",
                   "ticks": "inside",  "showline": True, "linewidth": 1,
                   "linecolor": "black", "mirror": True, },
            yaxis={"title": "Level (mm)", "ticklen": 5, "zeroline": False, "automargin": True,
                   "showgrid": True, "gridcolor": "rgba(0, 0, 0, 0.1)",
                   "ticks": "inside",  "showline": True, "linewidth": 1,
                   "linecolor": "black", "mirror": True},
            hovermode="closest",
            height=self.__settings["GENERAL"]["PLOT_HEIGHT"],
            width=self.__settings["GENERAL"]["PLOT_WIDTH"],
        )

        #
        # Create figure and append it to the HTML to be displayed.
        #
        fig = go.Figure(data=data, layout=layout).to_html(
            full_html=False,
            include_plotlyjs="cdn",
            include_mathjax=False,
            config={"scrollZoom": False})
        self.__html_elems.append(fig)

    def plot_resistivity_vs_time(self):
        """ ___ """

        #
        # Prepare data source.
        #
        _x = self.__data["lt_data"]["KeithleyTimeStamp"]
        _y = self.__data["lt_data"]["resistivity"]

        #
        # Create plot.
        #
        data = []
        for level in range(self.__data["level_count"]):
            level_val = self.__data["lt_data"]["Level_mm"][level][0]
            legend_label = f"ϱ(t) @ L{level_val:0.0f}mm"
            trace = go.Scatter(
                x=_x[level],
                y=_y[level],
                mode="lines+markers",
                opacity=self.__OPACITIES["lines"],
                line={
                    "color": self.__settings["GENERAL"]["COLORS"][level],
                    "width": self.__WIDTHS["lines"]
                },
                marker={
                    "size": self.__SIZES["markers"],
                    "line": {"width": self.__WIDTHS["marker_lines"],
                             "color": self.__settings["GENERAL"]["COLORS"][level]},
                    "color": self.__settings["GENERAL"]["COLORS"][level],
                    "opacity": self.__OPACITIES["markers"],
                },
                name=legend_label
            )

            data.append(trace)

        #
        # Layout.
        #
        layout = go.Layout(
            title={
                "text":
                f'<span style="font-weight:bold; text-transform:uppercase">'
                f'{self.__data["lt_name"]} — Resistivity vs time',
                "x": 0.5,
                "y": 0.9,
                "xanchor": "center",
                "yanchor": "top",
            },
            plot_bgcolor=self.__COLORS["background"],
            paper_bgcolor=self.__COLORS["background"],
            xaxis={"title": "Time (s)", "ticklen": 5, "zeroline": False, "automargin": True,
                   "showgrid": True, "gridcolor": "rgba(0, 0, 0, 0.1)",
                   "ticks": "inside",  "showline": True, "linewidth": 1,
                   "linecolor": "black", "mirror": True, },
            yaxis={"title": "Resistivity (Ω/mm)", "ticklen": 5, "zeroline": False, "automargin": True,
                   "showgrid": True, "gridcolor": "rgba(0, 0, 0, 0.1)",
                   "ticks": "inside",  "showline": True, "linewidth": 1,
                   "linecolor": "black", "mirror": True},
            hovermode="closest",
            height=self.__settings["GENERAL"]["PLOT_HEIGHT"],
            width=self.__settings["GENERAL"]["PLOT_WIDTH"],
        )

        #
        # Create figure and append it to the HTML to be displayed.
        #
        fig = go.Figure(data=data, layout=layout).to_html(
            full_html=False,
            include_plotlyjs="cdn",
            include_mathjax=False,
            config={"scrollZoom": False})
        self.__html_elems.append(fig)

    def plot_resistance_vs_current(self):
        """ ___ """

        #
        # Prepare data source.
        #
        _x = self.__data["lt_data"]["Current_A"]
        _y = self.__data["lt_data"]["Resistance_ohm"]

        #
        # Create plot.
        #
        data = []
        for level in range(self.__data["level_count"]):
            level_val = self.__data["lt_data"]["Level_mm"][level][0]
            legend_label = f"R(I) @ L{level_val:0.0f}mm"
            trace = go.Scatter(
                x=_x[level],
                y=_y[level],
                mode="lines+markers",
                opacity=self.__OPACITIES["lines"],
                line={
                    "color": self.__settings["GENERAL"]["COLORS"][level],
                    "width": self.__WIDTHS["lines"]
                },
                marker={
                    "size": self.__SIZES["markers"],
                    "line": {"width": self.__WIDTHS["marker_lines"],
                             "color": self.__settings["GENERAL"]["COLORS"][level]},
                    "color": self.__settings["GENERAL"]["COLORS"][level],
                    "opacity": self.__OPACITIES["markers"],
                },
                name=legend_label
            )

            data.append(trace)

        #
        # Layout.
        #
        layout = go.Layout(
            title={
                "text":
                f'<span style="font-weight:bold; text-transform:uppercase">'
                f'{self.__data["lt_name"]} — Resistance vs current</span>',
                "x": 0.5,
                "y": 0.95,
                "xanchor": "center",
                "yanchor": "top",
            },
            plot_bgcolor=self.__COLORS["background"],
            paper_bgcolor=self.__COLORS["background"],
            xaxis={"title": "Current (A)", "ticklen": 5, "zeroline": False, "automargin": True,
                   "showgrid": True, "gridcolor": "rgba(0, 0, 0, 0.1)",
                   "ticks": "inside",  "showline": True, "linewidth": 1,
                   "linecolor": "black", "mirror": True, },
            yaxis={"title": "Resistance (Ω)", "ticklen": 5, "zeroline": False, "automargin": True,
                   "showgrid": True, "gridcolor": "rgba(0, 0, 0, 0.1)",
                   "ticks": "inside",  "showline": True, "linewidth": 1,
                   "linecolor": "black", "mirror": True},
            hovermode="closest",
            height=self.__settings["GENERAL"]["PLOT_WIDTH"],
            width=self.__settings["GENERAL"]["PLOT_WIDTH"],
        )

        #
        # Create figure and append it to the HTML to be displayed.
        #
        fig = go.Figure(data=data, layout=layout).to_html(
            full_html=False,
            include_plotlyjs="cdn",
            include_mathjax=False,
            config={"scrollZoom": False})
        self.__html_elems.append(fig)

    def open_file(self, filename):
        if sys.platform == "win32":
            os.startfile(filename)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filename])

    def write_to_html_file(self):
        """ ___ """

        #
        # Create output dir if it does not exist.
        #
        if not os.path.isdir(self.__settings["PLOTLY"]["OUT_DIR"]):
            self.__logger.debug("Creating output dir %s",
                                self.__settings["PLOTLY"]["OUT_DIR"])
            os.makedirs(self.__settings["PLOTLY"]["OUT_DIR"])

        file_name = self.__settings["PLOTLY"]["OUT_DIR"] + \
            self.__data["lt_name"] + ".html"

        #
        # Save the report and display it if SHOW_HTML == True
        #
        start_html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>{self.__data["lt_name"]} • Plotly</title>
<style>
.centered{{width:{self.__settings["GENERAL"]["PLOT_WIDTH"]}px; margin: 0 auto; text-align: center;}}
.page-break-inside-avoid{{page-break-inside: avoid;}}
</style>
</head>
<body>
<div class="centered">"""
        end_html = "\n</div>\n</body>\n</html>"
        html_file = open(file_name, 'w')
        html_file.write(start_html)
        for htmL_elem in self.__html_elems:
            inner_html = '<div class=".page-break-inside-avoid">'
            inner_html += htmL_elem
            inner_html += '</div>'
            html_file.write(inner_html)
        html_file.write(end_html)

        if self.__settings["GENERAL"]["SHOW_HTML"]:
            self.open_file(file_name)
