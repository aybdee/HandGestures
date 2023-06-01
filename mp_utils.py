import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose


def annotate_hands(cam_feed: np.ndarray):
    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.5,
        # min_tracking_confidence=0.5,
    ) as hands:
        cam_feed.flags.writeable = True
        results = hands.process(cam_feed)

        if results.multi_hand_landmarks:
            print("found landmarks")
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    cam_feed,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style(),
                )


def annotate_body(cam_feed: np.ndarray):
    with mp_pose.Pose(
        static_image_mode=True,
        model_complexity=2,
        enable_segmentation=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as pose:
        cam_feed.flags.writeable = True
        results = pose.process(cam_feed)
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                cam_feed,
                results.pose_landmarks,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
            )
