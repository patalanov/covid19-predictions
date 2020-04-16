# Covid19-predictions
A tool for predicting the evolution of Covid19 in your country.

![00](https://user-images.githubusercontent.com/6799245/79267520-ae5cac00-7e6f-11ea-8f25-baab3c671a54.png)

![01](https://user-images.githubusercontent.com/6799245/79267670-f11e8400-7e6f-11ea-8d01-428079bf0a94.png)

![11](https://user-images.githubusercontent.com/6799245/79494057-c1e74e80-7ff8-11ea-9089-754ac2b46f8c.png)

![02](https://user-images.githubusercontent.com/6799245/78595118-d15be000-781f-11ea-92bb-5a36a4b2753a.png)

![03](https://user-images.githubusercontent.com/6799245/79267891-422e7800-7e70-11ea-8181-976d9e3219f3.png)

![04](https://user-images.githubusercontent.com/6799245/78592869-1da52100-781c-11ea-89de-ad86f5738a07.png)

![05](https://user-images.githubusercontent.com/6799245/78592872-1e3db780-781c-11ea-8b11-e01a79acb2aa.png)

![06](https://user-images.githubusercontent.com/6799245/78592874-1ed64e00-781c-11ea-87e5-8a203f67dde4.png)

![07](https://user-images.githubusercontent.com/6799245/78592880-1f6ee480-781c-11ea-8377-47394e66d6cc.png)

![08](https://user-images.githubusercontent.com/6799245/78592882-1f6ee480-781c-11ea-84c4-724de6e76b43.png)

![09](https://user-images.githubusercontent.com/6799245/78592883-20077b00-781c-11ea-8c7f-8053783387d2.png)

## **You can also make predictions adding some percentual of sub-notification of cases.**

![10](https://user-images.githubusercontent.com/6799245/79268106-9afe1080-7e70-11ea-9951-6b065dfd2a22.png)

## Notes
Data Sources
All data is collected from [Johns Hopkins University & Medicine.](https://coronavirus.jhu.edu/map.html)

## Testing
This prediction does not take into account an eventual lack of testing for Covid19 in your country. The sub-notification of cases can alter drastically the shape of the curves as well as the predictions. But unless sub-notification is due to a State policy, we believe that official data is still useful for projections into the future.

For a take on the limitation of models due to lack of testing, please refer to this article by Nate Silver: 
[Coronavirus Case Counts Are Meaningless, Unless you know something about testing. And even then, it gets complicated.](https://fivethirtyeight.com/features/coronavirus-case-counts-are-meaningless/amp/?__twitter_impression=true)

## Model
There is a common aphorism in statistics: "**All models are wrong, but some are useful.**"

Although the logistic model seems to be the most reasonable one, the shape of the curve will probably change due to exogenous effects like new infection hotspots, government actions to bind the infection and so on.

"_Imperfect data isn’t necessarily a problem if we know how it’s imperfect, and can adjust accordingly. For example, suppose your watch is an hour slow. If you aren’t aware of this, it will probably cause you problems. But if you know about the delay, you can make a mental adjustment and still be on time. Likewise, if we know the delay in reporting during an outbreak, we can adjust how we interpret the outbreak curve. Such ‘nowcasting’, which aims to understand the situation as it currently stands, is often necessary before forecasts can be made_". Quote from Adam’s Kucharski book The Rules of Contagion.

Predictions of this model will start to become useful only within a few weeks, reasonably after the infection peak.

## Credits
This page was created by Vítor Patalano, based on two main sources:

This article by Gianluca Malato: [Covid-19 infection in Italy. Mathematical models and predictions](https://towardsdatascience.com/covid-19-infection-in-italy-mathematical-models-and-predictions-7784b4d7dd8d)

This notebook by Enrico Ros: [Live analysis of the growth for the Italian COVID19 pandemic](https://colab.research.google.com/drive/16CzLtNCnYq8x3gEBOgg2pMmDQngSD2vG#scrollTo=zJMZaWqJFNJz)

## Source code
This project was created using python and streamlit. You are free to collaborate, fork, clone and improve on it. 

_Science must be contagious_!

Stay home.