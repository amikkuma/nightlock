import logging
import matplotlib.pyplot as plt
import pandas as pd
import requests
import yaml
from typing import Optional
from kaggle.api.kaggle_api_extended import KaggleApi



class Analysis:
    """
    A class for analyzing COVID-19 data.

    Attributes:
    -----------
    config : dict
        The configuration dictionary loaded from YAML files.
    dataset : pandas.DataFrame
        The COVID-19 dataset loaded from the Kaggle URL.
    logger : logging.Logger
        The logger instance for logging messages.

    Methods:
    --------
    load_config(configs: str) -> dict:
        Loads configuration from YAML files.

    load_data():
        Retrieves data from the Kaggle COVID-19 dataset.

    compute_analysis() -> pd.DataFrame:
        Performs analysis on the loaded data.

    notify_done(message: str):
        Notifies the user that the analysis is complete.

    plot_data(save_path: Optional[str] = None) -> plt.Figure:
        Plots the data and saves the figure.
    """

    def __init__(self, analysis_config: str):
        """
        Initializes the Analysis object with the specified configuration.

        Parameters:
        -----------
        analysis_config : str
            The path to the YAML configuration file for the analysis.
        """

        CONFIG_PATHS = ['configs/system_config.yml', 'configs/user_config.yml']
        paths = CONFIG_PATHS + [analysis_config]
        logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='analysis.log',
                    filemode='w')
        self.logger = logging.getLogger("analysis.log")
        self.config = self.load_config(paths)
        self.dataset = None
        self.logger.info("Analysis object initialized with config: %s", self.config)

    def load_config(self, configs: str) -> dict:
        """
        Loads configuration from YAML files.

        Parameters:
        -----------
        configs : str
            A list of paths to YAML configuration files.

        Returns:
        --------
        dict
            The combined configuration dictionary.

        Raises:
        -------
        FileNotFoundError
            If a configuration file is not found.
        yaml.YAMLError
            If there is an error parsing a YAML file.
        """
        config = {}
        for config_file in configs:
            print(f"Processing config file {config_file}")
            try:
                with open(config_file, 'r') as stream:
                    self.logger.info("Loading configuration from file: %s", config_file)
                    config.update(yaml.safe_load(stream))
            except FileNotFoundError:
                self.logger.error("Configuration file not found: %s", config_file)
                raise
            except yaml.YAMLError as e:
                self.logger.error("Error parsing configuration file: %s", e)
                raise
        return config

    def load_data(self):
        """
        Retrieves data from the Kaggle COVID-19 dataset.

        Raises:
        -------
        ValueError
            If the Kaggle dataset URL is not provided in the configuration.
        requests.exceptions.HTTPError
            If there is an HTTP error while fetching the Kaggle dataset.
        Exception
            If there is an error loading the Kaggle dataset.
        """
        kaggle_dataset_path = self.config.get('kaggle_dataset_url', '')
        if not kaggle_dataset_path:
            self.logger.error("Kaggle dataset path not provided in the configuration")
            raise ValueError("Kaggle dataset path not provided in the configuration")
        
        try:
            # Initialize the Kaggle API client
            api = KaggleApi()
            api.authenticate()
            
            # Download the dataset to a temporary file
            api.dataset_download_files(kaggle_dataset_path, path='.', unzip=True)
            self.dataset = pd.read_csv('covid_19_data.csv')
            
            self.logger.info("Data loaded successfully with %d rows", len(self.dataset))
        except Exception as e:
            self.logger.error("Error loading Kaggle dataset: %s", e)
            raise

    def compute_analysis(self) -> pd.DataFrame:
        """
        Performs analysis on the loaded data.

        Returns:
        --------
        pandas.DataFrame
            The result of the analysis.

        Raises:
        -------
        ValueError
            If no data is loaded for analysis.
        """
        if self.dataset is None:
            self.logger.error("No data loaded for analysis")
            raise ValueError("No data loaded for analysis")
        
        self.logger.info("Performing analysis on dataset")
        analysis_output = self.dataset.groupby('Country/Region')[['Confirmed', 'Deaths']].sum().reset_index()
        return analysis_output

    def notify_done(self, message: str):
        """
        Notifies the user that the analysis is complete.

        Parameters:
        -----------
        message : str
            The message to send to the notification service.

        Raises:
        -------
        requests.exceptions.RequestException
            If there is an error sending the notification.
        """
        try:
            ntfy_topic = self.config.get('ntfy_topic')
            self.logger.info("Sending notification to ntfy.sh topic: %s", ntfy_topic)
            response = requests.post(f"https://ntfy.sh/{ntfy_topic}", data=message.encode(encoding='utf-8'))
            response.raise_for_status()
            self.logger.info("Notification sent successfully")
        except requests.exceptions.RequestException as e:
            self.logger.error("Failed to send notification: %s", e)
            raise

    def plot_data(self, save_path: Optional[str] = None) -> plt.Figure:
        """
        Plots the data and saves the figure.

        Parameters:
        -----------
        save_path : str, optional
            The path to save the plot figure. If not provided, a default path is used.

        Returns:
        --------
        matplotlib.figure.Figure
            The figure containing the plot.

        Raises:
        -------
        ValueError
            If no data is available to plot.
        """
        if self.dataset is None:
            self.logger.error("No data to plot")
            raise ValueError("No data to plot")
        
        country = self.config.get('plot_country', 'Canada')
        country_data = self.dataset[self.dataset['Country/Region'] == country]
        
        plt.figure(figsize=self.config.get('figure_size', (8, 6)))
        plt.plot(country_data['Confirmed'], country_data['Deaths'], color=self.config.get('plot_color', 'blue'))
        plt.title(f"COVID-19 Cases in {country}")
        plt.xlabel(self.config.get('plot_xlabel', 'Confirmed Cases'))
        plt.ylabel(self.config.get('plot_ylabel', 'Deaths'))
        if save_path is None:
            save_path = self.config.get('default_save_path', 'plots/') + f'covid_cases_{country}.png'
        plt.savefig(save_path)
        self.logger.info("Plot saved to: %s", save_path)
        plt.show()
        return plt.gcf()

# Usage example
if __name__ == "__main__":
    # Initialize Analysis object
    analysis_obj = Analysis('configs/job_file.yml')

    # Load data
    analysis_obj.load_data()

    # Perform analysis
    analysis_output = analysis_obj.compute_analysis()
    print("Analysis output:", analysis_output)

    # Notify user
    analysis_obj.notify_done("Analysis is complete!")

    # Plot data
    analysis_figure = analysis_obj.plot_data()
