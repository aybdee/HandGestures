import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


def get_hands():
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
        static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5
    ) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("skip empty camera frame")
            else:
                # pass by reference to boost performance
                image.flags.writeable = True
                results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style(),
                        )

                cv2.imshow("Mediapipe Hands", cv2.flip(image, 1))
                # wait for kill signal
                if cv2.waitKey(5) and 0xFF == 27:
                    cv2.destroyAllWindows()
                    break

    cap.release()


get_hands()
