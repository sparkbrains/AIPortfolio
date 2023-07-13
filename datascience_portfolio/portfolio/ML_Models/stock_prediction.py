
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima
from statsmodels.tsa.stattools import adfuller
import plotly.graph_objects as go
import warnings
import plotly.io as pio
import seaborn as sns
from django.conf import settings
import os

def predict_stock_prices(path, plot_image_name,n_periods):
    try:
        new_data = pd.read_csv(path)    
        warnings.filterwarnings("ignore")
        df = new_data.copy()
        df.columns = map(str.lower, df.columns)
        df.dropna(inplace=True)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date')
        data= df.copy()
        data = data['close']
        result = adfuller(data)
        p_value = result[1]
        stationary = 0 if p_value < 0.05 else 1
        if stationary == 1:
            transformed_data = np.log(data)
        else:
            transformed_data = data
        model = auto_arima(transformed_data, D=12, start_p=1, start_d=1, start_q=1, max_p=3, max_d=3, max_q=7)

        last_date = df['date'].iloc[-1]
        future_dates = pd.date_range(start=last_date, periods=n_periods + 1)[1:]
        predicted_values = model.predict(n_periods=n_periods)
        predicted_df = pd.DataFrame({'date': future_dates, 'predicted': predicted_values})
        sns_data = pd.DataFrame({'date': predicted_df['date'], 'predicted': predicted_df['predicted']})
        final_data  = sns_data.values.tolist()
        plt.figure(figsize=(10, 10))  # Adjust the values as per your requirement

        sns.lineplot(x='date', y='predicted', data=sns_data)

        plt.title('Predicted Stocks')
        plt.xlabel('Date')
        plt.ylabel('Stocks')
        plt.xticks(rotation=90)
        plt.savefig(os.path.join(settings.BASE_DIR,settings.GRAPH_SAVING_PATH)+plot_image_name)
        plt.show()    
        return final_data
    except:
        pass


