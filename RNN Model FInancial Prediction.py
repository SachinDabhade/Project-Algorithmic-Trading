import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout


class StockMarketPredictor:
    
    def __init__(self, data_file, training_size=0.8, look_back=60, neurons=50, dropout=0.2, dense_layer=25, epochs=100, batch_size=32):
        self.data_file = data_file
        self.training_size = training_size
        self.look_back = look_back
        self.neurons = neurons
        self.dropout = dropout
        self.dense_layer = dense_layer
        self.epochs = epochs
        self.batch_size = batch_size
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = Sequential()
        
    def load_data(self):
        # Load the dataset
        dataset = pd.read_csv(self.data_file)

        # Extract the 'Close' column for prediction
        self.data = dataset.filter(['Close'])

        # Convert the data to a numpy array
        self.data = self.data.values

        # Set the training data size
        self.training_data_size = int(len(self.data) * self.training_size)

        # Scale the data
        self.scaled_data = self.scaler.fit_transform(self.data)

    def prepare_data(self):
        # Create the training data
        train_data = self.scaled_data[0:self.training_data_size, :]

        # Split the data into x_train and y_train datasets
        x_train = []
        y_train = []

        for i in range(self.look_back, len(train_data)):
            x_train.append(train_data[i-self.look_back:i, 0])
            y_train.append(train_data[i, 0])

        # Convert the x_train and y_train datasets to numpy arrays
        self.x_train, self.y_train = np.array(x_train), np.array(y_train)

        # Reshape the data for LSTM input
        self.x_train = np.reshape(self.x_train, (self.x_train.shape[0], self.x_train.shape[1], 1))

    def build_model(self):
        # Build the LSTM model
        self.model.add(LSTM(self.neurons, return_sequences=True, input_shape=(self.x_train.shape[1], 1)))
        self.model.add(Dropout(self.dropout))
        self.model.add(LSTM(self.neurons, return_sequences=False))
        self.model.add(Dropout(self.dropout))
        self.model.add(Dense(self.dense_layer))
        self.model.add(Dense(1))

        # Compile the model
        self.model.compile(optimizer='adam', loss='mean_squared_error')

    def train_model(self):
        # Train the model
        self.model.fit(self.x_train, self.y_train, batch_size=self.batch_size, epochs=self.epochs)

        # Save the model if specified
        if self.save_model:
            self.model.save('stock_market_predictor_model.h5')		

    def prepare_test_data(self):
        # Create the testing data
        test_data = self.scaled_data[self.training_data_size - self.look_back:, :]

        # Split the data into x_test and y_test datasets
        self.x_test = []
        self.y_test = self.data[self.training_data_size:, :]

        for i in range(self.look_back, len(test_data)):
            self.x_test.append(test_data[i-self.look_back:i, 0])

        # Convert the x_test dataset to a numpy array
        self.x_test = np.array(self.x_test)

        # Reshape the data for LSTM input
        self.x_test = np.reshape(self.x_test, (self.x_test.shape[0], self.x_test
