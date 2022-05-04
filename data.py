import pandas as pd
import settings

class Data:

    def __get_merged_df(self) -> pd.DataFrame:
        """Creates a dataframe containing all data for the application, by merging data from different sources.

        Returns:
            pd.DataFrame: A dataframe containing all data for the application.
        """        

        # Create dataframes
        try: 
            df_covid = pd.read_csv(settings.covid_csv_url)
            df_party = pd.read_csv(settings.party_csv_url)
            df_population = pd.read_csv(settings.population_csv_url)
            df_vaccination = pd.read_csv(settings.vaccination_csv_url)
        except:
            print("There was an error retrieving the data. Please try again.")
            return

        # Make the state column name consistent.
        df_party["state"] = df_party["state_name"]
        df_vaccination["state"] = df_vaccination["name"]

        # Drop non-states from the vaccination data. (They're missing an ID—a state identifier.)
        df_vaccination.drop(df_vaccination[df_vaccination["id"].isna()].index, inplace=True)

        # Drop the population column from the vaccination data to avoid a conflict with the existing population data.
        df_vaccination.drop("population", axis=1, inplace=True)

        # Merge the datasets.    
        df_merged = pd.merge(df_covid, df_party, on="state")
        df_merged = pd.merge(df_merged, df_population, on="state")
        df_merged = pd.merge(df_merged, df_vaccination, on="state")

        # Create calculated columns
        df_merged["cases_per_thousand_people"] = round(df_merged["cases"]/(df_merged["population"]/1000), 2)
        df_merged["deaths_per_thousand_people"] = round(df_merged["deaths"]/(df_merged["population"]/1000), 2)
        df_merged["deaths_per_thousand_cases"] = round(df_merged["deaths"]/(df_merged["cases"]/1000), 2)
        df_merged["percent_unvaccinated"] = ((df_merged["population"] - df_merged["peopleVaccinated"]) / df_merged["population"]) * 100

        # Return the merged data, but only with the columns we'll actually use
        return df_merged[["state", "party", "cases", "deaths", "cases_per_thousand_people", "deaths_per_thousand_people", "deaths_per_thousand_cases", "percent_unvaccinated"]]

    def __init__(self):
        self.merged_df = self.__get_merged_df()