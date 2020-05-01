"""
Prepare data from webminer.py to analyze and create prediction model.
"""

import re
import logging
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score


class Collector:
    """
    Collect data from webminer.py and prepare neural network model.

    Methods:
        collect()
        prepare_algorithm()
        algorithm()
        data_preparation()

    Variables:
        input_data -> data extracted from website by webminer.py.
        cars_data -> data frame created based on input_data.
        car_brand_name -> name of a car brand passed in webminer.py.
        car_vehicle_name -> name of a vehicle passed in webminer.py.
        model -> created neural network model.
        scaler -> data scaler created with use of MinMaxScaler().

    """
    def __init__(self,
                 input_data=None,
                 cars_data=None,
                 car_brand_name=None,
                 car_vehicle_name=None,
                 model=None,
                 scaler=None):

        self.input_data = input_data
        self.cars_data = cars_data
        self.car_brand_name = car_brand_name
        self.car_vehicle_name = car_vehicle_name
        self.model = model
        self.scaler = scaler

    def collect(self):
        """
        Extract data from input_data to dictionary cars_datadict
        which is transforming to data frame cars_data.
        """

        # Variables to extract.

        year_list = []
        mileage_list = []
        capacity_list = []
        fuel_list = []
        region_list = []
        price_list = []

        # Regular expressions used to extract values.

        km_cm3 = re.compile(r'(\d\d\d\d) (\d*)(\s*)(\d*) km (\d*)(\s*)(\d*) cm3 (.*)')
        pln = re.compile(r'(\d*) (\d*)')

        # Extract data based on regular expressions.

        for extract_offer in Collector.input_data:
            for feat in extract_offer:
                if 'km' and 'cm3' in feat:
                    match_km_cm3 = km_cm3.search(feat)
                    year_list.append(int(match_km_cm3.group(1)))
                    mileage_list.append(int(match_km_cm3.group(2)
                                            + match_km_cm3.group(4)))
                    capacity_list.append(int(match_km_cm3.group(5)+match_km_cm3.group(7)))
                    fuel_list.append(match_km_cm3.group(8))

                elif 'PLN' in feat:
                    match_pln = pln.search(feat)
                    price_list.append(int(match_pln.group(1)
                                          + match_pln.group(2)))

                elif feat[0] is '(' and feat[-1] is ')' and feat[-4:-1] == 'kie':
                    region_list.append(feat[1:-1])

                else:
                    pass

            # Check row completeness.
            # If row is not complete it is filled with None value.

            if (len(year_list)
                    == len(mileage_list)
                    == len(capacity_list)
                    == len(fuel_list)
                    == len(region_list)
                    == len(price_list)):
                pass

            else:
                max_elements = max(len(year_list), len(mileage_list),
                                   len(capacity_list), len(fuel_list),
                                   len(region_list), len(price_list))

                for list_element in [year_list, mileage_list,
                                     capacity_list, fuel_list,
                                     region_list, price_list]:
                    if len(list_element) < max_elements:
                        list_element.append(None)

        # Pass data to dictionary and than to dictionary with data to data frame.

        cars_datadict = {'Brand': [Collector.car_brand_name]*len(Collector.input_data),
                         'Vehicle': [Collector.car_vehicle_name]*len(Collector.input_data),
                         'Year': year_list, 'Mileage': mileage_list,
                         'Capacity': capacity_list, 'Fuel': fuel_list,
                         'Price': price_list}

        Collector.cars_data = pd.DataFrame(data=cars_datadict)

    def prepare_algorithm(self):
        """
        Execute following methods:
            Collector.data_preparation,
            Collector.algorithm.
        """
        Collector.data_preparation(self)
        Collector.algorithm(self)

    def algorithm(self):
        """
        Create predict algorithm for car price.
        """

        # Prepare data sets to create model.

        x = Collector.cars_data.drop(['Price', 'Brand', 'Vehicle'], axis=1).values
        y = Collector.cars_data['Price'].values
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=101)

        # Scale data.

        Collector.scaler = MinMaxScaler()
        x_train = Collector.scaler.fit_transform(x_train)
        x_test = Collector.scaler.transform(x_test)

        # Create neural network model.

        Collector.model = Sequential()
        Collector.model.add(Dense(5, activation='relu'))
        Collector.model.add(Dense(5, activation='relu'))
        Collector.model.add(Dense(5, activation='relu'))
        Collector.model.add(Dense(5, activation='relu'))
        Collector.model.add(Dense(5, activation='relu'))
        Collector.model.add(Dense(5, activation='relu'))
        Collector.model.add(Dense(1))
        Collector.model.compile(optimizer='adam', loss='mse')

        Collector.model.fit(x=x_train,
                            y=y_train,
                            validation_data=(x_test, y_test),
                            epochs=2000, verbose=1)

        # Code below can be used to check predictions quality of created neural network.

        # losses = pd.DataFrame(Collector.model.history.history)
        # losses[['loss', 'val_loss']].plot()
        # plt.show()

        # predictions = Collector.model.predict(x_test)

        # print("""
        # Summary of model effectiveness:
        # Real prices mean: {0}
        # Real prices median: {1}
        # Mean absolute error: {2}
        # Mean squared error: {3}
        # Explained variance score: {4}
        # """.format(Collector.cars_data['Price'].mean(),
        #           Collector.cars_data['Price'].median(),
        #           mean_absolute_error(y_test, predictions),
        #           np.sqrt(mean_squared_error(y_test, predictions)),
        #           explained_variance_score(y_test, predictions)))

    def data_preparation(self):
        """
        Drop N/A values and create dummy variables.
        """
        Collector.cars_data.dropna(inplace=True)
        categorical_variables = ['Fuel']
        Collector.cars_data = pd.get_dummies(Collector.cars_data,
                                             columns=categorical_variables,
                                             drop_first=True)


class Calculate:
    """
    Calculate car price based on created model and new data.

    Methods:
        prepare()
        predict()

    Variables:
        year_calc -> Given year of car production.
        mileage_calc -> Given car mileage.
        capacity_calc -> Given car capacity.
        fuel_calc -> Fuel type.
        single_car -> Data frame with data which will be used to predict
        car price.
        predicted_price -> Predicted car price.
    """
    def __init__(self,
                 year_calc=None,
                 mileage_calc=None,
                 capacity_calc=None,
                 fuel_calc=None,
                 single_car=None,
                 predicted_price=None):

        self.year_calc = year_calc
        self.mileage_calc = mileage_calc
        self.capacity_calc = capacity_calc
        self.fuel_calc = fuel_calc
        self.single_car = single_car
        self.predicted_price = predicted_price

    def prepare(self, dict_benlpg=0, dict_diesel=0):
        """
        Prepare data frame with data which will be used to predict
        car price.
        """
        if Calculate.fuel_calc == 'Benzyna':
            pass
        elif Calculate.fuel_calc == 'Diesel':
            dict_diesel = 1
        else:
            dict_benlpg = 1

        dict_calc = {'Year': Calculate.year_calc,
                     'Mileage': Calculate.mileage_calc,
                     'Capacity': Calculate.capacity_calc,
                     'Fuel_Benzyna+LPG': dict_benlpg,
                     'Fuel_Diesel': dict_diesel}

        self.single_car = pd.DataFrame(data=dict_calc, index=[0])

    def predict(self):
        """
        Predict car price.
        """
        fuel = ['Fuel_Benzyna+LPG', 'Fuel_Diesel']
        self.single_car[fuel] = self.single_car[fuel].astype('uint8')

        self.single_car = Collector.scaler.transform(
            self.single_car.values.reshape(-1, 5))

        Calculate.predicted_price = int(Collector.model.predict(self.single_car))


def export_to_csv(self, path):
    """
    Export extracted from website data to .csv file.
    """
    Collector.cars_data.to_csv(path, sep=",")


def execute_prediction(self):
    """
    Start execution of Calculate.prepare and Calculate.predict.
    """
    Calculate.prepare(self)
    Calculate.predict(self)
