import uvicorn
import json
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile
import joblib
import numpy as np
import xgboost
import sklearn

description = """
Get Around API suggest you the optimal rental price of a car. 
The goal of this API is to provide predictions based on a machine learning model taking data about the car as input 
(describe in the /features endpoint) in order to help the management team to decide a pricing for car rental. 

The features to enter to get a predictions are, in order:
- `model_key`: the brand of the car
- `mileage`: the mileage in kilometers
- `engine_power`: the engine power
- `fuel`: the type of fuel
- `paint_color`: the color of the car
- `car_type`: the type of car
- `private_parking_available`: The availability of a private parking for the car 
- `has_gps`: If the car is equiped of a gps
- `has_air_conditioning`: Does the car got air conditionning
- `automatic_car`: If the car is an automatic car
- `has_getaround_connect`:If the car is equiped of the get around connect
- `has_speed_regulator`: If the car is equiped of a speed regulator
- `winter_tires`: If the car is equiped of winter tires

To get more informations about the possible values to enter for each features please use the endpoint 'Features'.

API Endpoints:

## Preview
 
* `/preview` visualize a few rows of your dataset

## Features 

* `/features` give you the possible values for the features of the car

## Predictions 

* `/predict` give you a rental price proposition for the given features 


"""

tags_metadata = [
    {
        "name": "Preview",
        "description": "Endpoints that quickly explore dataset"
    },

    {
        "name": "Features",
        "description": "Endpoints that gives the list of the possible values to enter for each features in order to get a rental price prediction"
    },

    {
        "name": "Predictions",
        "description": "Endpoints that uses our Machine Learning model to suggest car pricing"
    }
]

app = FastAPI(
    title="Get Around API",
    description=description,
    version="1.0",
    contact={
        "name": "Sutz Florian",
    },
    openapi_tags=tags_metadata
)

class PredictionFeatures(BaseModel):
    model_key: str
    mileage: int
    engine_power: int
    fuel: str
    paint_color: str
    car_type: str
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool

@app.get("/features", tags=["Features"])
async def features(feature):
    """
    Get the possible values for each features: input the feature for which you want information
    """
    data = pd.read_csv('df_price_clean.csv')

    columns = [*data.loc[:,feature].value_counts().index]
    return columns


@app.post("/predict", tags=["Predictions"])
async def predict(new_line: PredictionFeatures):
    """
    Price prediction for given car features. Endpoint will return a dictionnary like this:

    ```
    {'prediction': prediction_value}
    ```

    You need to give this endpoint all columns values as dictionnary.
    """
    # Read data 
    new_line = dict(new_line)
    input_df = pd.DataFrame(columns=['model_key', 'mileage', 'engine_power', 'fuel', 'paint_color','car_type', 'private_parking_available', 'has_gps',
       'has_air_conditioning', 'automatic_car', 'has_getaround_connect','has_speed_regulator', 'winter_tires'])
    input_df.loc[0] = list(new_line.values())

    # Load model & predict
   
    loaded_model = xgboost.XGBRegressor()
    loaded_model.load_model('model_final.json')
    loaded_preprocessor = joblib.load('preprocessor.pkl')
    df = loaded_preprocessor.transform(input_df)
    prediction = loaded_model.predict(df)

    # Format response
    response = {"prediction": prediction.tolist()[0]}
    return response

@app.get("/preview", tags=["Preview"])
async def preview(rows: int):
    """ Give a preview of the dataset : Input the number of rows"""
    data = pd.read_csv('df_price_clean.csv')
    preview = data.head(rows)
    return preview.to_dict()

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000, debug=True, reload=True)