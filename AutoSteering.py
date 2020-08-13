import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D
import cv2

# Load CSV file
img_file = pd.read_csv("Lane_Data.csv")
# Prep Data
x = []
y = np.array(img_file["JoystickX"])
# Load all images and add it to x
img_urls = np.array(img_file["img_url"])
count = 0
for url in img_urls:
    if count > 100:
        break
    print("Loading image with url: " + url)
    loaded_image = cv2.imread(url)
    loaded_image = cv2.cvtColor(loaded_image, cv2.COLOR_BGR2GRAY)
    x.append(loaded_image)
    count += 1
x = np.asarray(x)
x = x.reshape(len(x), 425, 720, 1)
print("Data is loaded, creating model...")
print(len(x))
print(len(x[0]))
print(len(x[0][0]))
print(len(x[0][0][0]))

steering_model = Sequential()
steering_model.add(Conv2D(32, activation='relu', kernel_size=3, input_shape=(425, 720, 1)))
steering_model.add(Conv2D(64, activation='relu', kernel_size=3))
steering_model.add(Conv2D(128, activation='relu', kernel_size=3))
steering_model.add(Conv2D(256, activation='relu', kernel_size=3))
steering_model.add(Flatten())
steering_model.add(Dense(32, activation="sigmoid"))
steering_model.add(Dense(16, activation="sigmoid"))

steering_model.compile(loss="mean_squared_error", optimizer="adam", metrics="mean_squared_error")
steering_model.fit(x, y, batch_size=5, epochs=5, validation_split=0.2)
