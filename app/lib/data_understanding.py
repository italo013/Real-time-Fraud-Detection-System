import pandas as pd
from IPython.display import Markdown, display


class DataUnderstanding:
    """
    Classe para entender os dados de um DataFrame pandas.

    Atributos
    ----------
    df : pandas.DataFrame
        DataFrame original.
    metadata : pandas.DataFrame, opcional
        DataFrame contendo metadados gerados a partir do DataFrame original.
    metadata_dtype : pandas.DataFrame, opcional
        DataFrame contendo metadados sobre os tipos de dados no DataFrame original.

    Métodos
    -------
    generate_metadata():
        Gera metadados a partir do DataFrame original.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        metadata: pd.DataFrame = None,
        metadata_dtype: pd.DataFrame = None,
    ):
        """
        Construtor da classe DataUnderstanding.

        Parâmetros
        ----------
        df : pandas.DataFrame
            DataFrame original.
        metadata : pandas.DataFrame, opcional
            DataFrame contendo metadados gerados a partir do DataFrame original.
        metadata_dtype : pandas.DataFrame, opcional
            DataFrame contendo metadados sobre os tipos de dados no DataFrame original.
        """
        self.df = df
        self.metadata = metadata
        self.metadata_dtype = metadata_dtype

    def generate_metadata(self):
        """
        Gera metadados a partir do DataFrame original.

        Este método calcula várias estatísticas sobre o DataFrame original, incluindo a contagem de valores não nulos,
        a contagem de valores nulos, a porcentagem de valores nulos, o tipo de dados e a cardinalidade de cada coluna.
        Ele também gera um resumo dos tipos de dados presentes no DataFrame.

        Os metadados gerados são armazenados nos atributos 'metadata' e 'metadata_dtype' da classe.
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

        df_dtype = pd.DataFrame(self.df.dtypes.value_counts())
        df_dtype.columns = ["Contagem"]
        df_dtype["Percentual"] = round(
            df_dtype["Contagem"] / df_dtype["Contagem"].sum(), 2
        )

        self.metadata = df_info
        self.metadata_dtype = df_dtype

        texto = f"O dataset possui {self.df.shape[0]} linhas e {self.df.shape[1]} colunas. Dessas, temos:"

        df_info = df_info.style.background_gradient(
            cmap="jet", subset=["Perce Null"]
        ).format({"Perce Null": "{:.2%}"})
        df_dtype = df_dtype.style.background_gradient(
            cmap="YlGn", subset=["Percentual"]
        ).format({"Percentual": "{:.2%}"})

        display(
            Markdown(
                "<H3 style='text-align:left;float:left;'>Informações sobre o Dataset</H3>"
            )
        )
        display(Markdown(f"<H5>{texto}</H5>"))
        display(df_info)
        display(
            Markdown(
                "<H3 style='text-align:left;float:left;'>Informações sobre os Tipos de Dados:</H3>"
            )
        )
        display(df_dtype)