from datetime import datetime, timedelta
import json
import itertools
# dataframes
import pandas as pd
import numpy as np
# plotting
import matplotlib.pyplot as plt
from PIL import Image
from IPython.display import HTML as html_print
# machine learning
from sklearn.metrics import mean_squared_error
from scipy.optimize import curve_fit
from scipy.optimize import fsolve
# app
import streamlit as st
# big data
import COVID19Py


# Add a title
st.title('COVID19 predictions')
# Add some text
st.header('Check the pandemic evolution in your country.')

covid19 = COVID19Py.COVID19()

# # the model
# @st.cache 
# def logistic_model(x,a,b,c):
#     return c/(1+np.exp(-(x-b)/a))

# # relevant functions
# @st.cache 
# def predict_logistic_maximum(df, column = 'cases'):
#       samples = df.shape[0]
#       x_days = df['day'].tolist()
#       y_cases = df[column].tolist()
#       speed_guess = 2.5
#       peak_guess = 120
#       amplitude_guess = 250000
#       if (column == 'deaths'):
#         amplitude_guess = (amplitude_guess * speed_guess/100)   
#       initial_guess =speed_guess, peak_guess, amplitude_guess

#       fit = curve_fit(logistic_model, x_days, y_cases,p0=initial_guess,  maxfev=9999)

#       # parse the result of the fit
#       speed, x_peak, y_max = fit[0]
#       speed_error, x_peak_error, y_max_error = [np.sqrt(fit[1][i][i]) for i in [0, 1, 2]]

#       # find the "end date", as the x (day of year) where the function reaches 99.99%
#       end = int(fsolve(lambda x: logistic_model(x, speed, x_peak, y_max) - y_max * 0.9999, x_peak))

#       return x_days, y_cases, speed, x_peak, y_max, x_peak_error, y_max_error, end, samples

# #@st.cache 
# def print_prediction(df, label, column = 'cases'):
#     x, y, speed, x_peak, y_max, x_peak_error, y_max_error, end, samples = predict_logistic_maximum(df, column)
#     print(label + "'s prediction: " +
#           "maximum " + column + " : " + str(np.int64(round(y_max))) +
#           " (± " + str(np.int64(round(y_max_error))) + ")" +
#           ", peak at calendar day: " + str(datetime(2020, 1, 2) + timedelta(days=int(round(x_peak)))) +
#           " (± " + str(round(x_peak_error, 2)) + ")" +
#           ", ending on day: " + str(datetime(2020, 1, 2) + timedelta(days=end)))

#     st.markdown(label + "'s prediction: " + "maximum " + column + " : **" + str(np.int64(round(y_max))) + "** (± " + str(np.int64(round(y_max_error))) + ")" + ", peak at calendar day: " + str(datetime(2020, 1, 2) + timedelta(days=int(round(x_peak)))) + " (± " + str(round(x_peak_error, 2)) + ")" + ", ending on day: " + str(datetime(2020, 1, 2) + timedelta(days=end)))

#     return y_max

# @st.cache 
# def add_real_data(df, label,column = 'cases', color=None):
#     x = df['day'].tolist()
#     y = df[column].tolist()
#     plt.scatter(x, y, label="Data (" + label + ")", c=color)

# @st.cache 
# def add_logistic_curve(df, label,column = 'cases', **kwargs):
#     x, _, speed, x_peak, y_max, _, _, end, _ = predict_logistic_maximum(df, column)
#     x_range = list(range(min(x), end))
#     plt.plot(x_range,
#              [logistic_model(i, speed, x_peak, y_max) for i in x_range],
#              label="Logistic model (" + label + "): " + str(int(round(y_max))),
#              **kwargs)
#     return y_max

# @st.cache 
# def label_and_show_plot(plt, title, y_max=None):
#     plt.title(title)
#     plt.xlabel("Days since 1 January 2020")
#     plt.ylabel("Total number of people")
#     if (y_max):
#         plt.ylim(0, y_max * 1.1)
#     plt.legend()
#     plt.show()

# get data from Hopkins University
#data = covid19.getAll()
countries_and_codes = [['Afghanistan', 'AF'], ['Albania', 'AL'], ['Algeria', 'DZ'], ['Andorra', 'AD'], ['Angola', 'AO'], ['Antigua and Barbuda', 'AG'], ['Argentina', 'AR'], ['Armenia', 'AM'], ['Australia', 'AU'], ['Austria', 'AT'], ['Azerbaijan', 'AZ'], ['Bahamas', 'BS'], ['Bahrain', 'BH'], ['Bangladesh', 'BD'], ['Barbados', 'BB'], ['Belarus', 'BY'], ['Belgium', 'BE'], ['Belize', 'BZ'], ['Benin', 'BJ'], ['Bhutan', 'BT'], ['Bolivia', 'BO'], ['Bosnia and Herzegovina', 'BA'], ['Botswana', 'BW'], ['Brazil', 'BR'], ['Brunei', 'BN'], ['Bulgaria', 'BG'], ['Burkina Faso', 'BF'], ['Burma', 'MM'], ['Burundi', 'BI'], ['Cabo Verde', 'CV'], ['Cambodia', 'KH'], ['Cameroon', 'CM'], ['Canada', 'CA'], ['Central African Republic', 'CF'], ['Chad', 'TD'], ['Chile', 'CL'], ['China', 'CN'], ['Colombia', 'CO'], ['Congo (Brazzaville)', 'CG'], ['Congo (Kinshasa)', 'CD'], ['Costa Rica', 'CR'], ["Cote d'Ivoire", 'CI'], ['Croatia', 'HR'], ['Cuba', 'CU'], ['Cyprus', 'CY'], ['Czechia', 'CZ'], ['Denmark', 'DK'], ['Diamond Princess', 'XX'], ['Djibouti', 'DJ'], ['Dominica', 'DM'], ['Dominican Republic', 'DO'], ['Ecuador', 'EC'], ['Egypt', 'EG'], ['El Salvador', 'SV'], ['Equatorial Guinea', 'GQ'], ['Eritrea', 'ER'], ['Estonia', 'EE'], ['Eswatini', 'SZ'], ['Ethiopia', 'ET'], ['Fiji', 'FJ'], ['Finland', 'FI'], ['France', 'FR'], ['Gabon', 'GA'], ['Gambia', 'GM'], ['Georgia', 'GE'], ['Germany', 'DE'], ['Ghana', 'GH'], ['Greece', 'GR'], ['Grenada', 'GD'], ['Guatemala', 'GT'], ['Guinea', 'GN'], ['Guinea-Bissau', 'GW'], ['Guyana', 'GY'], ['Haiti', 'HT'], ['Holy See', 'VA'], ['Honduras', 'HN'], ['Hungary', 'HU'], ['Iceland', 'IS'], ['India', 'IN'], ['Indonesia', 'ID'], ['Iran', 'IR'], ['Iraq', 'IQ'], ['Ireland', 'IE'], ['Israel', 'IL'], ['Italy', 'IT'], ['Jamaica', 'JM'], ['Japan', 'JP'], ['Jordan', 'JO'], ['Kazakhstan', 'KZ'], ['Kenya', 'KE'], ['Korea, South', 'KR'], ['Kosovo', 'XK'], ['Kuwait', 'KW'], ['Kyrgyzstan', 'KG'], ['Laos', 'LA'], ['Latvia', 'LV'], ['Lebanon', 'LB'], ['Liberia', 'LR'], ['Libya', 'LY'], ['Liechtenstein', 'LI'], ['Lithuania', 'LT'], ['Luxembourg', 'LU'], ['MS Zaandam', 'XX'], ['Madagascar', 'MG'], ['Malawi', 'MW'], ['Malaysia', 'MY'], ['Maldives', 'MV'], ['Mali', 'ML'], ['Malta', 'MT'], ['Mauritania', 'MR'], ['Mauritius', 'MU'], ['Mexico', 'MX'], ['Moldova', 'MD'], ['Monaco', 'MC'], ['Mongolia', 'MN'], ['Montenegro', 'ME'], ['Morocco', 'MA'], ['Mozambique', 'MZ'], ['Namibia', 'NA'], ['Nepal', 'NP'], ['Netherlands', 'NL'], ['New Zealand', 'NZ'], ['Nicaragua', 'NI'], ['Niger', 'NE'], ['Nigeria', 'NG'], ['North Macedonia', 'MK'], ['Norway', 'NO'], ['Oman', 'OM'], ['Pakistan', 'PK'], ['Panama', 'PA'], ['Papua New Guinea', 'PG'], ['Paraguay', 'PY'], ['Peru', 'PE'], ['Philippines', 'PH'], ['Poland', 'PL'], ['Portugal', 'PT'], ['Qatar', 'QA'], ['Romania', 'RO'], ['Russia', 'RU'], ['Rwanda', 'RW'], ['Saint Kitts and Nevis', 'KN'], ['Saint Lucia', 'LC'], ['Saint Vincent and the Grenadines', 'VC'], ['San Marino', 'SM'], ['Saudi Arabia', 'SA'], ['Senegal', 'SN'], ['Serbia', 'RS'], ['Seychelles', 'SC'], ['Sierra Leone', 'SL'], ['Singapore', 'SG'], ['Slovakia', 'SK'], ['Slovenia', 'SI'], ['Somalia', 'SO'], ['South Africa', 'ZA'], ['Spain', 'ES'], ['Sri Lanka', 'LK'], ['Sudan', 'SD'], ['Suriname', 'SR'], ['Sweden', 'SE'], ['Switzerland', 'CH'], ['Syria', 'SY'], ['Taiwan*', 'TW'], ['Tanzania', 'TZ'], ['Thailand', 'TH'], ['Timor-Leste', 'TL'], ['Togo', 'TG'], ['Trinidad and Tobago', 'TT'], ['Tunisia', 'TN'], ['Turkey', 'TR'], ['US', 'US'], ['Uganda', 'UG'], ['Ukraine', 'UA'], ['United Arab Emirates', 'AE'], ['United Kingdom', 'GB'], ['Uruguay', 'UY'], ['Uzbekistan', 'UZ'], ['Venezuela', 'VE'], ['Vietnam', 'VN'], ['West Bank and Gaza', 'PS'], ['Zambia', 'ZM'], ['Zimbabwe', 'ZW']]
# pick your country
select = st.multiselect("Select one country:", [item[0] for item in countries_and_codes])
if select:
  # query selected country
  country = covid19.getLocationByCountryCode([item[1] for item in countries_and_codes if item[0] == select[0]], timelines=True)
  # filter target data
  cases = country[0]["timelines"]["confirmed"]["timeline"]
  deaths =  country[0]["timelines"]["deaths"]["timeline"]
  # create dataframes for cases
  cases_df = pd.DataFrame(list(cases.items()),
  						 columns=['day', 'cases'])
  # create dataframes for deaths
  deaths_df = pd.DataFrame(list(deaths.items()),
  						 columns=['day', 'deaths'])
  # merge into one single dataframe
  df = cases_df.merge(deaths_df, on='day')
  print (df)

  df = df.loc[:, ['day','deaths','cases']]
  # set first day
  first_day = datetime(2020, 1, 2) - timedelta(days=1)
  # time format
  FMT = "%Y-%m-%dT%H:%M:%SZ"
  # strip and correct timelines
  df['day'] = df['day'].map(lambda x: (datetime.strptime(x, FMT) - first_day).days)
  
  st.header('Timeline of cases and deaths')
  st.write('Day 01 of pandemic outbreak is January 1st, 2020.')
  if st.checkbox('Show numeric data'):
    st.dataframe(df.style.highlight_max(axis=0))
  # show data on a line chart
  st.write('The data plots the following line chart for cases and deaths.')

  st.line_chart(df)
  #df.tail()
  #df['day'] = np.arange(len(merged_df))

  # the following block is just for displaying the input data, with some unused augmentation
  dfG = df.copy()
  dfG['cases_diff'] = dfG.diff()['cases']
  dfG['cases_growth_%'] = round(dfG['cases_diff'] / (dfG['cases'] - dfG['cases_diff']) * 100, 1)
  dfG['date'] = [first_day + timedelta(days = day) for day in dfG['day']]
  print(" data for the last 7 days")
  print (dfG[-7:])
  # show last 7 days in case growth
  st.header('Data for the past 7 days')
  st.write('In this table, we show the growth of infection on a daily basis, which is crucial to understand the speed of infection. Top values are highlighted.')
  st.dataframe(dfG[-7:].style.highlight_max(axis=0))

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
  plt.scatter(x, y, color=(0.92, 0.26, 0.21), label="Brasil", linewidth=3)
  plt.xlim(int(min(x)), int(max(x) + 5))
  plt.ylim(0, 60)
  plt.title("Daily increase in the infected population")
  plt.xlabel("Day of the year, 2020")
  plt.ylabel("Daily % increase")
  plt.legend()
  plt.show()
  # plot
  st.header('Daily increase')
  st.write('Now, we plot the daily increase of cases throghout the year of 2020.')
  st.pyplot()

  # print full dataframe
  # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
  #     print(df)

  st.header('Predicting the outcome')
  st.subheader('*The Logistic model*')

  st.write('The logistic model has been widely used to describe the growth of a population. An infection can be described as the growth of the population of a pathogen agent, so applying a logistic model seems reasonable. This formula is very known among data scientists because it’s used in the logistic regression classifier and as an activation function of neural networks.The most generic expression of a logistic function is:')
  st.latex(r'''
       f(x,a,b,c) =
       \frac{c}{1+e^{-(x-b)/a)}}
       ''')
  st.write('In this formula, we have the variable x that is the time and three parameters: a,b,c.')
  st.write('- *a* refers to the infection speed')
  st.write('- *b* is the day with the maximum infections occurred')
  st.write('- *c* is the total number of recorded infected people at the infection’s end')
  st.write('At high time values, the number of infected people gets closer and closer to c and that’s the point at which we can say that the infection has ended. This function has also an inflection point at b, that is the point at which the first derivative starts to decrease (i.e. the peak after which the infection starts to become less aggressive and decreases)')

  # the model
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
  # fit the data to the model (find the model variables that best approximate)
  st.header('Prediction of maximum cases')
  st.subheader('As of *today*, *yesterday* and *2 days ago*')

  print_prediction(df[:-2], "2 days ago")
  print_prediction(df[:-1], "yesterday")
  pred = print_prediction(df, "today")
  #print()
  plt.rc('font', size=14)
  # show
  st.header('Infection stabilization')
  st.markdown("As of today, the total infection should stabilize at **" + str(int(round(pred))) + "** cases.")
  st.pyplot()

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
  # Plot 1. data & projections, for today and the former 2 days
  plt.figure(figsize=(12, 8))
  add_real_data(df[:-2], "2 days ago")
  add_real_data(df[-2:-1], "yesterday")
  add_real_data(df[-1:], "today")
  add_logistic_curve(df[:-2], "2 days ago", dashes=[8, 8])
  add_logistic_curve(df[:-1], "yesterday", dashes=[4, 4])
  y_max = add_logistic_curve(df, "today")
  label_and_show_plot(plt, "Best logistic fit with the freshest data", y_max)

  st.header('Best scenario with the latest data')

  st.pyplot()

  # #Plot 2. What changed since 2 days ago that steered the count up.
  # plt.figure(figsize=(12, 6))
  # add_real_data(df[:-2], "2 days ago")
  # add_real_data(df[-2:], "today")
  # y_max = add_logistic_curve(df[:-2], "2 days ago", linewidth=1)
  # add_logistic_curve(df, "today", linewidth=3)
  # label_and_show_plot(plt, "How does the chart change with new information (the case 2 days ago)", y_max)
  # st.pyplot()

  # # #@title Try it yourself { run: "auto", vertical-output: true, form-width: "620px", display-mode: "form" }
  # points_to_discard = 13 #@param {type:"slider", min:0, max:15, step:1}
  # # Plot: discard initial data points
  # plt.figure(figsize=(8, 6))
  # pts = points_to_discard
  # add_real_data(df[pts:], "today")
  # add_real_data(df[:pts], str(pts) + " discarded samples")
  # y_max = add_logistic_curve(df[pts:], "discarding samples")
  # label_and_show_plot(plt, "Discarding the initial (" + str(pts) + ") data points", y_max)
  # pred = print_prediction(df[pts:], "Today Discarding the initial (" + str(pts) + ") data points")
  # print()
  # html_print("As of today, the total infection should stabilize at <b>" + str(int(round(pred))) + "</b>")
  # st.pyplot()


  # Deaths
  st.header('Prediction of deaths')
  st.subheader('As of *today*, *yesterday* and *2 days ago*')

  print_prediction(df[:-2], "2 days ago", 'deaths')
  print_prediction(df[:-1], "yesterday", 'deaths')
  pred = print_prediction(df, "today", 'deaths')
  print()
  html_print("As of today, the total deaths should stabilize at <b>" + str(int(round(pred))) + "</b>")


  st.header('Deaths stabilization')
  st.markdown("As of today, the total number of deaths should stabilize at **" + str(int(round(pred))) + "** cases.")
  st.pyplot()
  # Plot
  plt.figure(figsize=(12, 8))
  add_real_data(df[:-2], "2 days ago", column = 'deaths')
  add_real_data(df[-2:-1], "yesterday", column = 'deaths')
  add_real_data(df[-1:], "today", column = 'deaths')
  add_logistic_curve(df[:-2], "2 days ago",column='deaths', dashes=[8, 8])
  add_logistic_curve(df[:-1], "yesterday",column='deaths', dashes=[4, 4])
  y_max = add_logistic_curve(df, "today", column='deaths')
  label_and_show_plot(plt, "Best logistic fit with the freshest data", y_max)

  st.header('Best scenario with the latest data')

  st.pyplot()


  st.header('Notes')
  st.subheader('*Data Sources*')
  st.markdown('All data is collected from [Johns Hopkins University & Medicine.] (https://coronavirus.jhu.edu/map.html)')
  st.subheader('*Testing*')
  st.write('This prediction does not take into account an eventual lack of testing for Covid19 in your country. The subnotification of cases can alter drastically the shape of the curves as well as the predictions. But unless subnotification is based on a State policy, we believe that official data is still useful for projections into the future.')
  st.markdown('For a take on the limitation of models due to lack of testing, please refer to this article by Nate Silver: [Coronavirus Case Counts Are Meaningless, Unless you know something about testing. And even then, it gets complicated.](https://fivethirtyeight.com/features/coronavirus-case-counts-are-meaningless/amp/?__twitter_impression=true)')
  st.subheader('*Model*')
  st.write('Although the logistic model seems to be the most reasonable one, the shape of the curve will probably change due to exogenous effects like new infection hotspots, government actions to bind the infection and so on.')
  st.write('Predictions of this model will start to become useful only within a few weeks, reasonably after the infection peak.')
  st.subheader('*Credits*')
  st.write('This page was created by Vítor Patalano based on two sources:')
  st.markdown('- This article by Gianluca Malato: [Covid-19 infection in Italy. Mathematical models and predictions] (https://towardsdatascience.com/covid-19-infection-in-italy-mathematical-models-and-predictions-7784b4d7dd8d)')
  st.markdown('- This notebook by Enrico Ros: [Live analysis of the growth for the Italian COVID19 pandemic] (https://colab.research.google.com/drive/16CzLtNCnYq8x3gEBOgg2pMmDQngSD2vG#scrollTo=zJMZaWqJFNJz)')
  st.subheader('*Source code*')
























