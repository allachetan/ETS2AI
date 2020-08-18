# ETS2AI
A Neural Network that takes a grayscale image as input and outputs joystick x values to attemt to keep the truck in the game Euro Truck Simulator 2 within its lane. It uses a combination of Convolutional, Max Pooling, Flattening, and Dense layers.

Data Collection:
- The data is collected using my DataColector.py. It records my screen and joystick inputs while I play the game.
- It uses mss and pygame to record the data and cv2 to format it.
- Pandas stores the urls of the image and the joystick inputs into the csv file. Images are not stored in the csv since the file would be very large and the program would run too slow. 
