# Wind power forecasting

## Statistical models

In this repository I am applying traditional statistical/econometric time series models for the purpose of forecasting 
future wind power. Specifically, I am focusing on ARIMA type models, starting with an AR (Autoregressive) model.

I am using data of offshore wind power in Belgium, obtained from OpenDataElia: 
https://opendata.elia.be/explore/dataset/ods086/information/ (1). 
This data is available from 2014/12/31, and is on 15 minute frequency. 
I store the obtained data in a local MySQL database.

Training an AR(p) model is done by:
```python
python3.11 -m apps.statistics.ar_model_fitting
```
which retrieves all of the available data from the MySQL database (DB) and trains an AR(p) model 
class instance on it, saving it into a pickle file.

Forecasting is done by:
```python
python3.11 -m apps.statistics.ar_model_forecasting
```
which uses the trained model class from a pickle file to produce an AR(p) model forecast 
on the latest data obtained from the DB.

## Automatic forecasting

To obtain the newest data of offshore wind power I use
```python
python3.11 -m apps.data.data_fetcher
```
which fetches the data from (1) and uploads it to the local database.

Automatic forecasting is done by making a cron job running every minute, running the script
```bash
bash_scripts.auto_ar_model_forecasting_bash.sh
```
which activates the python virtual environment and runs the script
```python
automatic_ar_model_forecasting.py
```
This script uses functions from `data_fetcher.py` and `ar_model_forecasting.py` to make new forecasts once 
every 15 minutes, when new data is uploaded.