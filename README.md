# GeoAIHack_team_18
We are answering the GeoAI Hack challenge at ADP on locust breeding ground segmentation: https://geoaihack.com/ and https://www.kaggle.com/datasets/chaimaboukthir/geo-ai-hack on Kaggle.

## Notebooks
Sarah made this code, using chatgpt, either for colab or kaggle with a DeepLabV3 (evi and ndvi addition in features), the remote sensing image is 6 bands: Blue, green, red, nir, swir1, swir2.

## Competition submission
Kenzo has used a prithvi model (base model from instageo package) in order to make the diverse results with changing batch, epoch and learning_rate and adding bands, ndwi and ndvi.
Stan added new bands to get locust colour areas in order to get the possible breading grounds.
The metric used is AUC.

## Streamlit App
Julian has made the streamlit app with the template provided by InstaDeep competition and modified it to get filter drop downs.
