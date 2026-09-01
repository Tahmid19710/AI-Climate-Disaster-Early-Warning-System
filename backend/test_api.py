import requests


url = "http://127.0.0.1:5000/predict_climate"


data = {

    "MonsoonIntensity":5,
    "TopographyDrainage":5,
    "RiverManagement":5,
    "Deforestation":5,
    "Urbanization":5,
    "ClimateChange":5,
    "DamsQuality":5,
    "Siltation":5,
    "AgriculturalPractices":5,
    "Encroachments":5,
    "IneffectiveDisasterPreparedness":5,
    "DrainageSystems":5,
    "CoastalVulnerability":5,
    "Landslides":5,
    "Watersheds":5,
    "DeterioratingInfrastructure":5,
    "PopulationScore":5,
    "WetlandLoss":5,
    "InadequatePlanning":5,
    "PoliticalFactors":5

}


response = requests.post(
    url,
    json=data
)


print("Status Code:")
print(response.status_code)


print("\nResponse:")
print(response.text)