from flask import Flask, Response
import cv2
import time

app = Flask(__name__)
video_path = "video.mp4"  # Updated video file path.


def simulate_camera_capture(video_path, resolution=(800, 600), jpeg_quality=80):
    """Simulates camera capture and returns a JPEG encoded frame."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return None
    frame_resized = cv2.resize(frame, resolution)
    ret, jpeg_frame = cv2.imencode('.jpg', frame_resized, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
    if not ret:
        return None
    return jpeg_frame.tobytes()

def generate_frames():
    while True:
        jpeg_frame = simulate_camera_capture(video_path)
        if jpeg_frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg_frame + b'\r\n')
        time.sleep(0.1)  # simulate frame rate.

@app.route('/stream')
def stream():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
