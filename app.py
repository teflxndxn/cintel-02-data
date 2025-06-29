from shiny import ui, App, render
from shinywidgets import render_plotly
import plotly.express as px
from palmerpenguins import load_penguins
import matplotlib.pyplot as plt
import seaborn as sns

# Load penguins data once at start
penguins_df = load_penguins()

app_ui = ui.page_fluid(
    ui.sidebar(
        ui.h2("Sidebar"),
        ui.input_selectize(
            "selected_attribute",
            "Select Attribute",
            ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
            selected="bill_length_mm"
        ),
        ui.input_numeric("plotly_bin_count", "Plotly Histogram Bins", 30),
        ui.input_slider("seaborn_bin_count", "Seaborn Histogram Bins", 1, 100, 20),
        ui.input_checkbox_group(
            "selected_species_list",
            "Select Species",
            ["Adelie", "Gentoo", "Chinstrap"],
            selected=["Adelie", "Gentoo", "Chinstrap"],
            inline=True
        ),
        ui.hr(),
        ui.a("GitHub", href="https://github.com/teflxndxn/cintel-02-data", target="_blank"),
        open="open",
    ),

    ui.layout_columns(
        ui.output_table("datatable"),
        ui.output_text("datagrid_placeholder"),
    ),
    ui.layout_columns(
        ui.output_plot("plotly_histogram"),
        ui.output_plot("seaborn_histogram_placeholder"),
    ),

    ui.card(
        ui.card_header("Plotly Scatterplot: Species"),
        ui.output_plot("plotly_scatterplot"),
        full_screen=True
    ),
)

def server(input, output, session):

    def get_filtered_df():
        selected_species = input.selected_species_list()
        if not selected_species:
            return penguins_df.iloc[0:0]  # empty df if nothing selected
        return penguins_df[penguins_df["species"].isin(selected_species)]

    @output
    @render.table
    def datatable():
        return get_filtered_df()

    @output
    @render.text
    def datagrid_placeholder():
        return "Data Grid will be implemented here in a future environment."

    @output
    @render_plotly
    def plotly_histogram():
        df_filtered = get_filtered_df()
        selected_col = input.selected_attribute()
        if not isinstance(selected_col, str):
            selected_col = "bill_length_mm"
        bin_count = input.plotly_bin_count() or 30

        # Drop NaN values for selected column
        df_filtered = df_filtered.dropna(subset=[selected_col])

        return px.histogram(df_filtered, x=selected_col, nbins=bin_count)

    @output
    @render_plotly
    def plotly_scatterplot():
        df_filtered = get_filtered_df()

        # Drop rows with NaN values in relevant columns
        df_filtered = df_filtered.dropna(subset=["bill_length_mm", "body_mass_g", "flipper_length_mm"])

        return px.scatter(
            df_filtered,
            x="bill_length_mm",
            y="body_mass_g",
            color="species",
            title="Plotly Scatterplot: Species",
            hover_data=["flipper_length_mm"]
        )

    @output
    @render.plot
    def seaborn_histogram_placeholder():
        df_filtered = get_filtered_df()
        selected_col = input.selected_attribute()
        if not isinstance(selected_col, str):
            selected_col = "bill_length_mm"
        bin_count = input.seaborn_bin_count() or 20

        plt.figure(figsize=(6, 4))
        sns.histplot(df_filtered[selected_col].dropna(), bins=bin_count, kde=False, color="skyblue")
        plt.title(f"Seaborn Histogram: {selected_col}")
        plt.xlabel(selected_col)
        plt.ylabel("Count")
        plt.tight_layout()
        return plt.gcf()

app = App(app_ui, server)
