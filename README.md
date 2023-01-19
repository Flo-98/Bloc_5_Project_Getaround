# Jedha_Project_Getaround

Bloc n°5: Industrialisation d'un algorithme d'apprentissage automatique et automatisation des processus de décision

7ème projet de la formation Jedha pour obtenir la certification en Data Science. Le projet porte sur de l'analyse de données et le déploiement d'application

Nom: Sutz

Prénom: Florian

Mail: floriansutz@hotmail.fr

Lien de la vidéo :
lien du dashboard: https://getaround-manage-board.herokuapp.com/
Lien de l'API: https://getaound-predic-api.herokuapp.com/docs#/

Présentation du répository:

- streamlit_app : contient les différents fichiers ayant servi pour créer et déployer le dashboard portant sur l'analyse des locations rendu en retard, leurs occurences, leurs impacts, et la nouvelle fonctionnalité du "seuil". Le fichier contenant le script du dashboard est "app.py".
Le travail de fond pour cette analyse a été effectué dans le fichier Deployment_project.ipynb (qui ne se trouve pas dans le dossier streamlit), il contient également des analyses/informations supplémentaires qui ne sont pas présentes dans le dashboard. 

Lien du dashboard: https://getaround-manage-board.herokuapp.com/

- Price_prediction_FASTAPI: contient les différents fichiers ayant servi pour créer et déployer l'API mis en place pour fournir une prédiction de prix pour la location de voiture basé sur les caractéristiques de la voiture. Le fichier contenant le script de construction de l'API est "app.py", le fichier "model_final.json" est le modèle de machine learning utilisé, et "preprocessor.pkl" le preprocesseur. 
Le travail de fond pour produire le modèle, le preprocesseur, ou encore le dataset nettoyé se trouve dans le fichier "Price_optimization.ipynb".

Lien de l'API: https://getaound-predic-api.herokuapp.com/docs#/

- Deployment_project.ipynb : contient le travail de fond d'analyse des retards présent dans le dashboard, ainsi que des analyses et informations supplémentaires qui n'ont pas été ajouté au dashboard.

- Price_optimization.ipynb: contient le travail effectué pour produire le modèle de machine learning utilisé pour l'API, passant par le nettoyage, le preprocessing et l'essai de différents modèles. 

- get_around_delay_analysis.xlsx, et get_around_pricing_project.csv: datasets donnés et utilisé pour le projet.


Contexte et consigne: 

GetAround
GetAround is the Airbnb for cars. You can rent cars from any person for a few hours to a few days! Founded in 2009, this company has known rapid growth. In 2019, they count over 5 million users and about 20K available cars worldwide.

As Jedha's partner, they offered this great challenges:

Context
When renting a car, our users have to complete a checkin flow at the beginning of the rental and a checkout flow at the end of the rental in order to:

Assess the state of the car and notify other parties of pre-existing damages or damages that occurred during the rental.
Compare fuel levels.
Measure how many kilometers were driven.
The checkin and checkout of our rentals can be done with three distinct flows:

📱 Mobile rental agreement on native apps: driver and owner meet and both sign the rental agreement on the owner’s smartphone
Connect: the driver doesn’t meet the owner and opens the car with his smartphone
📝 Paper contract (negligible)
Project 🚧
For this case study, we suggest that you put yourselves in our shoes, and run an analysis we made back in 2017 🔮 🪄

When using Getaround, drivers book cars for a specific time period, from an hour to a few days long. They are supposed to bring back the car on time, but it happens from time to time that drivers are late for the checkout.

Late returns at checkout can generate high friction for the next driver if the car was supposed to be rented again on the same day : Customer service often reports users unsatisfied because they had to wait for the car to come back from the previous rental or users that even had to cancel their rental because the car wasn’t returned on time.

Goals 🎯
In order to mitigate those issues we’ve decided to implement a minimum delay between two rentals. A car won’t be displayed in the search results if the requested checkin or checkout times are too close from an already booked rental.

It solves the late checkout issue but also potentially hurts Getaround/owners revenues: we need to find the right trade off.

Our Product Manager still needs to decide:

threshold: how long should the minimum delay be?
scope: should we enable the feature for all cars?, only Connect cars?
In order to help them make the right decision, they are asking you for some data insights. Here are the first analyses they could think of, to kickstart the discussion. Don’t hesitate to perform additional analysis that you find relevant.

Which share of our owner’s revenue would potentially be affected by the feature How many rentals would be affected by the feature depending on the threshold and scope we choose?
How often are drivers late for the next check-in? How does it impact the next driver?
How many problematic cases will it solve depending on the chosen threshold and scope?
Web dashboard
First build a dashboard that will help the product Management team with the above questions. You can use streamlit or any other technology that you see fit.

Machine Learning - /predict endpoint
In addition to the above question, the Data Science team is working on pricing optimization. They have gathered some data to suggest optimum prices for car owners using Machine Learning.

You should provide at least one endpoint /predict. The full URL would look like something like this: https://your-url.com/predict.

This endpoint accepts POST method with JSON input data and it should return the predictions. We assume inputs will be always well formatted. It means you do not have to manage errors. We leave the error handling as a bonus.

Input example:

{
  "input": [[7.0, 0.27, 0.36, 20.7, 0.045, 45.0, 170.0, 1.001, 3.0, 0.45, 8.8], [7.0, 0.27, 0.36, 20.7, 0.045, 45.0, 170.0, 1.001, 3.0, 0.45, 8.8]]
}
The response should be a JSON with one key prediction corresponding to the prediction.

Response example:

{
  "prediction":[6,6]
}
Documentation page
You need to provide the users with a documentation about your API.

It has to be located at the /docs of your website. If we take the URL example above, it should be located directly at https://your-url.com/docs).

This small documentation should at least include:

An h1 title: the title is up to you.
A description of every endpoints the user can call with the endpoint name, the HTTP method, the required input and the expected output (you can give example).
You are free to add other any other relevant informations and style your HTML as you wish.

Online production
You have to host your API online. We recommend you to use Heroku as it is free of charge. But you are free to choose any other hosting provider.
