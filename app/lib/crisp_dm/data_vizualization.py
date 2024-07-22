from typing import Optional
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pydantic import BaseModel, field_validator
from IPython.display import Markdown, display

class DataVisualization(BaseModel):
    """
    Class to visualize data from a pandas DataFrame.

    Attributes:
        df (pd.DataFrame): The DataFrame to be visualized.
    """

    df: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True

    @field_validator("df")
    def validate_dataframe(cls, v):
        """
        Validates if the df attribute is a pandas DataFrame.

        Args:
            v: The value to be validated.

        Returns:
            The validated value if it is a DataFrame.

        Raises:
            ValueError: If the value is not a DataFrame.
        """
        if not isinstance(v, pd.DataFrame):
            raise ValueError("df must be a pandas DataFrame")
        return v

    def plot_correlation_heatmap(self, dtypes=['float64', 'int64'], colorscale='Inferno', title='Heatmap Correlation', width=1000, height=500):
        """
        Plots a correlation heatmap of the DataFrame.

        Args:
            dtypes (list): List of data types to include in the correlation matrix.
            colorscale (str): Colorscale to use for the heatmap.
            title (str): Title of the heatmap.
            width (int): Width of the heatmap.
            height (int): Height of the heatmap.
        """
        numeric_columns = self.df.select_dtypes(include=dtypes).columns

        df_corr = self.df[numeric_columns]
        correlation_matrix = df_corr.corr()
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
        correlation_matrix_masked = correlation_matrix.mask(mask)

        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix_masked.values,
            x=correlation_matrix_masked.columns,
            y=correlation_matrix_masked.columns,
            colorscale=colorscale,
            zmin=-1,
            zmax=1,
            text=correlation_matrix_masked.values,
            texttemplate="%{text:.2f}",
            hoverongaps=False
        ))

        fig.update_layout(
            title=title,
            xaxis_nticks=36,
            yaxis_autorange='reversed',
            template='plotly_white',
            width=width,
            height=height
        )

        fig.show()