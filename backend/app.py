from flask import Flask, request, jsonify
from flask_cors import CORS

import tensorflow as tf
import xgboost as xgb

import numpy as np
from PIL import Image

import json
import os


app = Flask(__name__)

CORS(app, resources={
    r"/*":{
        "origins":"*"
    }
})


# =========================
# Paths
# =========================

IMAGE_MODEL_PATH = "models/flood_detection_mobilenetv2.keras"
CLIMATE_MODEL_PATH = "models/flood_model.json"
CONFIG_PATH = "models/config.json"


# =========================
# Load MobileNetV2
# =========================

image_model = tf.keras.models.load_model(
    IMAGE_MODEL_PATH
)

print("MobileNetV2 Loaded")


# =========================
# Load Config
# =========================

with open(CONFIG_PATH) as f:
    config = json.load(f)


IMAGE_SIZE = config.get(
    "image_size",
    224
)

THRESHOLD = config.get(
    "threshold",
    0.40
)


print("Config Loaded")


# =========================
# Load XGBoost
# =========================

climate_model = xgb.XGBRegressor()

climate_model.load_model(
    CLIMATE_MODEL_PATH
)


print("XGBoost Loaded")



# =========================
# Image Preprocessing
# =========================

def preprocess_image(path):

    img = Image.open(path)

    img = img.convert("RGB")

    img = img.resize(
        (IMAGE_SIZE, IMAGE_SIZE)
    )


    img = np.array(img)

    img = img / 255.0


    img = np.expand_dims(
        img,
        axis=0
    )


    return img




# =========================
# Climate Features
# =========================

def get_climate_features(data):

    features = [

        "MonsoonIntensity",
        "TopographyDrainage",
        "RiverManagement",
        "Deforestation",
        "Urbanization",
        "ClimateChange",
        "DamsQuality",
        "Siltation",
        "AgriculturalPractices",
        "Encroachments",
        "IneffectiveDisasterPreparedness",
        "DrainageSystems",
        "CoastalVulnerability",
        "Landslides",
        "Watersheds",
        "DeterioratingInfrastructure",
        "PopulationScore",
        "WetlandLoss",
        "InadequatePlanning",
        "PoliticalFactors"

    ]


    return [

        float(data[x])

        for x in features

    ]




# =========================
# Combined Prediction
# =========================


@app.route(
    "/final_prediction",
    methods=["POST"]
)
def final_prediction():


    print("\n========== FINAL API CALLED ==========")


    print("FILES:")
    print(request.files)


    print("\nFORM DATA:")
    print(request.form)



    # Check image received

    if "image" not in request.files:

        return jsonify({

            "error":"Image not received"

        }),400



    print("\nImage received successfully")



    file = request.files["image"]



    image_path = "uploads/" + file.filename



    file.save(image_path)



    print("Image saved:", image_path)



    # Image prediction

    img = preprocess_image(
        image_path
    )


    image_score = image_model.predict(
        img
    )[0][0]


    print(
        "Image Score:",
        image_score
    )



    # Climate prediction

    climate_data = request.form.to_dict()



    print(
        "Climate Data:",
        climate_data
    )



    climate_features = get_climate_features(
        climate_data
    )



    climate_score = climate_model.predict(

        np.array(climate_features).reshape(1,-1)

    )[0]



    print(
        "Climate Score:",
        climate_score
    )



    # Combine score

    final_score = (

        float(image_score)*0.6

        +

        float(climate_score)*0.4

    )



    print(
        "Final Score:",
        final_score
    )



    if final_score >= 0.7:

        warning = "HIGH FLOOD RISK"


    elif final_score >= 0.4:

        warning = "MEDIUM FLOOD RISK"


    else:

        warning = "LOW FLOOD RISK"




    print(
        "Warning:",
        warning
    )



    print(
        "========== FINAL API END ==========\n"
    )



    return jsonify({


        "image_probability":
        float(image_score),



        "climate_risk":
        float(climate_score),



        "final_score":
        float(final_score),



        "warning":
        warning


    })
    # =====================
    # IMAGE MODEL
    # =====================


    if "image" not in request.files:

        return jsonify({

            "error":"Image missing"

        }),400



    file = request.files["image"]


    os.makedirs(
        "uploads",
        exist_ok=True
    )


    image_path = (
        "uploads/"
        +
        file.filename
    )


    file.save(image_path)



    img = preprocess_image(
        image_path
    )



    image_score = image_model.predict(
        img
    )[0][0]



    print(
        "Image Score:",
        image_score
    )




    # =====================
    # CLIMATE MODEL
    # =====================


    climate_data = request.form.to_dict()



    climate_features = get_climate_features(
        climate_data
    )


    climate_score = climate_model.predict(

        np.array(
            climate_features
        ).reshape(1,-1)

    )[0]



    print(
        "Climate Score:",
        climate_score
    )




    # =====================
    # FINAL SCORE
    # =====================


    final_score = (

        float(image_score)*0.6

        +

        float(climate_score)*0.4

    )




    if final_score >= 0.7:

        warning="HIGH FLOOD RISK"


    elif final_score >=0.4:

        warning="MEDIUM FLOOD RISK"


    else:

        warning="LOW FLOOD RISK"




    response= {

        "image_probability":
            float(image_score),


        "climate_risk":
            float(climate_score),


        "final_score":
            float(final_score),


        "warning":
            warning
    }
    print("response ",response);
    return jsonify(response);





# =========================
# Home
# =========================


@app.route("/")
def home():

    return "AI Climate Disaster Early Warning System"





if __name__=="__main__":


    os.makedirs(
        "uploads",
        exist_ok=True
    )


    app.run(
        debug=True
    )