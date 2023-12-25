from PIL import Image, ImageOps  
import cv2 
import cvzone
import os
import time

def generateImage(nbrImages, output_folder):
    """
    nbrImages: Number of images to capture.
    output_folder: The folder where the captured images will be saved.
    """
    cap = cv2.VideoCapture(0)

    # counter for image generation
    counter = 0

    while counter < nbrImages:
        _,img = cap.read()

        # Get the height and width of the image
        height, width, _ = img.shape

        # Define the dimensions of the rectangle
        rect_width = int(width * 0.45)
        rect_height = int(height * 0.9)

        # Calculate the starting point of the rectangle to keep it centered
        rect_x = (width - rect_width) // 2
        rect_y = (height - rect_height) // 2

        # Draw the centered rectangle on the frame
        cv2.rectangle(img, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (0, 255, 0), 2)

        # Display the frame
        cv2.imshow("Zoomed Image", img)

        # Capture the specified rectangle from the image
        captured_rect = img[rect_y:rect_y + rect_height, rect_x:rect_x + rect_width]
        
        # Create the "DataTest" folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Save the captured image to a file
        image_filename = os.path.join("DataTest", f"captured_image_{time.strftime('%H%M%S')}_{counter}.jpg")
        cv2.imwrite(image_filename, captured_rect)
        counter += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# test the code 
generateImage(10, "DataTest")