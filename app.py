import altair as alt
import data
import streamlit as st

d = data.Data()

st.title("US COVID Data Analysis")

# List of state sections to create
state_sections = [
    "Cases per thousand people",
    "Deaths per thousand people",
    "Deaths per thousand cases",
    "Percent unvaccinated"
]

# Loop through each state section and write out the user interface
for section in state_sections:

    # Use the section name as the basis to create the column name and then get appropriate data
    column = section.lower().replace(" ", "_")
    df = d.merged_df[["state", column]].sort_values(by=column, ascending=False)
    total_states = len(df['state'].unique())
    best_state = df.iloc[-1]["state"]
    worst_state = df.iloc[0]["state"]

    # Create the header and introductory sentence
    st.header(section)
    st.write(f"The worst state for {section.lower()} is {worst_state}. The best state is {best_state}.")

    # Create the main the chart with a slider that lets users specify how many states to show
    states_to_show = st.slider("See more states", min_value=1, max_value=total_states, value=10, key=column)
    chart = alt.Chart(df[:states_to_show]).mark_bar().encode(    
        x=alt.X(column, title=section),
        y=alt.Y("state", sort=[column], title="State"),
        tooltip=[alt.Tooltip(field=column, title=section)]
    )
    st.altair_chart(chart, use_container_width=True)

    # Create the party subsection
    st.subheader(f"{section} by party")
    st.write(f"Which party did worse at minimizing the {section.lower()}?")
    chart = alt.Chart(d.merged_df).mark_bar().encode(    
        x=alt.X(f"mean({column})", title=f"Mean {section.lower()}"),
        y=alt.Y("party", sort=[f"mean({column})"], title="Party"),
        tooltip=[alt.Tooltip(field=column, title=section)]
        )
    st.altair_chart(chart, use_container_width=True)

# Create the temperature analysis chart
st.header("Temperature and COVID")
st.write("This chart shows the relationship between a state's average temperature (in Fahrenheit) and COVID.")
temperature_chart = alt.Chart(d.merged_df).mark_circle().encode(
     x=alt.X("average_fahrenheit", title="Average Fahrenheit"),
     y=alt.Y("cases_per_thousand_people", title="Cases per thousand people"), 
     size="deaths_per_thousand_cases", 
     color="state", 
     tooltip=[
         alt.Tooltip("state", title="State"),
         alt.Tooltip("average_fahrenheit", title="Average Fahrenheit"), 
         alt.Tooltip("cases_per_thousand_people", title="Cases per thousand people"), 
         alt.Tooltip("deaths_per_thousand_cases", title="Deaths per thousand cases")
    ])
st.altair_chart(temperature_chart, use_container_width=True)
