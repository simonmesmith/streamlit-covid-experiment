import string
import pandas as pd
import requests
import settings
from bs4 import BeautifulSoup

class Data:

    def __merge_dfs(self, *dfs: pd.DataFrame, on: str) -> pd.DataFrame:
        """Merges provided dataframes.

        Args:
            self: The class instance.
            *dfs: A list of dataframes to merge.
            on (str): The column to merge on (same as for pandas.DataFrame.merge)

        Returns:
            pd.DataFrame: A single dataframe consolidating data from the provided dataframes.
        """

        for i, df in enumerate(dfs):
            if i == 0:
                df_merged = df
            else:
                df_merged = pd.merge(df_merged, df, on=on)
        return df_merged

    def __get_temperature_df(self) -> pd.DataFrame:
        """Gets temperature data for charts in a dataframe.

        Returns:
            pd.DataFrame: A dataframe containing temperature data.
        """        
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"
        }
        req = requests.get(settings.average_temperature_url, headers)
        soup = BeautifulSoup(req.content, "html.parser")
        tables = soup.find_all("table")
        dfs = pd.read_html(str(tables))
        df = pd.concat(dfs)
        df.rename(columns={"State": "state", "Avg °F": "average_fahrenheit"}, inplace=True)
        return df

    def __get_merged_df(self) -> pd.DataFrame:
        """Creates a dataframe containing all data for the application, by merging data from different sources.

        Args:
            self: The class instance.

        Returns:
            pd.DataFrame: A dataframe containing all data for the application.
        """        

        # Create dataframes
        try: 
            df_covid = pd.read_csv(settings.covid_csv_url)
            df_party = pd.read_csv(settings.party_csv_url)
            df_population = pd.read_csv(settings.population_csv_url)
            df_vaccination = pd.read_csv(settings.vaccination_csv_url)
            df_temperature = self.__get_temperature_df()
        except:
            print("There was an error retrieving the data. Please try again.")
            return

        # Make the state column name consistent.
        df_party["state"] = df_party["state_name"]
        df_vaccination["state"] = df_vaccination["name"]

        # Drop non-states from the vaccination data. (We can find them because they're missing an ID value.)
        df_vaccination.drop(df_vaccination[df_vaccination["id"].isna()].index, inplace=True)

        # Drop the population column from the vaccination data to avoid a conflict with the existing population data in df_population.
        df_vaccination.drop("population", axis=1, inplace=True)

        # Merge the datasets.
        df_merged = self.__merge_dfs(df_covid, df_party, df_population, df_vaccination, df_temperature, on="state")

        # Create calculated columns
        df_merged["cases_per_thousand_people"] = round(df_merged["cases"]/(df_merged["population"]/1000), 2)
        df_merged["deaths_per_thousand_people"] = round(df_merged["deaths"]/(df_merged["population"]/1000), 2)
        df_merged["deaths_per_thousand_cases"] = round(df_merged["deaths"]/(df_merged["cases"]/1000), 2)
        df_merged["percent_unvaccinated"] = round(((df_merged["population"] - df_merged["peopleVaccinated"]) / df_merged["population"]) * 100, 2)

        # Return the merged data, but only with the columns we'll actually use
        return df_merged[["state", "party", "cases", "deaths", "average_fahrenheit", "cases_per_thousand_people", "deaths_per_thousand_people", "deaths_per_thousand_cases", "percent_unvaccinated"]]

    def __init__(self):
        self.merged_df = self.__get_merged_df()