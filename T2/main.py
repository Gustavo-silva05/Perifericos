import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose

mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose()


captura = cv2.VideoCapture(0)


while captura.isOpened():

    _, imagem = captura.read()

    imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    

    resultado = pose.process(imagem_rgb)

    if resultado.pose_landmarks:

        mp_drawing.draw_landmarks(imagem, resultado.pose_landmarks, mp_pose.POSE_CONNECTIONS)


    cv2.imshow('MediaPipe Pose', imagem)

    if cv2.waitKey(1) & 0xFF == ord('a'):

        break


captura.release()

cv2.destroyAllWindows()