def get_points(lm, lmPose, w, h):
    return {
        "ombro_esq": (
            int(lm.landmark[lmPose.LEFT_SHOULDER].x * w),
            int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
        ),
        "ombro_dir": (
            int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w),
            int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)
        ),
        "cotovelo_esq": (
            int(lm.landmark[lmPose.LEFT_ELBOW].x * w),
            int(lm.landmark[lmPose.LEFT_ELBOW].y * h)
        ),
        "cotovelo_dir": (
            int(lm.landmark[lmPose.RIGHT_ELBOW].x * w),
            int(lm.landmark[lmPose.RIGHT_ELBOW].y * h)
        ),
        "pulso_esq": (
            int(lm.landmark[lmPose.LEFT_WRIST].x * w),
            int(lm.landmark[lmPose.LEFT_WRIST].y * h)
        ),
        "pulso_dir": (
            int(lm.landmark[lmPose.RIGHT_WRIST].x * w),
            int(lm.landmark[lmPose.RIGHT_WRIST].y * h)
        ),
        "cintura_esq": (
            int(lm.landmark[lmPose.LEFT_HIP].x * w),
            int(lm.landmark[lmPose.LEFT_HIP].y * h)
        ),
        "cintura_dir": (
            int(lm.landmark[lmPose.RIGHT_HIP].x * w),
            int(lm.landmark[lmPose.RIGHT_HIP].y * h)
        ),
        "joelho_esq": (
            int(lm.landmark[lmPose.LEFT_KNEE].x * w),
            int(lm.landmark[lmPose.LEFT_KNEE].y * h)
        ),
        "joelho_dir": (
            int(lm.landmark[lmPose.RIGHT_KNEE].x * w),
            int(lm.landmark[lmPose.RIGHT_KNEE].y * h)
        ),
        "tornozelo_esq": (
            int(lm.landmark[lmPose.LEFT_ANKLE].x * w),
            int(lm.landmark[lmPose.LEFT_ANKLE].y * h)
        ),
        "tornozelo_dir": (
            int(lm.landmark[lmPose.RIGHT_ANKLE].x * w),
            int(lm.landmark[lmPose.RIGHT_ANKLE].y * h)
        )
    }
