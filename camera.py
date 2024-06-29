import cv2

def main():
    # Open a connection to the camera
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Frame counter
    frame_count = 0

    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Failed to capture image")
            break
        
        # Convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Display the resulting frame
        cv2.imshow('Gray Camera Feed', gray_frame)
        
        # Save frame as an image file when 's' is pressed
        if cv2.waitKey(1) & 0xFF == ord('s'):
            frame_count += 1
            image_filename = f'captured_image_{frame_count}.png'
            cv2.imwrite(image_filename, frame)
            print(f"Image saved as {image_filename}")
        
        # Press 'q' to exit the camera feed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
