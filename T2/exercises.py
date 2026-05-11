from utils import calcular_angulo, distancia_euclidiana


class ExerciseCounter:
    """
    Base class for all exercises.
    Holds state, rep counter and invalid rep flag.

    State machine:
        - "inicio"   : waiting for the user to reach the start position
        - "pronto"   : at start position, waiting for movement
        - "subindo"  : committed to a rep (passed LIMIAR_COMMIT)
        - "descendo" : completed the peak, returning to start
    
    A rep is only considered started after crossing LIMIAR_COMMIT.
    Small accidental movements before that are ignored entirely.
    An invalid rep is only registered if the user commits past LIMIAR_COMMIT
    but reverses before reaching LIMIAR_CIMA (or LIMIAR_BAIXO for push/squat).
    """

    def __init__(self):
        self.contador    = 0
        self.invalidas   = 0
        self.estado      = "inicio"
        self.rep_invalida = False

    def _registrar_rep_valida(self):
        self.contador += 1
        self.rep_invalida = False

    def _registrar_rep_invalida(self):
        self.invalidas += 1
        self.rep_invalida = True

    def reset(self):
        self.contador     = 0
        self.invalidas    = 0
        self.estado       = "inicio"
        self.rep_invalida = False


# ---------------------------------------------------------------------------
# SIDE-VIEW EXERCISES
# ---------------------------------------------------------------------------

class RoscaBiceps(ExerciseCounter):
    """
    Bicep Curl — side view.
    Angle tracked: shoulder -> elbow -> wrist

    Positions:
        LIMIAR_BAIXO  (160°) : arm fully extended  — ready position
        LIMIAR_COMMIT (120°) : point of no return  — rep is now "started"
        LIMIAR_CIMA   ( 40°) : arm fully curled    — valid rep peak
    """

    LIMIAR_BAIXO  = 160
    LIMIAR_COMMIT = 120
    LIMIAR_CIMA   = 40

    def atualizar(self, pts):
        angulo = calcular_angulo(
            pts["ombro_esq"],
            pts["cotovelo_esq"],
            pts["pulso_esq"]
        )

        if self.estado == "inicio":
            if angulo > self.LIMIAR_BAIXO:
                self.estado = "pronto"

        elif self.estado == "pronto":
            # Only commit when the arm moves meaningfully
            if angulo < self.LIMIAR_COMMIT:
                self.estado = "subindo"

        elif self.estado == "subindo":
            if angulo < self.LIMIAR_CIMA:
                # Reached full curl — valid
                self.estado = "descendo"
                self._registrar_rep_valida()
            elif angulo > self.LIMIAR_BAIXO:
                # Committed but gave up — invalid
                self.estado = "pronto"
                self._registrar_rep_invalida()

        elif self.estado == "descendo":
            if angulo > self.LIMIAR_BAIXO:
                self.estado = "pronto"
                self.rep_invalida = False

        return self.contador, self.invalidas, self.rep_invalida, angulo


class Flexao(ExerciseCounter):
    """
    Push-Up — side view.
    Angle tracked: shoulder -> elbow -> wrist

    Positions:
        LIMIAR_CIMA   (160°) : arms fully extended — ready position
        LIMIAR_COMMIT (130°) : point of no return  — rep is now "started"
        LIMIAR_BAIXO  ( 90°) : arms fully bent     — valid rep bottom
    """

    LIMIAR_CIMA   = 160
    LIMIAR_COMMIT = 130
    LIMIAR_BAIXO  = 90

    def atualizar(self, pts):
        angulo = calcular_angulo(
            pts["ombro_esq"],
            pts["cotovelo_esq"],
            pts["pulso_esq"]
        )

        if self.estado == "inicio":
            if angulo > self.LIMIAR_CIMA:
                self.estado = "pronto"

        elif self.estado == "pronto":
            if angulo < self.LIMIAR_COMMIT:
                self.estado = "descendo"

        elif self.estado == "descendo":
            if angulo < self.LIMIAR_BAIXO:
                # Reached the bottom
                self.estado = "subindo"
            elif angulo > self.LIMIAR_CIMA:
                # Committed but reversed before reaching bottom — invalid
                self.estado = "pronto"
                self._registrar_rep_invalida()

        elif self.estado == "subindo":
            if angulo > self.LIMIAR_CIMA:
                # Fully extended again — valid
                self.estado = "pronto"
                self._registrar_rep_valida()

        return self.contador, self.invalidas, self.rep_invalida, angulo


class Agachamento(ExerciseCounter):
    """
    Squat — side view.
    Angle tracked: hip -> knee -> ankle

    Positions:
        LIMIAR_CIMA   (160°) : legs fully extended — ready position
        LIMIAR_COMMIT (140°) : point of no return  — rep is now "started"
        LIMIAR_BAIXO  ( 90°) : thighs parallel     — valid rep bottom
    """

    LIMIAR_CIMA   = 160
    LIMIAR_COMMIT = 140
    LIMIAR_BAIXO  = 90

    def atualizar(self, pts):
        angulo = calcular_angulo(
            pts["cintura_esq"],
            pts["joelho_esq"],
            pts["tornozelo_esq"]
        )

        if self.estado == "inicio":
            if angulo > self.LIMIAR_CIMA:
                self.estado = "pronto"

        elif self.estado == "pronto":
            if angulo < self.LIMIAR_COMMIT:
                self.estado = "descendo"

        elif self.estado == "descendo":
            if angulo < self.LIMIAR_BAIXO:
                self.estado = "subindo"
            elif angulo > self.LIMIAR_CIMA:
                # Committed but reversed before reaching depth — invalid
                self.estado = "pronto"
                self._registrar_rep_invalida()

        elif self.estado == "subindo":
            if angulo > self.LIMIAR_CIMA:
                self.estado = "pronto"
                self._registrar_rep_valida()

        return self.contador, self.invalidas, self.rep_invalida, angulo


class Abdominal(ExerciseCounter):
    """
    Sit-Up — side view (person lying down).
    Angle tracked: shoulder -> hip -> knee

    Positions:
        LIMIAR_DEITADO (120°) : body flat      — ready position
        LIMIAR_COMMIT  ( 90°) : point of no return
        LIMIAR_SENTADO ( 60°) : torso raised   — valid rep peak
    """

    LIMIAR_DEITADO = 120
    LIMIAR_COMMIT  = 90
    LIMIAR_SENTADO = 60

    def atualizar(self, pts):
        angulo = calcular_angulo(
            pts["ombro_esq"],
            pts["cintura_esq"],
            pts["joelho_esq"]
        )

        if self.estado == "inicio":
            if angulo > self.LIMIAR_DEITADO:
                self.estado = "pronto"

        elif self.estado == "pronto":
            if angulo < self.LIMIAR_COMMIT:
                self.estado = "subindo"

        elif self.estado == "subindo":
            if angulo < self.LIMIAR_SENTADO:
                self.estado = "descendo"
                self._registrar_rep_valida()
            elif angulo > self.LIMIAR_DEITADO:
                # Committed but reversed before reaching the top — invalid
                self.estado = "pronto"
                self._registrar_rep_invalida()

        elif self.estado == "descendo":
            if angulo > self.LIMIAR_DEITADO:
                self.estado = "pronto"
                self.rep_invalida = False

        return self.contador, self.invalidas, self.rep_invalida, angulo


# ---------------------------------------------------------------------------
# FRONT-VIEW EXERCISES
# ---------------------------------------------------------------------------

class Salto(ExerciseCounter):
    """
    Jump — front view.
    Tracks vertical displacement of the average hip Y position.

    LIMIAR_SALTO_FATOR : hips must rise by this fraction of frame height
    LIMIAR_COMMIT_FATOR: fraction of LIMIAR_SALTO that must be crossed
                         before a jump is considered "started"

    State machine:
        "calibrando" : collecting baseline hip Y (first N frames)
        "pronto"     : standing, waiting for jump
        "no_ar"      : committed to a jump (hips rose past commit threshold)
    """

    CALIBRATION_FRAMES  = 30
    LIMIAR_SALTO_FATOR  = 0.15  
    LIMIAR_COMMIT_FATOR = 0.5   

    def __init__(self, altura_frame):
        super().__init__()
        self.estado               = "calibrando"
        self.altura_frame         = altura_frame
        self._calibration_readings = []
        self.baseline_y           = None
        self.limiar_salto         = int(altura_frame * self.LIMIAR_SALTO_FATOR)
        self.limiar_commit        = int(self.limiar_salto * self.LIMIAR_COMMIT_FATOR)

    def _hip_y(self, pts):
        return (pts["cintura_esq"][1] + pts["cintura_dir"][1]) // 2

    def atualizar(self, pts):
        y_atual = self._hip_y(pts)

        if self.estado == "calibrando":
            self._calibration_readings.append(y_atual)
            if len(self._calibration_readings) >= self.CALIBRATION_FRAMES:
                self.baseline_y = int(
                    sum(self._calibration_readings) / len(self._calibration_readings)
                )
                self.estado = "pronto"

        elif self.estado == "pronto":
            # Commit only after rising past the commit threshold
            if y_atual < self.baseline_y - self.limiar_commit:
                self.estado = "no_ar"

        elif self.estado == "no_ar":
            # Register at the peak — when Y stops dropping
            # Full jump: reached LIMIAR_SALTO
            if y_atual < self.baseline_y - self.limiar_salto:
                self._registrar_rep_valida()
                self.estado = "aterrissando"
            # Partial jump: rising back without reaching full height
            elif y_atual > self.baseline_y - self.limiar_commit:
                self._registrar_rep_invalida()
                self.estado = "pronto"

        elif self.estado == "aterrissando":
            # Wait for full return to baseline before next rep
            if y_atual > self.baseline_y - self.limiar_commit:
                self.estado = "pronto"
                self.rep_invalida = False

        return self.contador, self.invalidas, self.rep_invalida, y_atual


class FlexaoLateralPerna(ExerciseCounter):
    """
    Lateral Leg Flexion — front view.
    Angle tracked: opposite_hip -> lifting_hip -> lifting_knee

    Positions:
        LIMIAR_BAIXO  (10°) : leg hanging down  — ready position
        LIMIAR_COMMIT (18°) : point of no return — rep is now "started"
        LIMIAR_CIMA   (30°) : leg fully lifted   — valid rep peak
    """

    LIMIAR_BAIXO  = 10
    LIMIAR_COMMIT = 18
    LIMIAR_CIMA   = 30

    def _abducao_angulo(self, pts, lado):
        if lado == "esq":
            ref     = pts["cintura_dir"]
            quadril = pts["cintura_esq"]
            joelho  = pts["joelho_esq"]
        else:
            ref     = pts["cintura_esq"]
            quadril = pts["cintura_dir"]
            joelho  = pts["joelho_dir"]
        return calcular_angulo(ref, quadril, joelho)

    def _detectar_lado(self, pts):
        # Lower Y = higher on screen = lifted leg
        if pts["joelho_esq"][1] < pts["joelho_dir"][1]:
            return "esq"
        return "dir"

    def atualizar(self, pts):
        lado   = self._detectar_lado(pts)
        angulo = self._abducao_angulo(pts, lado)

        if self.estado == "inicio":
            if angulo < self.LIMIAR_BAIXO:
                self.estado = "pronto"

        elif self.estado == "pronto":
            if angulo > self.LIMIAR_COMMIT:
                self.estado = "subindo"

        elif self.estado == "subindo":
            if angulo > self.LIMIAR_CIMA:
                # Reached full lateral lift — valid
                self.estado = "descendo"
                self._registrar_rep_valida()
            elif angulo < self.LIMIAR_BAIXO:
                # Committed but leg came back down — invalid
                self.estado = "pronto"
                self._registrar_rep_invalida()

        elif self.estado == "descendo":
            if angulo < self.LIMIAR_BAIXO:
                self.estado = "pronto"
                self.rep_invalida = False

        return self.contador, self.invalidas, self.rep_invalida, angulo