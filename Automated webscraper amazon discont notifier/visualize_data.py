import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb

# Function to visualize the train test
def plot_train_test_split(train_df, test_df, index):
    fig, ax = plt.subplots(figsize=(15, 5))
    train_df.plot(ax=ax, label="Training Set")
    test_df.plot(ax=ax, label="Test Set")
    ax.grid(True)
    ax.axvline(index, color='black', ls="--")
    plt.show()

def create_features(df):
    """
    Create features based on timeseries index
    """
    df['hour'] = df.index.hour
    df['minute'] = df.index.minute
    df['second'] = df.index.second
    return df


color_pal = sns.color_palette()
df = pd.read_csv('amazon_ringcam.csv')
df = df.drop(columns=['Rating','Title', 'Date'])

# Convert the "Time" column to a datetime type
df['Time'] = pd.to_datetime(df['Time'])

# Set the "Time" column as the index
df.set_index("Time", inplace=True)

# Sort the DataFrame by the datetime index (if not already sorted)
df.sort_index(inplace=True)

# Check for and handle missing data if necessary

# Plot the time series data
#plot_df(df, "Time", "Price", "Amazon Ringcam Prices")

# Split into train and test sets (you can adjust the split index as needed)
train = df.loc[df.index < '2023-09-29 02:50:27']
test = df.loc[df.index >= '2023-09-29 02:50:27']

# Visualize the train/test split
# plot_train_test_split(train, test, '2023-09-29 02:50:27')

df = create_features(df)

# ?Create our model

train = create_features(train)
test = create_features(test)

Features = ["hour", "minute", "second"]
Target = "Price"

X_train = train[Features]
y_train = train[Target]

X_test = test[Features]
y_test = test[Target]

reg = xgb.XGBRegressor(n_estimators=1000,early_stopping_rounds=50)
reg.fit(X_train, y_train,eval_set=[(X_train, y_train), (X_test, y_test)])

# ?Feature Importance

fi = pd.DataFrame(data=reg.feature_importances_, index=reg.feature_names_in_, columns=['importance'])

fi.sort_values('importance').plot(kind='barh', figsize=(15, 5), title ="Feature Importance")

test['prediction'] = reg.predict(X_test)

df = df.merge(test[['prediction']],how='left', left_index=True, right_index=True)

ax = df[['Price']].plot(figsize=(15,5))
df['prediction'].plot(ax=ax, style='.')
plt.legend(['True data','Predicted data'])
ax.set_title('Raw Data and Predictions')
plt.show()