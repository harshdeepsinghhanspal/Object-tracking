import cv2

cap = cv2.VideoCapture('Resources/VID20220428160731.mp4')
frameWidth = 1280
frameHeight = 720


############### Tracker Types #####################

#tracker = cv2.legacy.TrackerBoosting_create()
#tracker = cv2.TrackerMIL_create()
#tracker = cv2.legacy.TrackerKCF_create()
#tracker = cv2.legacy.TrackerTLD_create()
#tracker = cv2.legacy.TrackerMedianFlow_create()
#tracker = cv2.TrackerCSRT_create()
tracker = cv2.legacy.TrackerMOSSE_create()

########################################################


# TRACKER INITIALIZATION
success, frame = cap.read()
frame = cv2.resize(frame, (frameWidth, frameHeight))
bbox = cv2.selectROI("Tracking",frame, False)
tracker.init(frame, bbox)


def drawBox(img,bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (0, 0, 255), 3, 3 )
    cv2.putText(img, "Tracking", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


while True:

    timer = cv2.getTickCount()
    success, img = cap.read()
    img = cv2.resize(img, (frameWidth, frameHeight))
    success, bbox = tracker.update(img)

    if success:
        drawBox(img,bbox)
    else:
        cv2.putText(img, "Lost", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.rectangle(img,(15,15),(200,90),(0,255,0),2)
    cv2.putText(img, "Fps:", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    cv2.putText(img, "Status:", (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)


    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    if fps>60: myColor = (20,230,20)
    elif fps>20: myColor = (230,20,20)
    else: myColor = (20,20,230)
    cv2.putText(img,str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, myColor, 2)

    cv2.imshow("Tracking", img)
    if cv2.waitKey(1) & 0xff == ord('q'):
       break