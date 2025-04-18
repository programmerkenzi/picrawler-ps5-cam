import cv2
from datetime import datetime
from picamera2 import Picamera2
from shared.state import joy_status, recording, show_camera


def camera_stream():
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (640, 480)
    picam2.preview_configuration.main.format = "BGR888"
    picam2.configure("preview")
    picam2.start()

    out = None
    window_created = False

    while True:
        image = picam2.capture_array()

        if show_camera:
            cv2.putText(
                image,
                f"X: {joy_status['x']:.2f}  Y: {joy_status['y']:.2f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

            if recording:
                cv2.putText(
                    image,
                    "REC",
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2,
                )

            if not window_created:
                cv2.namedWindow("PiCamera2 Live", cv2.WINDOW_AUTOSIZE)
                window_created = True

            cv2.imshow("PiCamera2 Live", image)
        else:
            if window_created:
                try:
                    if (
                        cv2.getWindowProperty("PiCamera2 Live", cv2.WND_PROP_VISIBLE)
                        >= 1
                    ):
                        cv2.destroyWindow("PiCamera2 Live")
                except:
                    pass
                window_created = False

        if recording:
            if out is None:
                filename = datetime.now().strftime("record_%Y%m%d_%H%M%S.avi")
                out = cv2.VideoWriter(
                    filename, cv2.VideoWriter_fourcc(*"XVID"), 20.0, (640, 480)
                )
            out.write(image)
        elif out:
            out.release()
            out = None

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    if out:
        out.release()
    cv2.destroyAllWindows()
