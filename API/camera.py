import cv2 
#launch camera 
cap = cv2.VideoCapture(0)

while True: 
    ret, img = cap.read()
        
    cv2.imshow("Original Image", img)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
