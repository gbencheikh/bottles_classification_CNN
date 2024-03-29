# import dependencies 
import snap7
import cv2 
import numpy as np 
import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense
from keras.models import Sequential, load_model
import threading
import time 
import os
"------------------------------------------------------"
# connection with PLC 
plc = snap7.client.Client()
try:
    plc.connect("192.168.1.10", 0, 1)
except ValueError:
    print("PLC Error Connection")

# PLC settings 
db_number4 =4
db_number5 =5
db_number8 =8
start_address =0
byte_to_read =1
true_val = 1
bytes_True = true_val.to_bytes(1, 'little') 
DB_value = 0
"------------------------------------------------------"
# load trained model 
model = load_model("Model/Model.h5", compile=False)
class_names = open("Model/labels.txt", "r").readlines()   
proba = 0.8
"------------------------------------------------------"
# utils functions 
def predict(img, fileName):
    """ function to predict the class of an image 
    Input:
        img: input image to classify 

    Returns:
        Tuple: Index of predicted class, Confidence score.
    """
    # make a copy of the image 
    image = img.copy()

    # Get the height and width of the image
    height, width, _ = img.shape

    # Define the dimensions of the rectangle
    rect_width = int(width * 0.45)
    rect_height = int(height * 0.9)

    # Calculate the starting point of the rectangle to keep it centered
    rect_x = (width - rect_width) // 2
    rect_y = (height - rect_height) // 2

    # Capture the specified rectangle from the image
    captured_rect = img[rect_y:rect_y + rect_height, rect_x:rect_x + rect_width]
        
    # Create the "DataTest" folder if it doesn't exist
    os.makedirs("Data_Simulation", exist_ok=True)

    # Save the captured image to a file
    image_filename = os.path.join("Data_Simulation", fileName)
    cv2.imwrite(image_filename, captured_rect)
   
    # resize the image to meet prediction model
    resize = tf.image.resize(image, (256,256))
    np.expand_dims(resize, 0)

    #launch the predicting model 
    prediction = model.predict(np.expand_dims(resize/255, 0))

    # get index of predicted class 
    index = np.argmax(prediction)
    
    # Get the corresponding confidence probability
    confidence_score = prediction[0, index]

    return index, confidence_score

def show_canvas(img, result_text):
    """Display an image into a frame and add results label.

    Args:
        img (numpy.ndarray): Input image.
        result_text (str): Text to display on the image.
    """
    # Get the height and width of the image
    height, width, _ = img.shape

    # create a new canvas
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    canvas[:img.shape[0], :img.shape[1]] = img

    # Get the size of the text
    text_size = cv2.getTextSize(result_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]

    # Calculate the position to center the text
    text_x = (width - text_size[0]) // 2
    text_y = 30

    # Define the dimensions of the rectangle
    rect_width = int(width * 0.45)
    rect_height = int(height * 0.9)

    # Calculate the starting point of the rectangle to keep it centered
    rect_x = (width - rect_width) // 2
    rect_y = (height - rect_height) // 2

    # Draw the centered rectangle on the frame
    cv2.rectangle(canvas, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (0, 255, 0), 2)

    # Display the result
    cv2.putText(canvas, result_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2) 
    cv2.imshow("Image", canvas)

def wait_for_machine_finish():
    """ Wait until the machine has finished working and DB_PLC changed """
    global DB_value
    while working:
        DB_PLC = plc.read_area(snap7.types.Areas.DB,db_number4,start_address,byte_to_read)
        DB_Value=int.from_bytes(DB_PLC, byteorder='big', signed=False)
        if(DB_Value !=0) :
            working=False
"------------------------------------------------------"
# a special thread for waiting machine finish function  
file_lock = threading.Lock()

########################### start simulation ###########################
# Check PLC value
DB_PLC = plc.read_area(snap7.types.Areas.DB,db_number4,start_address,byte_to_read)
DB_Value=int.from_bytes(DB_PLC, byteorder='big', signed=False)
wait_for_machine_finish()

def main():
    #launch camera 
    cap = cv2.VideoCapture(0)

    # Start a separate thread for reading the file
    wait_thread = threading.Thread(target=wait_for_machine_finish)
    wait_thread.daemon = True
    wait_thread.start()

    while True:
        counter = 0
        list_index = []
        list_confidence = []

        while counter < 10:
            # Add a small delay to allow OpenCV to update the window
            cv2.waitKey(1)
            ret, img = cap.read()
            cv2.imshow("Original Image", img)
            
            fileName = f"image_{time.strftime('%H%M%S')}_{counter}.jpg"

            index, confidence_score = predict(img, fileName)

            # Write results to a file
            file_name = "simulation_results.txt"
            with open(file_name, "a") as file:
                file.write(f"{fileName};{index};{confidence_score}\n")

            counter += 1

            list_index.append(index)
            list_confidence.append(confidence_score)
               
        confidence_score = max(list_confidence)
        index = list_index[list_confidence.index(confidence_score)]
                
        if index != 0:
            # if the machine is not empty!
            if confidence_score > proba:
                """ if program recognizes bottle """
                # Open Accepted Gate
                writing = plc.write_area(snap7.types.Areas.DB,db_number8,start_address,bytes_True)

                with file_lock:
                    value_to_display = DB_value

                show_canvas(img, f"Class: {class_names[index]}")
                
            else:
                # Open Rejected Gate
                writing = plc.write_area(snap7.types.Areas.DB,db_number5,start_address,bytes_True)

                with file_lock:
                    value_to_display = DB_value
                    
                show_canvas(img, "Unkown object")

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
