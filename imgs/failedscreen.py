from typing import List, Tuple
import numpy as np
import cv2

font = cv2.FONT_HERSHEY_SIMPLEX

def make_failedscreen(size: Tuple[int], score: int, best_score: int):
    img = np.zeros((size[0], size[1], 4), dtype=np.ubyte)

    img[:, :, 3] = 127

    cv2.putText(img, f'SCORE: {score}', (size[0] // 2, size[1] * 1 // 5), font, 1.2, (255, 255, 255, 255))
    cv2.putText(img, f'BEST : {best_score}', (size[0] // 2, size[1] * 2 // 5), font, 1.2, (255, 255, 255, 255))

    return img