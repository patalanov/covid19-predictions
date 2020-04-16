# big data
import COVID19Py
# python libraries
from datetime import datetime, timedelta
import json
import itertools
import time
# data tools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import seaborn as sns
import pycountry
from PIL import Image
from IPython.display import HTML as html_print
# machine learning libraries
from sklearn.metrics import mean_squared_error
from scipy.optimize import curve_fit
from scipy.optimize import fsolve
# app
import streamlit as st


# all countries, and alpha 2 code for api query (global locations need alpha 3)
countries_and_codes = [
   ['Afghanistan', 'AF'], ['Albania', 'AL'], ['Algeria', 'DZ'], ['Andorra', 'AD'], ['Angola', 'AO'], 
   ['Antigua and Barbuda', 'AG'], ['Argentina', 'AR'], ['Armenia', 'AM'], ['Australia', 'AU'], ['Austria', 'AT'], 
   ['Azerbaijan', 'AZ'], ['Bahamas', 'BS'], ['Bahrain', 'BH'], ['Bangladesh', 'BD'], ['Barbados', 'BB'], 
   ['Belarus', 'BY'], ['Belgium', 'BE'], ['Belize', 'BZ'], ['Benin', 'BJ'], ['Bhutan', 'BT'], ['Bolivia', 'BO'], 
   ['Bosnia and Herzegovina', 'BA'], ['Botswana', 'BW'], ['Brazil', 'BR'], ['Brunei', 'BN'], ['Bulgaria', 'BG'], 
   ['Burkina Faso', 'BF'], ['Burma', 'MM'], ['Burundi', 'BI'], ['Cabo Verde', 'CV'], ['Cambodia', 'KH'], 
   ['Cameroon', 'CM'], ['Canada', 'CA'], ['Central African Republic', 'CF'], ['Chad', 'TD'], ['Chile', 'CL'], 
   ['China', 'CN'], ['Colombia', 'CO'], ['Congo (Brazzaville)', 'CG'], ['Congo (Kinshasa)', 'CD'], 
   ['Costa Rica', 'CR'], ["Cote d'Ivoire", 'CI'], ['Croatia', 'HR'], ['Cuba', 'CU'], ['Cyprus', 'CY'], 
   ['Czechia', 'CZ'], ['Denmark', 'DK'], ['Diamond Princess', 'XX'], ['Djibouti', 'DJ'], ['Dominica', 'DM'], 
   ['Dominican Republic', 'DO'], ['Ecuador', 'EC'], ['Egypt', 'EG'], ['El Salvador', 'SV'], 
   ['Equatorial Guinea', 'GQ'], ['Eritrea', 'ER'], ['Estonia', 'EE'], ['Eswatini', 'SZ'], ['Ethiopia', 'ET'], 
   ['Fiji', 'FJ'], ['Finland', 'FI'], ['France', 'FR'], ['Gabon', 'GA'], ['Gambia', 'GM'], ['Georgia', 'GE'], 
   ['Germany', 'DE'], ['Ghana', 'GH'], ['Greece', 'GR'], ['Grenada', 'GD'], ['Guatemala', 'GT'], ['Guinea', 'GN'], 
   ['Guinea-Bissau', 'GW'], ['Guyana', 'GY'], ['Haiti', 'HT'], ['Holy See', 'VA'], ['Honduras', 'HN'], 
   ['Hungary', 'HU'], ['Iceland', 'IS'], ['India', 'IN'], ['Indonesia', 'ID'], ['Iran', 'IR'], ['Iraq', 'IQ'], 
   ['Ireland', 'IE'], ['Israel', 'IL'], ['Italy', 'IT'], ['Jamaica', 'JM'], ['Japan', 'JP'], ['Jordan', 'JO'], 
   ['Kazakhstan', 'KZ'], ['Kenya', 'KE'], ['Korea, South', 'KR'], ['Kosovo', 'XK'], ['Kuwait', 'KW'], 
   ['Kyrgyzstan', 'KG'], ['Laos', 'LA'], ['Latvia', 'LV'], ['Lebanon', 'LB'], ['Liberia', 'LR'], ['Libya', 'LY'], 
   ['Liechtenstein', 'LI'], ['Lithuania', 'LT'], ['Luxembourg', 'LU'], ['MS Zaandam', 'XX'], ['Madagascar', 'MG'], 
   ['Malawi', 'MW'], ['Malaysia', 'MY'], ['Maldives', 'MV'], ['Mali', 'ML'], ['Malta', 'MT'], ['Mauritania', 'MR'], 
   ['Mauritius', 'MU'], ['Mexico', 'MX'], ['Moldova', 'MD'], ['Monaco', 'MC'], ['Mongolia', 'MN'], ['Montenegro', 'ME'], 
   ['Morocco', 'MA'], ['Mozambique', 'MZ'], ['Namibia', 'NA'], ['Nepal', 'NP'], ['Netherlands', 'NL'], ['New Zealand', 'NZ'], 
   ['Nicaragua', 'NI'], ['Niger', 'NE'], ['Nigeria', 'NG'], ['North Macedonia', 'MK'], ['Norway', 'NO'], ['Oman', 'OM'], 
   ['Pakistan', 'PK'], ['Panama', 'PA'], ['Papua New Guinea', 'PG'], ['Paraguay', 'PY'], ['Peru', 'PE'], ['Philippines', 'PH'], 
   ['Poland', 'PL'], ['Portugal', 'PT'], ['Qatar', 'QA'], ['Romania', 'RO'], ['Russia', 'RU'], ['Rwanda', 'RW'], 
   ['Saint Kitts and Nevis', 'KN'], ['Saint Lucia', 'LC'], ['Saint Vincent and the Grenadines', 'VC'], ['San Marino', 'SM'], 
   ['Saudi Arabia', 'SA'], ['Senegal', 'SN'], ['Serbia', 'RS'], ['Seychelles', 'SC'], ['Sierra Leone', 'SL'], 
   ['Singapore', 'SG'], ['Slovakia', 'SK'], ['Slovenia', 'SI'], ['Somalia', 'SO'], ['South Africa', 'ZA'], ['Spain', 'ES'], 
   ['Sri Lanka', 'LK'], ['Sudan', 'SD'], ['Suriname', 'SR'], ['Sweden', 'SE'], ['Switzerland', 'CH'], ['Syria', 'SY'], 
   ['Taiwan*', 'TW'], ['Tanzania', 'TZ'], ['Thailand', 'TH'], ['Timor-Leste', 'TL'], ['Togo', 'TG'], 
   ['Trinidad and Tobago', 'TT'], ['Tunisia', 'TN'], ['Turkey', 'TR'], ['US', 'US'], ['Uganda', 'UG'], ['Ukraine', 'UA'], 
   ['United Arab Emirates', 'AE'], ['United Kingdom', 'GB'], ['Uruguay', 'UY'], ['Uzbekistan', 'UZ'], ['Venezuela', 'VE'], 
   ['Vietnam', 'VN'], ['West Bank and Gaza', 'PS'], ['Zambia', 'ZM'], ['Zimbabwe', 'ZW']]



# APP
def main():
  # Add a title
  st.title('COVID19 predictions')
  # get preliminary data
  with st.spinner('Global map is being updated...'):
    time.sleep(3)
    countries, codes, cases, world_cases_now, evolution_of_cases_worldwide = get_codes()
  st.header('Cases around the world:')
  st.markdown(world_cases_now)
  # show map
  plot_world_data(countries, codes, cases, world_cases_now, evolution_of_cases_worldwide)
  # header
  st.header('The rate of global infection')
  # show global evolution in a line chart
  st.line_chart(evolution_of_cases_worldwide)
  # top countries
  top10_countries, top10_columns, top10_with_datetimes = get_top_10()
  # show  evolution for top x countries in number of cases
  st.header('Top 10 countries in number of cases')
  # style it
  cm = sns.light_palette("red", as_cmap=True)
  # show table
  st.table(top10_with_datetimes[-1:].style.background_gradient(cmap=cm, axis=1))
  # chart it
  st.line_chart(top10_columns)
  # Start querying for prediction
  st.header('Predict the spread of COVID-19')
  # pick your country
  select = st.multiselect("Select one country:", [item[0] for item in countries_and_codes])
  if select:
    try:
      # query selected country
      with st.spinner('Data is being prepared...'):
        time.sleep(2)
        country = get_data(countries_and_codes, select)
      # notification factor where official data == 100% accurate
      notification_percentual = 100
      # create sidebar for sub-notification scenarios
      st.sidebar.subheader('Sub-notification')
      st.sidebar.info('You can test predictions assuming which percentage of the official number of cases are not being reported. For example, if only 50% of cases are being reported, move the slider to the middle. Notification depends on the capacity health services have for testing the population, and may vary greatly from country to country, and even from region to region within a country.')
      notification_percentual = st.sidebar.slider(
        "Notification in %", 
        min_value=0,
        max_value=100,
        step=5,
        value=100)
      #show timeline
      first_day, df = timeline_of_cases_and_deaths(country, notification_percentual)
      # plot  daily increase of cases
      plot_daily_increase(select, first_day, df)

      # A brief theoretical explanation
      st.header('Predicting the outcome')
      st.subheader('*The Logistic model*')
      st.write('The logistic model has been widely used to describe the growth of a population. An infection can be described as the growth of the population of a pathogen agent, so applying a logistic model seems reasonable. This formula is very known among data scientists because it’s used in the logistic regression classifier and as an activation function of neural networks. The most generic expression of a logistic function is:')
      st.latex(r'''
           f(x,a,b,c) =
           \frac{c}{1+e^{-(x-b)/a)}}
           ''')
      st.write('In this formula, we have the variable x that is the time and three parameters: a,b,c.')
      st.write('- *a* refers to the infection speed')
      st.write('- *b* is the day with the maximum infections occurred')
      st.write('- *c* is the total number of recorded infected people at the infection’s end')
      st.write('At high time values, the number of infected people gets closer and closer to c and that’s the point at which we can say that the infection has ended. This function has also an inflection point at b, that is the point at which the first derivative starts to decrease (i.e. the peak after which the infection starts to become less aggressive and decreases)')

      # Data & projections for cases, for today and the former 2 days
      prediction_of_maximum_cases(df, notification_percentual)
      # Data & projections for deaths, for today and the former 2 days
      prediction_of_deaths(df)

      # Final considerations
      st.header('Notes')
      st.subheader('*Data Sources*')
      st.markdown('Data used for prediction is operated by the Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE) and collected from the [Worldwide Data repository.] (https://coronavirus.jhu.edu/map.html)')
      st.subheader('*Testing*')
      st.write('Predictions that apply sub-notification of cases should be interpreted with *extreme caution*. Give preference to official data. Unless sub-notification is due to a State policy, we believe that official data is still useful for projections into the future.')
      st.markdown('For a take on the limitation of models due to lack of testing, please refer to this article by Nate Silver: [Coronavirus Case Counts Are Meaningless, Unless you know something about testing. And even then, it gets complicated.](https://fivethirtyeight.com/features/coronavirus-case-counts-are-meaningless/amp/?__twitter_impression=true)')
      st.subheader('*Model*')
      st.write('There is a common aphorism in statistics: "*All models are wrong, but some are useful*."')   
      st.write('Although the logistic model seems to be the most reasonable one, the shape of the curve will probably change due to exogenous effects like new infection hotspots, government actions to bind the infection and so on.')
      st.markdown('>*Imperfect data isn’t necessarily a problem if we know how it’s imperfect, and can adjust accordingly. For example, suppose your watch is an hour slow. If you aren’t aware of this, it will probably cause you problems. But if you know about the delay, you can make a mental adjustment and still be on time. Likewise, if we know the delay in reporting during an outbreak, we can adjust how we interpret the outbreak curve. Such ‘nowcasting’, which aims to understand the situation as it currently stands, is often necessary before forecasts can be made*. -Adam Kucharski, [The Rules of Contagion.](https://www.amazon.com.br/Rules-Contagion-Outbreaks-Infectious-Diseases-ebook/dp/B07JLSHT7M)')
      st.write('**Predictions of this model will start to become more useful only within a few weeks, reasonably after the infection peak.**')
      st.subheader('*Credits*')
      st.write('This page was created by Vítor Patalano, based on two main sources:')
      st.markdown('- This article by Gianluca Malato: [Covid-19 infection in Italy. Mathematical models and predictions] (https://towardsdatascience.com/covid-19-infection-in-italy-mathematical-models-and-predictions-7784b4d7dd8d)')
      st.markdown('- This notebook by Enrico Ros: [Live analysis of the growth for the Italian COVID19 pandemic] (https://colab.research.google.com/drive/16CzLtNCnYq8x3gEBOgg2pMmDQngSD2vG#scrollTo=zJMZaWqJFNJz)')
      st.subheader('*Source code*')
      st.write('This project was created using python and streamlit. Source code can be found on the github link bellow. You are free to collaborate, fork, clone and improve on it. *Science must be contagious*!')
      st.markdown('[COVID19 Predictions on Github.](https://github.com/patalanov/covid19-predictions)')
      st.write('**Stay home.**')
    except Exception as e:
      print ('There is a problem. Please try again later.', e)



# - world data - alpha3 code for countries 
@st.cache(suppress_st_warning=True)
def get_codes():
  # global, generic data
  df = pd.read_csv('https://covid.ourworldindata.org/data/ecdc/total_cases.csv')
  # lookup function
  def look(x):
      try:
          return pycountry.countries.search_fuzzy(x)[0].alpha_3
      except:
          return x
  # get countries
  countries = list(df)[2:]
  print (df)
  # last entry
  world_cases = df['World'].iloc[-1]
  evolution_of_cases_worldwide = df['World']
  #get cases
  cases=[]
  for item in df:
    if item in countries:
      # most recent is the last
      n = df[item].iloc[-1]
      cases.append(n)
  # get alpha 3 code for map locations
  iso3_codes = [look(c) for c in countries]
  return (countries, iso3_codes, cases, world_cases, evolution_of_cases_worldwide)


@st.cache(suppress_st_warning=True)
def get_top_10():
  df = pd.read_csv('https://covid.ourworldindata.org/data/ecdc/total_cases.csv')
  
  top10 = df.iloc[:, 2:].iloc[-1].nlargest(10)
  top10_countries = df.iloc[-1, 2:].astype(float).nlargest(10)
  top10_columns = df[df.iloc[-1, 2:].astype(float).nlargest(10).index]
  # for datetime
  url = 'https://covid.ourworldindata.org/data/ecdc/total_cases.csv'
  
  df = pd.read_csv(url, index_col=0, parse_dates=[0])
  
  top10_with_datetimes = df[df.iloc[-1, 1:].astype(float).nlargest(10).index]

  return (top10_countries, top10_columns, top10_with_datetimes)



# - single country data - use alpha2 code for countries 
@st.cache(suppress_st_warning=True)
def get_data(countries_and_codes, select):
  # instantiate wrapper to data api
  covid19 = COVID19Py.COVID19()
  # get data from Hopkins University
  country_data = covid19.getLocationByCountryCode([item[1] for item in countries_and_codes if item[0] == select[0]], timelines=True)
  return country_data



def plot_world_data(countries, codes, cases, world_cases_now, evolution_of_cases_worldwide):
  data = [go.Choropleth(
      locations = codes,
      z = cases,
      text = countries,
      colorscale = [
        [0, "rgb(103,0,13)"],
        [0.35, "rgb(165,15,21)"],
        [0.5, "rgb(203,24,29)"],
        [0.6, "rgb(239,59,44)"],
        [0.7, "rgb(251,106,74)"],
        [1, "rgb(254,229,217)"]
      ],
      autocolorscale = False,
      reversescale = True,
      marker = go.choropleth.Marker(
          line = go.choropleth.marker.Line(
              color = 'rgb(180,180,180)',
              width = 0.5
          )),
      colorbar = go.choropleth.ColorBar(
          #tickprefix = '$',
          title = 'Cases'),
  )]

  layout = go.Layout(
      title = go.layout.Title(
          text = 'Covid19 Global Map'
      ),
      geo = go.layout.Geo(
          showframe = False,
          showcoastlines = False,
          projection = go.layout.geo.Projection(
              type = 'equirectangular'
          )
      ),
      annotations = [go.layout.Annotation(
          x = 0.55,
          y = 0.1,
          xref = 'paper',
          yref = 'paper',
          text = 'Source: <a href="https://covid.ourworldindata.org">\
              Our World In Data</a>',
          showarrow = False
      )]
  )

  fig = go.Figure(data = data, layout = layout)
  #fig.show()
  # show global cases on a map
  st.plotly_chart(fig)


def timeline_of_cases_and_deaths(country, notification_percentual):
  # filter target data
  cases = country[0]["timelines"]["confirmed"]["timeline"]
  #print ('CASES', cases, 'ITEMS', cases.items())
  deaths =  country[0]["timelines"]["deaths"]["timeline"]
  # create dataframes for cases
  cases_df = pd.DataFrame(list(cases.items()),
               columns=['day', 'cases'])
  # apply subnotification percentage
  # if none was entered, it is == 1
  cases_df.cases = cases_df.cases*100/notification_percentual
  # create dataframes for deaths
  deaths_df = pd.DataFrame(list(deaths.items()),
               columns=['day', 'deaths'])
  # apply subnotification percentage
  # if none was entered, it is == 1
  #deaths_df.deaths*=sub_factor
  # merge into one single dataframe
  df = cases_df.merge(deaths_df, on='day')
  # add culumn for 'day'
  df = df.loc[:, ['day','deaths','cases']]
  # set first day of pendemic
  first_day = datetime(2020, 1, 2) - timedelta(days=1)
  # time format
  FMT = "%Y-%m-%dT%H:%M:%SZ"
  # strip and correct timelines
  df['day'] = df['day'].map(lambda x: (datetime.strptime(x, FMT) - first_day).days)
  # bring steramlit to the stage
  st.header('Timeline of cases and deaths')
  st.write('Day 01 of pandemic outbreak is January 1st, 2020.')
  st.write('(*For scenarios with sub-notification, click on side bar*)')
  # make numerical dataframe optional
  if st.checkbox('Show numeric data'):
    cm = sns.light_palette("red", as_cmap=True)
    st.dataframe(df.style.background_gradient(cmap=cm, axis=0))
  st.write('The data plots the following line chart for cases and deaths.')
  # show data on a line chart
  st.line_chart(df)
  return first_day, df


def plot_daily_increase(select, first_day, df):
  dfG = df.copy()
  dfG['cases_diff'] = dfG.diff()['cases']
  dfG['cases_growth_%'] = round(dfG['cases_diff'] / (dfG['cases'] - dfG['cases_diff']) * 100, 1)
  dfG['date'] = [first_day + timedelta(days = day) for day in dfG['day']]
  print(" data for the last 7 days")
  print (dfG[-7:])
  # show last 7 days in case growth
  st.header('Official data for the past 7 days')
  st.write('In this table, we show the growth of infection on a daily basis, which is crucial to understand the speed of infection. Top values are highlighted.')
  cm = sns.light_palette("red", as_cmap=True)
  st.table(dfG[-7:].style.background_gradient(cmap=cm,axis=0))
  # add cases growth
  dfg2 = dfG[-14:]
  x = dfg2['day'].tolist()
  y = dfg2['cases_growth_%'].tolist()
  # Daily increase in the infected population
  plt.rc('font', size=14)
  plt.figure(figsize=(8, 4))
  plt_axes = plt.gca()
  plt_axes.grid(axis='y', color=(0.4, 0.4, 0.4), alpha=0.2)
  plt.stackplot(x, y, color=(0.92, 0.26, 0.21, 0.3), linewidth=0)
  plt.plot(x, y, color=(0.92, 0.26, 0.21), linewidth=2)
  plt.scatter(x, y, color=(0.92, 0.26, 0.21), label=[item[0] for item in countries_and_codes if item[0] == select[0]][0], linewidth=3)
  plt.xlim(int(min(x)), int(max(x) + 5))
  plt.ylim(0, 60)
  plt.title("Daily increase in the infected population")
  plt.xlabel("Day of the year, 2020")
  plt.ylabel("Daily % increase")
  plt.legend()
  plt.show()
  # header, text and plot
  st.header('Daily increase')
  st.write('Now, we plot the daily increase of cases throughout the year of 2020.')
  st.pyplot()


# formula for the model
def logistic_model(x,a,b,c):
    return c/(1+np.exp(-(x-b)/a))


# relevant functions
def predict_logistic_maximum(df, column = 'cases'):
      samples = df.shape[0]
      x_days = df['day'].tolist()
      y_cases = df[column].tolist()
      speed_guess = 2.5
      peak_guess = 120
      amplitude_guess = 250000
      if (column == 'deaths'):
        amplitude_guess = (amplitude_guess * speed_guess/100)   
      initial_guess =speed_guess, peak_guess, amplitude_guess

      fit = curve_fit(logistic_model, x_days, y_cases,p0=initial_guess,  maxfev=9999)

      # parse the result of the fit
      speed, x_peak, y_max = fit[0]
      speed_error, x_peak_error, y_max_error = [np.sqrt(fit[1][i][i]) for i in [0, 1, 2]]

      # find the "end date", as the x (day of year) where the function reaches 99.99%
      end = int(fsolve(lambda x: logistic_model(x, speed, x_peak, y_max) - y_max * 0.9999, x_peak))

      return x_days, y_cases, speed, x_peak, y_max, x_peak_error, y_max_error, end, samples


def print_prediction(df, label, column = 'cases'):
    x, y, speed, x_peak, y_max, x_peak_error, y_max_error, end, samples = predict_logistic_maximum(df, column)
    print(label + "'s prediction: " +
          "maximum " + column + " : " + str(np.int64(round(y_max))) +
          " (± " + str(np.int64(round(y_max_error))) + ")" +
          ", peak at calendar day: " + str(datetime(2020, 1, 2) + timedelta(days=int(round(x_peak)))) +
          " (± " + str(round(x_peak_error, 2)) + ")" +
          ", ending on day: " + str(datetime(2020, 1, 2) + timedelta(days=end)))

    st.markdown(label + "'s prediction: " + "maximum " + column + " : **" + str(np.int64(round(y_max))) + "** (± " + str(np.int64(round(y_max_error))) + ")" + ", peak at calendar day: " + str(datetime(2020, 1, 2) + timedelta(days=int(round(x_peak)))) + " (± " + str(round(x_peak_error, 2)) + ")" + ", ending on day: " + str(datetime(2020, 1, 2) + timedelta(days=end)))

    return y_max


def add_real_data(df, label,column = 'cases', color=None):
    x = df['day'].tolist()
    y = df[column].tolist()
    plt.scatter(x, y, label="Data (" + label + ")", c=color)


def add_logistic_curve(df, label,column = 'cases', **kwargs):
    x, _, speed, x_peak, y_max, _, _, end, _ = predict_logistic_maximum(df, column)
    x_range = list(range(min(x), end))
    plt.plot(x_range,
             [logistic_model(i, speed, x_peak, y_max) for i in x_range],
             label="Logistic model (" + label + "): " + str(int(round(y_max))),
             **kwargs)
    return y_max


def label_and_show_plot(plt, title, y_max=None):
    plt.title(title)
    plt.xlabel("Days since 1 January 2020")
    plt.ylabel("Total number of people")
    if (y_max):
        plt.ylim(0, y_max * 1.1)
    plt.legend()
    plt.show()


def prediction_of_maximum_cases(df, notification_percentual):
  plt.figure(figsize=(12, 8))
  add_real_data(df[:-2], "2 days ago")
  add_real_data(df[-2:-1], "yesterday")
  add_real_data(df[-1:], "today")
  add_logistic_curve(df[:-2], "2 days ago", dashes=[8, 8])
  add_logistic_curve(df[:-1], "yesterday", dashes=[4, 4])
  y_max = add_logistic_curve(df, "today")
  label_and_show_plot(plt, "Best logistic fit with the freshest data", y_max)
  # A bit more theory 
  st.header('Prediction of maximum cases')
  # considering the user entered notification values
  if notification_percentual == 1:
    st.markdown("With sub-notification of 0%.")
  else:
    st.markdown("With sub-notification of " + str(int(round(100 - notification_percentual))) + " %.")

  st.write('At high time values, the number of infected people gets closer and closer to *c* and that’s the point at which we can say that the infection has ended. This function has also an inflection point at *b*, that is the point at which the first derivative starts to decrease (i.e. the peak after which the infection starts to become less aggressive and decreases).')
  # plot
  st.pyplot(clear_figure=False)
  # fit the data to the model (find the model variables that best approximate)
  st.subheader('Predictions as of *today*, *yesterday* and *2 days ago*')

  print_prediction(df[:-2], "2 days ago")
  print_prediction(df[:-1], "yesterday")
  pred = print_prediction(df, "today")
  # PREDICTION 1
  st.header('Infection stabilization')
  st.markdown("Predictions as of today, the total infection should stabilize at **" + str(int(round(pred))) + "** cases.")


def prediction_of_deaths(df):
  # Plot
  plt.figure(figsize=(12, 8))
  add_real_data(df[:-2], "2 days ago", column = 'deaths')
  add_real_data(df[-2:-1], "yesterday", column = 'deaths')
  add_real_data(df[-1:], "today", column = 'deaths')
  add_logistic_curve(df[:-2], "2 days ago",column='deaths', dashes=[8, 8])
  add_logistic_curve(df[:-1], "yesterday",column='deaths', dashes=[4, 4])
  y_max = add_logistic_curve(df, "today", column='deaths')
  label_and_show_plot(plt, "Best logistic fit with the freshest data", y_max)

  st.header('Prediction of deaths')
  st.pyplot(clear_figure=False)

  st.subheader('Predictions as of *today*, *yesterday* and *2 days ago*')

  print_prediction(df[:-2], "2 days ago", 'deaths')
  print_prediction(df[:-1], "yesterday", 'deaths')
  pred = print_prediction(df, "today", 'deaths')
  print()
  html_print("As of today, the total deaths should stabilize at <b>" + str(int(round(pred))) + "</b>")
  # PREDICTION 2
  st.header('Deaths stabilization')
  st.markdown("As of today, the total number of deaths should stabilize at **" + str(int(round(pred))) + "** cases.")


if __name__ == '__main__':
  main()





















