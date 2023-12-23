# bottles_classification_CNN
The project aims to develop an automated system of bottles and cups recycling using a Convolutional Neural Network (CNN). The primary goal is to identify and classify bottles and cups in images captured through a camera.

Key Components:

CNN Model:

A Convolutional Neural Network has been implemented using TensorFlow and Keras version 2.15.0.
The model is designed for bottles and cups classification, with convolutional layers for feature extraction and dense layers for classification.
The model is trained on a dataset with labeled images to learn and generalize patterns.

Image Input:

Images are captured using a camera (or loaded from a image file or video file in the case of testing).
accepted extensions are: 
The OpenCV library is used to read and process the images.

Model Inference:

The trained CNN model is utilized to make predictions on the input images.
Predictions include the class of the recognized object and a confidence score.
User Interaction: '.jpeg', '.jpg', '.png', '.bmp'

The system interacts with the user during inference.
If a certain object class is recognized (e.g., a bottle), the program pauses and prompts the user for input.
The user can decide whether to continue processing or stop based on the recognition results.

User Interface (UI):

OpenCV is used to display the video stream with the classification results.
The user can visualize the recognition outcomes in real-time.

Testing:

The code includes testing functionality, such as reading images from files for validation purposes.
The project demonstrates flexibility for both live camera input and image file input.

Extensions:

The system can be extended to include additional object classes by retraining the CNN model on a diverse dataset.
Real-time video processing and deployment on edge devices could be explored for practical applications.

Note:

Please ensure that the paths to the model file (Model/Model.h5) and label file (Model/labels.txt) are correctly specified for proper execution.
This project lays the foundation for a versatile image classification system, with potential applications in various domains such as recycling bottles.
