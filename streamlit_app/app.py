import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np

### Config
st.set_page_config(
    page_title="Delay management dashbord",
    page_icon=" ",
    layout="wide"
)

DATA_PATH = ('get_around_delay_analysis.xlsx')

### App
st.title("Delay management dashbord")
st.markdown("""
    The objective of this dashboard is to perform some analysis about the rentals returned late like:
    - How often are drivers late for the next check-in? How does it impact the next driver?
    - How is the delay repartition between the different check-in type?
    And explore the possibility of a new feature, a threshold between the location to avoid late rentals, answering questions like:
    - Which share of our owner’s revenue would potentially be affected by the feature? How many rentals would be affected by the feature depending on the threshold and scope we choose?
    - How long should the minimum delay be?
    - should we enable the feature for all cars?, only Connect cars?
    - How many problematic cases will it solve depending on the chosen threshold and scope?

""")
st.markdown("""
    ------------------------
""")

# Use `st.cache` when loading data is extremly useful
# because it will cache your data so that your app 
# won't have to reload it each time you refresh your app
@st.cache
def load_data():
    data = pd.read_excel(DATA_PATH,index_col=None)
    return data


st.subheader("Load and showcase data")


data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Data loaded")

## Run the below code if the check is checked ✅
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)    

st.markdown("""
    ------------------------
""")
st.subheader("Late rental analysis")
st.markdown("""
    Here we are going to explore the proportion of late rentals, the repartition, and the possible impact:
""")

st.markdown("""
    

""")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""Global late proportion""")

    df_delay = data.copy()
    mask = df_delay['delay_at_checkout_in_minutes'] > 0
    df_delay['checkout_status'] = ["Late" if x>0 else "in_time" for x in df_delay['delay_at_checkout_in_minutes']] 
    fig_late_proportion = px.pie(df_delay, names='checkout_status')
    fig_late_proportion.update_layout(title_text='Proportion of late checkout',title_y=0.5)
    st.plotly_chart(fig_late_proportion, use_container_width=True)


with col2:
    st.markdown("""Late rental chekout analysis by check-in type""")
    df_delay['delay_repartition'] = 'In time'
    df_delay.loc[((df_delay['checkin_type'] == 'mobile') & (df_delay['checkout_status'] == 'Late')),'delay_repartition'] = 'Mobile and late'
    df_delay.loc[((df_delay['checkin_type'] == 'connect') & (df_delay['checkout_status'] == 'Late')),'delay_repartition'] = 'Connect and late'
    fig_late_repartition = px.pie(df_delay, names='delay_repartition', title='Proportion of late checkout', width= 700)
    fig_late_repartition.update_layout(title_text='Proportion of late checkout by check-in type',title_y=0.95,title_x=0.5)
    st.plotly_chart(fig_late_repartition, use_container_width=True)


with col3:
    st.markdown("""Additional data analysis""")
    st.markdown("""                     """)
    st.markdown("""
It seems that there is way more late rental in proportion when the check-in type is mobile, but it might be that there is juste more mobile check-in, 
how is it when we look at the percentage:
""")
    Late_perc_mobile = len(df_delay.loc[((df_delay['checkin_type'] == 'mobile') & (df_delay['checkout_status'] == 'Late')),:])/len(df_delay.loc[(df_delay['checkin_type'] == 'mobile'),:])*100
    Late_perc_connect = len(df_delay.loc[((df_delay['checkin_type'] == 'connect') & (df_delay['checkout_status'] == 'Late')),:])/len(df_delay.loc[(df_delay['checkin_type'] == 'connect'),:])*100
    st.metric("Percentage of late rental for the check in by connect:", round(Late_perc_connect,2))
    st.metric("Percentage of late rental for the check in by mobile:", round(Late_perc_mobile,2))

    st.markdown("""
As we can see the mobile type of check in also got an higher proportion of late checkout of 13%, to finaly help decide if there is a need to add a threshold only for 
one type of check-in type (like the connect) we can check the average delay time by check-in type:
""")

    mask2 = (df_delay['delay_at_checkout_in_minutes'] > 0) & (df_delay['checkin_type'] == 'mobile')
    average_delay_mobile = (df_delay.loc[mask2, 'delay_at_checkout_in_minutes']).mean()
    st.metric("Average delay time by mobile check-in (when late) :", round(average_delay_mobile,2))

    mask3 = (df_delay['delay_at_checkout_in_minutes'] > 0) & (df_delay['checkin_type'] == 'connect')
    average_delay_connect = (df_delay.loc[mask3, 'delay_at_checkout_in_minutes']).mean()
    st.metric("Average delay time by connect check-in (when late) :", round(average_delay_connect,2))


st.markdown("""
Considering this data it could be intresting for the  product Management team to consider creating a threshold concerning at least the people that check-in 
by mobile.



""")
st.markdown("""
    ------------------------
""")

st.subheader("Late rental chekout impact analysis")
st.markdown("""
The objective of this part is to help the product management team to have a better understanding on how this delay checkout can impact other rental
""")

col1, col2 = st.columns(2)
#Construction of a dataset matching the rented car with the previous rental
df_loc_consecutive = pd.merge(df_delay, df_delay, how='inner', left_on = 'previous_ended_rental_id', right_on = 'rental_id')


df_loc_consecutive.drop(
    [
        "delay_at_checkout_in_minutes_x",
        "rental_id_y", 
        "car_id_y", 
        "state_y",
        "time_delta_with_previous_rental_in_minutes_y",
        "previous_ended_rental_id_y",
        "checkout_status_x"
    ], 
    axis=1,
    inplace=True
)

df_loc_consecutive = df_loc_consecutive.rename(columns={
    'rental_id_x' : 'rental_id',
    'car_id_x': 'car_id',
    'checkin_type_x':'checkin_type',
    'state_x':'state',
    'previous_ended_rental_id_x':'previous_ended_rental_id',
    'time_delta_with_previous_rental_in_minutes_x':'time_delta_with_previous_rental_in_minutes',
    'checkin_type_y':'previous_checkin_type',
    'delay_at_checkout_in_minutes_y':'previous_delay_at_checkout_in_minutes',
    'checkout_status_y':'previous_checkout_status'
})
#Drop the rows with missing values
mask4 = df_loc_consecutive["previous_delay_at_checkout_in_minutes"].notnull() 
df_loc_consecutive = df_loc_consecutive.loc[mask4, :]
df_loc_consecutive.reset_index(drop=True, inplace=True)
#Calculation of the real delay between the locations taking into account rentals returned late
df_loc_consecutive['real_delay_between_loc_in_min'] = df_loc_consecutive['time_delta_with_previous_rental_in_minutes'] - df_loc_consecutive['previous_delay_at_checkout_in_minutes']
df_loc_consecutive.sort_values(by = 'real_delay_between_loc_in_min')

#Impacted location, when the late returned is superior to the time planned between the two rentals 
df_impacted_loc = df_loc_consecutive.loc[df_loc_consecutive['real_delay_between_loc_in_min'] < 0, :]
#Impacted location that have been canceled
df_impacted_canceled_loc = df_impacted_loc.loc[df_impacted_loc['state'] == 'canceled',:]
#Location non impacted by a late return
df_non_impacted_loc = df_loc_consecutive.loc[df_loc_consecutive['real_delay_between_loc_in_min'] >= 0, :]
#Total number of canceled location
total_cancel = len(df_loc_consecutive.loc[(df_loc_consecutive['state'] == 'canceled')])
#Number of rental cancel that have not been impacted by late return
no_late_cancel = len(df_non_impacted_loc.loc[(df_non_impacted_loc['state'] == 'canceled')])


df_impacted_loc['previous_ended_rental_id'] = df_impacted_loc['previous_ended_rental_id'].apply(lambda x: int(x))

with col1:
    for elt in df_delay['rental_id']:
        if elt in (df_impacted_loc['previous_ended_rental_id'].values):
            df_delay.loc[elt,'checkout_status'] = 'late and impacting'

    fig_late_impact = px.pie(df_delay, names='checkout_status', title='Proportion of late checkout', width = 700)
    fig_late_impact.update_layout(title_text='Proportion of late checkout',title_y=0.95,title_x=0.5)
    st.plotly_chart(fig_late_impact, use_container_width=True)

with col2:
    st.markdown("""

""")
    st.markdown("""
Some numbers resultings from the analysis:
""")
    st.metric("Number of impacted location :", len(df_impacted_loc))
    st.metric('Number of canceled rentals with a delay:',len(df_impacted_canceled_loc))
    st.metric("Percentage of cancellations without apparent reasons (in non impacted locations):",round((no_late_cancel/len(df_non_impacted_loc) *100),2))
    st.metric("Percentage of rental canceled due to delay (in the impacted locations): ",round((len(df_impacted_canceled_loc)/len(df_impacted_loc)*100),2))
    st.markdown("We notice a higher percentage of canceled rentals when the delay of a rental impacts the next rental")
    st.markdown("We can estimate the percentage of rentals canceled (with every location comprised impacted and non impacted) due to this delay at: ")
    st.metric('',round(((len(df_impacted_canceled_loc)- (len(df_impacted_canceled_loc)*11/100))/len(df_delay)*100),2))
    st.markdown("(Number of rentals impacted and canceled minus the 11% which are representative of rentals canceled without reason)")

st.markdown("The number of location impacted by late rental is quite small and can question the necessity of a threshold, we will study further the threshold management in the next part")
    

st.markdown("""
    ------------------------
""")

st.subheader("Threshold management")

st.markdown("""
The problem is difficult to approach, as a threshold would indeed prevent the late location to impact others, but
it would also make every cars (including those who would not impacted by a late rental) unavaible for an extra period of time, and therefore losing potential client and profit.

Therefore we need to find a good balance in order to avoid a maximum of the friction but also having the smaller threshold possible to avoid making the cars unavaible for too long.
""")

st.markdown("""
Delay repartition preview:
""")
df_impacted_canceled_loc = df_impacted_canceled_loc.reset_index()
df_impacted_canceled_loc = df_impacted_canceled_loc.drop('index', axis = 1)

fig_late_preview = px.bar(df_impacted_canceled_loc, x= 'real_delay_between_loc_in_min', y = df_impacted_canceled_loc.index )
st.plotly_chart(fig_late_preview, use_container_width=True)

st.markdown("""
With this preview we can already identity that a threshold around 200 minutes could be intresting to avoid a majority of the late rental. 

Now let's look at how a threshold would impact the location (late rental avoided and location missed), based on the precedent analysis we are only looking at the 
location done by mobile check-in:
""")

def threshold_result(max_threshold):
    late_avoided = []
    location_missed = []
    for threshold in range(0,max_threshold):
        df_loc_consecutive_threshold = df_loc_consecutive.loc[df_loc_consecutive['previous_checkin_type'] == 'mobile', : ]
        df_loc_consecutive_threshold['time_delta_with_previous_rental_in_minutes'] = df_loc_consecutive_threshold['time_delta_with_previous_rental_in_minutes'].apply(lambda x: threshold if x < threshold else x )
        df_loc_consecutive_threshold['real_delay_between_loc_in_min'] = df_loc_consecutive_threshold['time_delta_with_previous_rental_in_minutes'] - df_loc_consecutive_threshold['previous_delay_at_checkout_in_minutes']
        df_impacted_loc_theshold = df_loc_consecutive_threshold.loc[df_loc_consecutive_threshold['real_delay_between_loc_in_min'] < 0, :]
        late_avoided.append(len(df_impacted_loc) - len(df_impacted_loc_theshold))
        location_missed.append(len(df_loc_consecutive) - len(df_loc_consecutive.loc[df_loc_consecutive['time_delta_with_previous_rental_in_minutes'] > threshold,:]))
    fig_threshold = px.line(x = [i for i in range(0,max_threshold)], y = [late_avoided,location_missed] )
    legend_names = {'wide_variable_0':'Late location avoided', 'wide_variable_1': 'Location missed'}
    fig_threshold.for_each_trace(lambda t: t.update(name = legend_names[t.name],
                                      legendgroup = legend_names[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, legend_names[t.name])
                                     ))
    fig_threshold.update_layout(
    height=700, 
    xaxis_title = 'Threshold value',
    title={
        'text': 'Threshold impact',
        'y':0.98,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
)
    st.plotly_chart(fig_threshold, use_container_width=True)


with st.form("Threshold results preview"):
    number = st.number_input('Insert a threshold number', min_value=0, step=1)
    submit = st.form_submit_button("submit")
    if submit:
        threshold_result(number)


st.markdown("""
As we can see on the graph (when we set a high threshold number like 500 to get an overview) and as we could see on the preview most of the delay can be avoid with a threshold around 200 minutes,
after this the increase in the late location avoided become very slow, while the possible missed location due to the increase of time (and therefore indisponibility between two location) keep increasing.

Considering that even with a threshold around 200 the missed location is significatively higher (906) than the late location avoided (180) the necessity of a threshold can be discussed.
The management team must determined if the frictions (and their consequences) caused by the delay are more important than the high number of missed location induce by a threshold.
""")

st.sidebar.header("Rental delay management dashboard")
st.sidebar.markdown("""
    * [Load and showcase data](#load-and-showcase-data)
    * [Late rental analysis](#late-rental-analysis)
    * [Late rental chekout impact analysis](#late-rental-chekout-impact-analysis)
    * [Threshold management](#threshold-management)
""")
e = st.sidebar.empty()
e.write("")