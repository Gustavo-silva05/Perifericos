import cv2
import time
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import RunningMode
import points_tasks as pts_module
from exercises import (
    RoscaBiceps,
    Flexao,
    Agachamento,
    Abdominal,
    Salto,
    FlexaoLateralPerna,
)

# ---------------------------------------------------------------------------
# Exercise selection
# Change EXERCICIO_ATIVO to test each exercise.
# Options: "rosca_biceps" | "flexao" | "agachamento" | "abdominal"
#          | "salto" | "flexao_lateral_perna"
# ---------------------------------------------------------------------------
EXERCICIO_ATIVO   = "rosca_biceps"
META_REPETICOES   = 10
MODEL_PATH        = "pose_landmarker.task"
CAMERA_INDEX      = 0   # change to 1, 2... if using Iriun
COUNTDOWN_SECONDS = 5
# ---------------------------------------------------------------------------
# MediaPipe setup (new Tasks API)
# ---------------------------------------------------------------------------
base_options    = python.BaseOptions(model_asset_path=MODEL_PATH)
options         = vision.PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=RunningMode.VIDEO,   # VIDEO mode: we pass timestamps ourselves
    num_poses=1,
    min_pose_detection_confidence=0.5,
    min_pose_presence_confidence=0.5,
    min_tracking_confidence=0.5,
)
landmarker = vision.PoseLandmarker.create_from_options(options)

def countdown(captura, landmarker, segundos=COUNTDOWN_SECONDS):
    """
    Shows a live camera feed with a countdown overlay.
    The exercise counter won't start until this returns.
    """
    inicio = time.time()
    while True:
        ret, imagem = captura.read()
        if not ret:
            break

        restante = segundos - int(time.time() - inicio)
        if restante <= 0:
            break

        cv2.putText(imagem, "Entre em posicao!", (w_frame // 2 - 160, h_frame // 2 - 50),
                    FONTE, 1.0, (255, 255, 0), 2)
        cv2.putText(imagem, str(restante), (w_frame // 2 - 30, h_frame // 2 + 40),
                    FONTE, 3.0, (0, 255, 0), 4)

        cv2.imshow("Exercicio", imagem)
        cv2.waitKey(1)

# ---------------------------------------------------------------------------
# Drawing helper (replaces mp_drawing — new API has no built-in draw util)
# ---------------------------------------------------------------------------
CONNECTIONS = [
    (11, 12), (11, 13), (13, 15),   # left arm
    (12, 14), (14, 16),             # right arm
    (11, 23), (12, 24),             # torso sides
    (23, 24),                       # hips
    (23, 25), (25, 27),             # left leg
    (24, 26), (26, 28),             # right leg
]

def desenhar_skeleton(imagem, landmarks, w, h):
    pts = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
    for a, b in CONNECTIONS:
        cv2.line(imagem, pts[a], pts[b], (0, 255, 0), 2)
    for p in pts:
        cv2.circle(imagem, p, 4, (255, 255, 255), -1)

# ---------------------------------------------------------------------------
# Camera capture
# ---------------------------------------------------------------------------
captura = cv2.VideoCapture(CAMERA_INDEX)
ret, frame_teste = captura.read()
if not ret:
    raise RuntimeError(
        f"Could not open camera at index {CAMERA_INDEX}. "
        "Try changing CAMERA_INDEX to 1 or 2."
    )
h_frame, w_frame = frame_teste.shape[:2]

# ---------------------------------------------------------------------------
# Instantiate exercise counters
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
# HUD
# ---------------------------------------------------------------------------
COR_VALIDA   = (0, 255, 0)
COR_INVALIDA = (0, 0, 255)
FONTE        = cv2.FONT_HERSHEY_SIMPLEX


def desenhar_hud(imagem, contador, invalidas, rep_invalida, info_valor, meta):
    overlay = imagem.copy()
    cv2.rectangle(overlay, (0, 0), (260, 140), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.4, imagem, 0.6, 0, imagem)

    cor_borda = COR_INVALIDA if rep_invalida else COR_VALIDA
    cv2.putText(imagem, f"Reps: {contador} / {meta}",  (10, 35),  FONTE, 1.0, cor_borda, 2)
    cv2.putText(imagem, f"Invalidas: {invalidas}",      (10, 70),  FONTE, 0.8,
                COR_INVALIDA if invalidas > 0 else COR_VALIDA, 2)
    cv2.putText(imagem, f"Valor: {info_valor:.1f}",     (10, 105), FONTE, 0.7, (255, 255, 255), 1)

    if rep_invalida:
        cv2.putText(imagem, "! REP INCOMPLETA !",
                    (w_frame // 2 - 160, h_frame - 20),
                    FONTE, 1.2, COR_INVALIDA, 3)


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
frame_idx = 0

countdown(captura, landmarker)

while captura.isOpened():
    ret, imagem = captura.read()
    if not ret:
        break

    # Optional: flip if camera is mirrored
    # imagem = cv2.flip(imagem, 1)

    h, w = imagem.shape[:2]

    # Convert to mediapipe Image
    imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    mp_image   = mp.Image(image_format=mp.ImageFormat.SRGB, data=imagem_rgb)

    # Detect — VIDEO mode requires a monotonically increasing timestamp in ms
    timestamp_ms = int(captura.get(cv2.CAP_PROP_POS_MSEC))
    if timestamp_ms == 0:
        timestamp_ms = frame_idx * 33   # fallback: assume ~30fps
    resultado = landmarker.detect_for_video(mp_image, timestamp_ms)

    contador, invalidas, rep_invalida, info_valor = 0, 0, False, 0.0

    if resultado.pose_landmarks:
        landmarks = resultado.pose_landmarks[0]
        desenhar_skeleton(imagem, landmarks, w, h)
        pontos = pts_module.get_points(landmarks, w, h)
        contador, invalidas, rep_invalida, info_valor = exercicio.atualizar(pontos)

        print(f"[{EXERCICIO_ATIVO}] valor={info_valor:.1f}  estado={exercicio.estado}  reps={contador}")

    desenhar_hud(imagem, contador, invalidas, rep_invalida, info_valor, META_REPETICOES)

    if contador >= META_REPETICOES:
        cv2.putText(imagem, "META ATINGIDA!", (w // 2 - 140, h // 2),
                    FONTE, 1.5, COR_VALIDA, 3)
        cv2.imshow("Exercicio", imagem)
        cv2.waitKey(2000)
        break

    cv2.imshow("Exercicio", imagem)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_idx += 1

captura.release()
landmarker.close()
cv2.destroyAllWindows()