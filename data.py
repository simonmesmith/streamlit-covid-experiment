import pandas as pd
import settings

class Data:

    def __get_merged_df(self) -> pd.DataFrame:

        # Create dataframes
        try: 
            df_covid = pd.read_csv(settings.covid_csv_url)
            df_party = pd.read_csv(settings.party_csv_url)
            df_population = pd.read_csv(settings.population_csv_url)
        except:
            print("There was an error retrieving the data. Please try again.")
            return

        # Merge dataframes (have to make the state column name consistent first in the party dataframe)
        # TODO: See if it's possible to merge all the dataframes in one line versus the current two. 
        df_party["state"] = df_party["state_name"]
        df_merged = pd.merge(df_covid, df_party, on="state")
        df_merged = pd.merge(df_merged, df_population, on="state")

        # Create calculated columns
        df_merged["cases_per_thousand_people"] = round(df_merged["cases"]/(df_merged["population"]/1000), 2)
        df_merged["deaths_per_thousand_people"] = round(df_merged["deaths"]/(df_merged["population"]/1000), 2)
        df_merged["deaths_per_thousand_cases"] = round(df_merged["deaths"]/(df_merged["cases"]/1000), 2)

        # Return the merged data, but only with the columns we'll actually use
        return df_merged[["state", "party", "cases", "deaths", "cases_per_thousand_people", "deaths_per_thousand_people", "deaths_per_thousand_cases"]]

    def __format_state_chart_df(self, column: str) -> pd.DataFrame:
        return self.merged_df[["state", column]].sort_values(by=column, ascending=False)

    def __init__(self):
        self.merged_df = self.__get_merged_df()
        self.state_count = len(self.merged_df['state'].unique())
        self.cases_per_thousand_people_df = self.__format_state_chart_df("cases_per_thousand_people")
        self.deaths_per_thousand_people_df = self.__format_state_chart_df("deaths_per_thousand_people")
        self.deaths_per_thousand_cases_df = self.__format_state_chart_df("deaths_per_thousand_cases")
        self.cases_per_thousand_people_best_state = self.cases_per_thousand_people_df.iloc[-1]["state"]
        self.cases_per_thousand_people_worst_state = self.cases_per_thousand_people_df.iloc[0]["state"]
        self.deaths_per_thousand_people_best_state = self.deaths_per_thousand_people_df.iloc[-1]["state"]
        self.deaths_per_thousand_people_worst_state = self.deaths_per_thousand_people_df.iloc[0]["state"]
        self.deaths_per_thousand_cases_best_state = self.deaths_per_thousand_cases_df.iloc[-1]["state"]
        self.deaths_per_thousand_cases_worst_state = self.deaths_per_thousand_cases_df.iloc[0]["state"]