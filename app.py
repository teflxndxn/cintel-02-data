import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
import palmerpenguins  # This package provides the Palmer Penguins dataset

penguins_df = palmerpenguins.load_penguins()

ui.page_opts(title="Peng Data - Blessing", fillable=True)

with ui.layout_columns():

    @render_plotly
    def plot1():
        # Histogram of species counts
        return px.histogram(penguins_df, x="species", title="Penguin Species Count")

    @render_plotly
    def plot2():
        # Histogram of flipper length distribution
        return px.histogram(penguins_df, x="flipper_length_mm", title="Flipper Length Distribution")
