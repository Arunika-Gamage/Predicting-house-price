
"""Predicting House Price using Linear Regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15fJaa8D7ZZnQ0df4vf2r4ETg2uiKdQxU

Importing libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline
import numpy as np

#read in the data with read_csv() into a pandas dataframe
housing_df = pd.read_csv('housing.csv')

#use .info() to show the feature in your dataset along with a count and datatype
housing_df.info()

"""Data visualizations to see relationship of the target variable with other features"""

#plot teh distribution of the target variable using a histogram
#bins = amount of columns

plt.hist(housing_df['median_house_value'], bins=80)
plt.xlabel("House values")

housing_df.hist(bins=50, figsize=(15,8))

"""Using a heatmap to show correlation"""

corr = housing_df.corr() # data frame correlation function
print(corr)

plt.figure(figsize=(5,5))
sns.heatmap(corr, annot=True)
plt.show()

"""## **Prepare and Preprocess data**

Finding missing data
"""

#verify which features have missing values
housing_df.isnull().sum()

#calculate the percentage of the missing data
housing_df['total_bedrooms'].isnull().sum()/housing_df.shape[0]*100

"""impute missing data using machine learning"""

from sklearn.impute import KNNImputer

#create a temporary copy of the dataset
housing_df_temp = housing_df.copy()

#retrieve columns with numerical data: will exclude the ocean-proximity column since the datatype is objetc
columns_list = [col for col in housing_df_temp.columns if housing_df_temp[col].dtype!='object']

#extract columns that contain at least one missing valus
new_column_list = [col for col in housing_df_temp.loc[:, housing_df_temp.isnull().any()]]

#update temp dataframe with numeric columns that have empty values
housing_df_temp = housing_df_temp[new_column_list]

#initialize knnimputer to impute missing data using ml
knn = KNNImputer(n_neighbors = 3)

#fit function trains the model
knn.fit(housing_df_temp)

#transform the dta using the model
#applies the transformation model(ie; knn) to data
array_Values = knn.transform(housing_df_temp)

#convert the array values to a dataframe with the approriate column names
housing_df_temp = pd.DataFrame(array_Values, columns = new_column_list)

"""Feature Engineering"""

# a new feature that is a ratio of the total rooms to households
housing_df['rooms_per_household'] = housing_df['total_rooms']/housing_df['households']

# a new feature that is a ratio of the total bedrooms to total rooms
housing_df['bedrooms_per_rooms'] = housing_df['total_bedrooms']/housing_df['total_rooms']

# a new feature that is a ratio of the population to households
housing_df['population_per_household'] = housing_df['population']/housing_df['households']

# a new feature that is a ratio of the total rooms to households
housing_df['coords'] = housing_df['longitude']/housing_df['latitude']

housing_df.info()

#remove those features
housing_df = housing_df.drop('total_rooms', axis=1)
housing_df = housing_df.drop('households', axis=1)
housing_df = housing_df.drop('total_bedrooms', axis=1)
housing_df = housing_df.drop('population', axis=1)
housing_df = housing_df.drop('longitude', axis=1)
housing_df = housing_df.drop('latitude', axis=1)

housing_df.info()

"""Heatmap after removing correlation"""

corr = housing_df.corr()
plt.figure(figsize=(5,5))
sns.heatmap(corr, annot=True)
plt.show()

"""ENCODING CATEGORICAL DATA"""

#unique categories of ocean
housing_df.ocean_proximity.unique()

housing_df["ocean_proximity"].value_counts()

print(pd.get_dummies(housing_df['ocean_proximity']))

#replace the ocean_proximity column using get_dummies()
h_df_encodeed = pd.get_dummies(data= housing_df, columns=['ocean_proximity'])
