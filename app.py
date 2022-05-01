import altair as alt
import data
import streamlit as st

d = data.Data()

st.title("US COVID Data Analysis")

# TODO: Programmatically create the user interface elements with a for loop or function, since they all follow the same format.

# --------------------------------
# Cases per thousand people 
# --------------------------------
st.header("Cases per thousand people")
st.write(f"The worst state for cases per thousand people is {d.cases_per_thousand_people_worst_state}. The best state is {d.cases_per_thousand_people_best_state}.")
cases_per_thousand_people_slider = st.slider("See more states", min_value=1, max_value=d.state_count, value=10, key="cases_per_thousand_people_slider")
cases_per_thousand_people_chart = alt.Chart(d.cases_per_thousand_people_df[:cases_per_thousand_people_slider]).mark_bar().encode(    
    x=alt.X("cases_per_thousand_people", title="Cases per thousand people"),
    y=alt.Y("state", sort=["cases_per_thousand_people"], title="State"),
    )
st.altair_chart(cases_per_thousand_people_chart, use_container_width=True)

st.subheader("Cases per thousand people by party")
st.write("Which party did worse at minimizing the cases per thousand people?")
cases_per_thousand_people_by_party_chart = alt.Chart(d.merged_df).mark_bar().encode(    
    x=alt.X("mean(cases_per_thousand_people)", title="Mean cases per thousand people"),
    y=alt.Y("party", sort=["mean(cases_per_thousand_people)"], title="Party"),
    )
st.altair_chart(cases_per_thousand_people_by_party_chart, use_container_width=True)

# --------------------------------
# Deaths per thousand people
# --------------------------------
st.header("Deaths per thousand people")
st.write(f"The worst state for deaths per thousand people is {d.deaths_per_thousand_people_worst_state}. The best state is {d.deaths_per_thousand_people_best_state}.")
deaths_per_thousand_people_slider = st.slider("See more states", min_value=1, max_value=d.state_count, value=10, key="deaths_per_thousand_people_slider")
deaths_per_thousand_people_chart = alt.Chart(d.deaths_per_thousand_people_df[:deaths_per_thousand_people_slider]).mark_bar().encode(    
    x=alt.X("deaths_per_thousand_people", title="Cases per thousand people"),
    y=alt.Y("state", sort=["deaths_per_thousand_people"], title="State"),
    )
st.altair_chart(deaths_per_thousand_people_chart, use_container_width=True)

st.subheader("Deaths per thousand people by party")
st.write("Which party did worse at minimizing the deaths per thousand people?")
deaths_per_thousand_people_by_party_chart = alt.Chart(d.merged_df).mark_bar().encode(    
    x=alt.X("mean(deaths_per_thousand_people)", title="Mean deaths per thousand people"),
    y=alt.Y("party", sort=["mean(deaths_per_thousand_people)"], title="Party"),
    )
st.altair_chart(deaths_per_thousand_people_by_party_chart, use_container_width=True)

# --------------------------------
# Deaths per thousand cases
# --------------------------------
st.header("Deaths per thousand cases")
st.write(f"The worst state for deaths per thousand cases is {d.deaths_per_thousand_cases_worst_state}. The best state is {d.deaths_per_thousand_cases_best_state}.")
deaths_per_thousand_cases_slider = st.slider("See more states", min_value=1, max_value=d.state_count, value=10, key="deaths_per_thousand_cases_slider")
deaths_per_thousand_cases_chart = alt.Chart(d.deaths_per_thousand_cases_df[:deaths_per_thousand_cases_slider]).mark_bar().encode(    
    x=alt.X("deaths_per_thousand_cases", title="Cases per thousand cases"),
    y=alt.Y("state", sort=["deaths_per_thousand_cases"], title="State"),
    )
st.altair_chart(deaths_per_thousand_cases_chart, use_container_width=True)

st.subheader("Deaths per thousand cases by party")
st.write("Which party did worse at minimizing the deaths per thousand cases?")
deaths_per_thousand_cases_by_party_chart = alt.Chart(d.merged_df).mark_bar().encode(    
    x=alt.X("mean(deaths_per_thousand_cases)", title="Mean deaths per thousand cases"),
    y=alt.Y("party", sort=["mean(deaths_per_thousand_cases)"], title="Party"),
    )
st.altair_chart(deaths_per_thousand_cases_by_party_chart, use_container_width=True)