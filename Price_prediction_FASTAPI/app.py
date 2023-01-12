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
Get Around API suggest you the optimum prices for rental cars. 
The goal of this api is to provide predictions based in a machine learning model taking data about the car as input
in order to help management team to deicde a pricing for car rental. 


## Machine-Learning 

Where you can:
* `/predict` if one person is likely to quit the company
* `/batch-predict` where you can upload a file to get predictions for several employees


Check out documentation for more information on each endpoint. 
"""

tags_metadata = [
    {
        "name": "Categorical",
        "description": "Endpoints that deal with categorical data",
    },

    {
        "name": "Numerical",
        "description": "Endpoints that deal with numerical data"
    },

    {
        "name": "Preview",
        "description": "Endpoints that quickly explore dataset"
    },

    {
        "name": "Predictions",
        "description": "Endpoints that uses our Machine Learning model to suggest car pricing"
    }
]

app = FastAPI(
    title="Get Around API",
    description=description,
    version="0.1",
    contact={
        "name": "Sutz Florian",
        "url": "Mettre URL streamlit app?",
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


@app.get("/test")
async def test():
    return 'Test ok'


@app.post("/predict", tags=["Machine-Learning"])
async def predict(new_line: PredictionFeatures):
    """
    Prediction for one observation. Endpoint will return a dictionnary like this:

    ```
    {'prediction': PREDICTION_VALUE[0,1]}
    ```

    You need to give this endpoint all columns values as dictionnary, or form data.
    """
    # Read data 
    new_line = dict(new_line)
    input_df = pd.DataFrame(columns=['model_key', 'mileage', 'engine_power', 'fuel', 'paint_color','car_type', 'private_parking_available', 'has_gps',
       'has_air_conditioning', 'automatic_car', 'has_getaround_connect','has_speed_regulator', 'winter_tires'])
    input_df.loc[0] = list(new_line.values())
    # df = pd.DataFrame(dict(new_line), index=[0])
    
    # Will output in console when new data is received by the endpoint
    print("The /predict endpoint received a new line :")
    # print(df)


    # Load model & predict
    # loaded_model = joblib.load('Model_final.pkl')
    loaded_model = xgboost.XGBRegressor()
    loaded_model.load_model('model_final.json')
    loaded_preprocessor = joblib.load('preprocessor.pkl')
    df = loaded_preprocessor.transform(input_df)
    prediction = loaded_model.predict(df)

    # Format response
    response = {"prediction": prediction.tolist()[0]}
    return response

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000, debug=True, reload=True)