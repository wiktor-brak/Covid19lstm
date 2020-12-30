# Imports

import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from keras.preprocessing.sequence import TimeseriesGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM


import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import datetime

url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
df = pd.read_csv(url)


class Predict:

    def __init__(self, df, input, feature):
        self.df = df
        self.n_input = input
        self.n_feature = feature
        self.scaler = MinMaxScaler()
        self.test_predictions = []

    def setLocation(self, location):
        self.df = self.df[self.df.location == location]


    def preprocess(self):
        self.df = self.df.reset_index()
        self.df = self.df.drop(self.df.columns.difference(['date', 'new_cases']), axis=1)
        self.df = self.df.fillna(0.)
        self.df.drop(self.df.tail(1).index, inplace=True)

    def addDate(self, numberOfDays):
        for nDays in range(0, numberOfDays):
            nextDay = datetime.datetime.today() + datetime.timedelta(days=nDays)
            self.df = self.df.append({'date': nextDay.date(), 'new_cases': None}, ignore_index=True)
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df = self.df.set_index('date')

    def split(self):
        train = self.df.iloc[:-7]
        test = self.df.iloc[-7:]
        return train, test

    def scale(self, train):
        self.scaler.fit(train)
        scaled_train = self.scaler.transform(train)
        return scaled_train

    def generator(self, scaled_train):
        return TimeseriesGenerator(scaled_train, scaled_train, length=self.n_input, batch_size=1)

    def predictionModel(self):
        model = Sequential()
        model.add(LSTM(256, activation='relu', input_shape=(self.n_input, self.n_feature), return_sequences=True))
        model.add(LSTM(128, activation='relu', dropout=0.1, recurrent_dropout=0.5, return_sequences=True))
        model.add(LSTM(64, activation='relu', dropout=0.1, recurrent_dropout=0.5, return_sequences=True))
        model.add(LSTM(32, activation='relu', return_sequences=False))
        model.add(Dense(1))
        model.compile(optimizer='rmsprop', loss='mae')
        return model

    def predictFuture(self):

        first_eval_batch = scaled_train[-self.n_input:]
        current_batch = first_eval_batch.reshape((1, self.n_input, self.n_feature))

        for i in range(len(test)):
            current_pred = model.predict(current_batch)[0]
            self.test_predictions.append(current_pred)
            current_batch = np.append(current_batch[:, 1:, :], [[current_pred]], axis=1)

        return self.test_predictions


predict = Predict(df, 7, 1)
predict.setLocation('Poland')
predict.preprocess()
predict.addDate(7)
train, test = predict.split()
scaled_train = predict.scale(train)
train_generator = predict.generator(scaled_train)
model = predict.predictionModel()
model.fit(train_generator, epochs=5)
test_predictions = predict.predictFuture()
true_predictions = predict.scaler.inverse_transform(test_predictions)
test['Predictions'] = true_predictions

plot_data = [
    go.Scatter(
        x=predict.df.index,
        y=predict.df.new_cases,
        name='Actual'
    ),
    go.Scatter(
        x=test.index,
        y=test['Predictions'],
        name='Predicted future days'
    )

]

plot_layout = go.Layout(
    title='Model prediction for COVID-19 expansion with Long short-term memory algorithm',
    height=700
)

# fig = go.Figure(data=plot_data, layout=plot_layout)
# fig.show()

layout = html.Div(
    [

        html.H4(
            children='COVID-19 Prediction',
            style={
                'marginTop': 20,
                'marginBottom': 30,
                'textAlign': 'center'
            }
        ),

        dbc.Row(dbc.Col(html.Div(
            dcc.Graph(
                id='example-graph',
                figure=fig
            )

        )))

    ]
)
