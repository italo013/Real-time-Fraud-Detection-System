from typing import Optional
import pandas as pd
from pydantic import BaseModel, field_validator
from IPython.display import Markdown, display


class DataUnderstanding(BaseModel):
    """
    Class to understand and analyze a pandas DataFrame.

    Attributes:
        df (pd.DataFrame): The DataFrame to be analyzed.
        metadata (Optional[pd.DataFrame]): Metadata generated from the DataFrame.
        metadata_dtype (Optional[pd.DataFrame]): Metadata about the data types in the DataFrame.
    """

    df: pd.DataFrame
    metadata: Optional[pd.DataFrame] = None
    metadata_dtype: Optional[pd.DataFrame] = None

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

    def generate_metadata(self):
        """
        Generates metadata from the DataFrame and stores it in the metadata and metadata_dtype attributes.
        """
        df_info = pd.DataFrame(
            {
                "Not Null": self.df.notnull().sum(),
                "Null": self.df.isnull().sum(),
                "Perce Null": self.df.isnull().sum() / len(self.df),
                "Dtype": self.df.dtypes,
                "Cardinality": self.df.nunique(),
            }
        )

        df_dtype = pd.DataFrame(self.df.dtypes.value_counts()).reset_index()
        df_dtype.columns = ["Dtype", "Count"]
        df_dtype["Percentage"] = round(df_dtype["Count"] / df_dtype["Count"].sum(), 2)

        self.metadata = df_info
        self.metadata_dtype = df_dtype

        self.display_metadata()

    def display_metadata(self):
        """
        Displays the generated metadata in a stylized manner using IPython.display.
        """
        text = f"The dataset has {self.df.shape[0]} rows and {self.df.shape[1]} columns. Of these, we have:"

        df_info_styled = self.metadata.style.background_gradient(
            cmap="jet", subset=["Perce Null"]
        ).format({"Perce Null": "{:.2%}"})

        df_dtype_styled = self.metadata_dtype.style.background_gradient(
            cmap="YlGn", subset=["Percentage"]
        ).format({"Percentage": "{:.2%}"})

        display(
            Markdown("<H3 style='text-align:left;float:left;'>Dataset Information</H3>")
        )
        display(Markdown(f"<H5>{text}</H5>"))
        display(df_info_styled)
        display(
            Markdown(
                "<H3 style='text-align:left;float:left;'>Data Types Information:</H3>"
            )
        )
        display(df_dtype_styled)
