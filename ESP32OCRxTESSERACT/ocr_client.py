import cv2
import urllib.request
import numpy as np
import pytesseract
import time # Import time for delays

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Cj Parame\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# --- CRITICAL CHANGE ---
# Point this URL to your *simulated* server
url = 'http://127.0.0.1:5000/jpg' # Use 127.0.0.1 or localhost
# If server runs on 0.0.0.0 and client is on same machine, 127.0.0.1 is fine.
# If client is on a different machine, use the server machine's actual IP address.



print(f"Attempting to connect to simulated server at: {url}")
print("Ensure the simulate_esp32_server.py script is running.")

while True:
    try:
        # 1. Fetch JPEG data from simulated server
        img_resp = urllib.request.urlopen(url, timeout=5) # Added timeout

        # 2. Convert it to a NumPy array
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)

        # 3. Decode it into an OpenCV image
        # cv2.IMREAD_COLOR is default, -1 includes alpha channel if present
        frame = cv2.imdecode(imgnp, cv2.IMREAD_COLOR)

        if frame is None:
            print("Failed to decode image. Skipping frame.")
            time.sleep(1) # Wait a bit before retrying
            continue

        # --- OCR Implementation ---
        # Optional: Pre-processing (Example: convert to grayscale)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Optional: Apply thresholding etc. if needed for better OCR
        # _, thresh_frame = cv2.threshold(gray_frame, 150, 255, cv2.THRESH_BINARY)

        # 1. Extracts text using Tesseract (using gray frame often works better)
        # --psm 6: Assume a single uniform block of text. Adjust as needed.
        # See Tesseract docs for different PSM modes.
        text = pytesseract.image_to_string(gray_frame, config='--psm 6')
        text = text.strip() # Remove leading/trailing whitespace

        print(f"Detected Text: '{text}'")

        # 2. Overlays the detected text on the original color video stream
        # Use a bounding box or just put text at the top
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('OCR Stream (Simulated)', frame)

        # --- Wait for key press ---
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): # Press 'q' to quit
            break
        elif key == ord(' '): # Press 'space' to pause/resume (optional)
             print("Paused. Press space again to resume.")
             while True:
                 key2 = cv2.waitKey(0) & 0xFF
                 if key2 == ord(' '):
                     print("Resumed.")
                     break
                 elif key2 == ord('q'):
                    key = key2 # Pass 'q' to outer loop
                    break
             if key == ord('q'):
                 break


    except urllib.error.URLError as e:
        print(f"Error connecting to server or fetching image: {e}")
        print("Is the simulated server script running?")
        time.sleep(2) # Wait before retrying connection
    except cv2.error as e:
        print(f"OpenCV Error: {e}")
        time.sleep(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        time.sleep(1) # Wait a bit before retrying

# Clean up
cv2.destroyAllWindows()
print("Client stopped.")
