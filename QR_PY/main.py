from pyzbar import  pyzbar
import cv2
import numpy as np

VideoSignal = cv2.VideoCapture(0)

while True:
    ret, frame = VideoSignal.read()
    inputImage = frame
    ROI = frame[100:380, 180:460]
    cv2.rectangle(ROI,(0,0),(279,279),(255,255,255),3)
    gray = cv2.cvtColor(inputImage,cv2.COLOR_RGB2GRAY)
    gray = cv2.GaussianBlur(gray, ksize=(3, 3), sigmaX=0) #------노이즈 제거용 가우시안 필터

    barcodes = pyzbar.decode(ROI)
    for barcode in barcodes:
        # 바코드의 영역을 추출하고 영역 그리기
        # 이미지의 바코드 주변에 박스를 그림
        (x, y, w, h) = barcode.rect
        (p1,p2,p3,p4)=barcode.polygon
        cx = int((p1[0] + p2[0] + p3[0] + p4[0]) / 4)
        cy = int((p1[1] + p2[1] + p3[1] + p4[1]) / 4)
        ax1 = int((p1[0] + p2[0]) / 2)
        ay1 = int((p1[1] + p2[1]) / 2)
        cv2.line(ROI, (cx,cy), (ax1,ay1),(255,0,0),3)

        ax2 = int((p1[0] + p4[0]) / 2)
        ay2 = int((p1[1] + p4[1]) / 2)
        cv2.line(ROI, (cx, cy), (ax2, ay2), (0, 255, 0), 3)

        x += 180 ; y+=100
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.circle(ROI, p1, 3, (255, 0, 0), 3)
        cv2.circle(ROI, p2, 3, (255, 255, 0), 3)
        cv2.circle(ROI, p3, 3, (0, 255, 0), 3)
        cv2.circle(ROI, p4, 3, (0, 25, 255), 3)

        cv2.circle(ROI, (cx,cy), 3, (0, 0, 255), 3) #중심
        print(barcode.polygon)
        #np.arctan2((cx,cy),)
        # 바코드 데이터는 바이트 객체이므로 이미지에 그리려면 문자열을 먼져 바꿔야 한다.
        barcodeData = barcode.data.decode("utf-8")

        barcodeType = barcode.type

    # 바코드 데이터와 타입을 이미지에 그림
        text = "{} ({})".format(barcodeData, barcodeType)
        #cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)

        # 바코드타입과 데이터를 터미널에 출력
        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))


    # 출력 이미지를 보여 줌

    cv2.imshow("Image",frame)
    cv2.waitKey(1)