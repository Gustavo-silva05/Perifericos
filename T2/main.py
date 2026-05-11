import cv2
import mediapipe as mp
import points as pts_module
from exercises import (
    RoscaBiceps,
    Flexao,
    Agachamento,
    Abdominal,
    Salto,
    FlexaoLateralPerna,
)

# ---------------------------------------------------------------------------
# MediaPipe setup
# ---------------------------------------------------------------------------
mp_pose    = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose       = mp_pose.Pose()

# ---------------------------------------------------------------------------
# Exercise selection
# This would be driven by the Qt interface via a parameter / signal.
# For standalone testing, change EXERCICIO_ATIVO here.
#
# Options: "rosca_biceps" | "flexao" | "agachamento" | "abdominal"
#          | "salto" | "flexao_lateral_perna"
# ---------------------------------------------------------------------------
EXERCICIO_ATIVO = "rosca_biceps"

# ---------------------------------------------------------------------------
# Camera capture
# ---------------------------------------------------------------------------
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.read()[0]:
        print(f"Camera found at index {i}")
    cap.release()
_, frame_teste = captura.read()
h_frame, w_frame = frame_teste.shape[:2]

# ---------------------------------------------------------------------------
# Instantiate the active exercise counter
# ---------------------------------------------------------------------------
exercicios = {
    "rosca_biceps":         RoscaBiceps(),
    "flexao":               Flexao(),
    "agachamento":          Agachamento(),
    "abdominal":            Abdominal(),
    "salto":                Salto(altura_frame=h_frame),
    "flexao_lateral_perna": FlexaoLateralPerna(),
}

exercicio = exercicios[EXERCICIO_ATIVO]

# ---------------------------------------------------------------------------
# HUD helpers
# ---------------------------------------------------------------------------
COR_VALIDA   = (0, 255, 0)    # green  — good rep / neutral
COR_INVALIDA = (0, 0, 255)    # red    — bad rep warning
FONTE        = cv2.FONT_HERSHEY_SIMPLEX


def desenhar_hud(imagem, contador, invalidas, rep_invalida, info_valor, meta):
    """
    Draws the rep counter, invalid counter and bad-rep warning on the frame.
    info_valor: angle (degrees) or Y position depending on the exercise.
    """
    cor_borda = COR_INVALIDA if rep_invalida else COR_VALIDA

    # Semi-transparent background panel
    overlay = imagem.copy()
    cv2.rectangle(overlay, (0, 0), (260, 140), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.4, imagem, 0.6, 0, imagem)

    # Rep counter
    cv2.putText(imagem, f"Reps: {contador} / {meta}", (10, 35),
                FONTE, 1.0, cor_borda, 2)

    # Invalid counter
    cv2.putText(imagem, f"Invalidas: {invalidas}", (10, 70),
                FONTE, 0.8, COR_INVALIDA if invalidas > 0 else COR_VALIDA, 2)

    # Angle / info
    cv2.putText(imagem, f"Valor: {info_valor:.1f}", (10, 105),
                FONTE, 0.7, (255, 255, 255), 1)

    # Bad rep warning banner
    if rep_invalida:
        cv2.putText(imagem, "! REP INCOMPLETA !", (w_frame // 2 - 160, h_frame - 20),
                    FONTE, 1.2, COR_INVALIDA, 3)

    return imagem


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
META_REPETICOES = 10   # would come from the Qt interface

while captura.isOpened():
    ret, imagem = captura.read()
    if not ret:
        break

    h, w = imagem.shape[:2]
    imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    resultado  = pose.process(imagem_rgb)

    contador, invalidas, rep_invalida, info_valor = 0, 0, False, 0.0

    if resultado.pose_landmarks:
        print(f"[{EXERCICIO_ATIVO}] valor={info_valor:.1f} estado={exercicio.estado} reps={contador}")
        
        mp_drawing.draw_landmarks(
            imagem,
            resultado.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        pontos = pts_module.get_points(
            resultado.pose_landmarks,
            mp_pose.PoseLandmark,
            w, h
        )

        contador, invalidas, rep_invalida, info_valor = exercicio.atualizar(pontos)

    desenhar_hud(imagem, contador, invalidas, rep_invalida, info_valor, META_REPETICOES)

    # Stop automatically when goal is reached
    if contador >= META_REPETICOES:
        cv2.putText(imagem, "META ATINGIDA!", (w // 2 - 140, h // 2),
                    FONTE, 1.5, COR_VALIDA, 3)
        cv2.imshow("Exercicio", imagem)
        cv2.waitKey(2000)
        break

    cv2.imshow("Exercicio", imagem)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

captura.release()
cv2.destroyAllWindows()
