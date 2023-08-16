import ctypes
import cv2 as cv
from cvzone.HandTrackingModule import HandDetector


capture = cv.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)
is_thumb_tip_finger = False

while True:
    ret, frame = capture.read()
    hands, img = detector.findHands(frame)
    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        bbox1 = hand1["bbox"]
        center1 = hand1["center"]
        handType1 = hand1["type"]

        fingers1 = detector.fingersUp(hand1)

        middle_finger = tuple(lmList1[12][:2])
        thumb_tip_finger = tuple(lmList1[4][:2])
        thumb_mcp_finger = tuple(lmList1[2][:2])
        is_middle_finger = False

        length_thumb_mcp_and_middle, info, img = detector.findDistance(middle_finger, thumb_mcp_finger, img)
        length_thumb_tip_and_middle, info, img = detector.findDistance(middle_finger, thumb_tip_finger, img)

        if length_thumb_tip_and_middle < 15:
            is_thumb_tip_finger = True # middle ist auf thumb_tip
            print("is_thumb_tip_finger", is_thumb_tip_finger)

        if is_thumb_tip_finger == True and length_thumb_mcp_and_middle < 40:
            is_thumb_tip_finger = False # middle ist nicht mehr auf thumb_tip
            is_middle_finger = True # middle ist auf thumb_mcp
            print("is_middle_finger", is_middle_finger)

        length_thumb_tip_and_middle, info, img = detector.findDistance(middle_finger, thumb_tip_finger, img)
        if is_middle_finger == True and 30 < length_thumb_tip_and_middle < 110:
            ctypes.windll.user32.LockWorkStation()
            break

        cv.imshow("Image", img)
        cv.waitKey(1)

capture.release()
cv.destroyAllWindows()