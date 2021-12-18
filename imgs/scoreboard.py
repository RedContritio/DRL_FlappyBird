from typing import List, Tuple
import numpy as np
import cv2

font = cv2.FONT_HERSHEY_SIMPLEX

def make_scoreboard(size: Tuple[int], score: int, best_score: int):
    img = np.zeros((size[0], size[1], 4), dtype=np.ubyte)

    cv2.putText(img, f'SCORE: {score}', (20, 20), font, 0.5, (255, 255, 255, 255))
    cv2.putText(img, f'BEST : {best_score}', (20, 40), font, 0.5, (255, 255, 255, 255))

    return img