import datetime
import numpy as np
import time
import cv2
import glob
import config
from common.gAPI import GoogleAPI
from common.sheetOperations import SheetOps

class Yolo:

    def __init__(self):
        self.objGAPI = GoogleAPI()
        self.objSheet = SheetOps()

    def getPredictOutput(self, INPUT_FILE, cmpName, range):
        service = self.objGAPI.intiate_gdAPI()
        id = ''
        # service = con
        predicatedOutput = []
        LABELS_FILE = 'yolo/obj.names'
        CONFIG_FILE = 'yolo/stock.cfg'
        WEIGHTS_FILE = 'yolo/stock_4000.weights'
        CONFIDENCE_THRESHOLD = 0.6
        try:
            LABELS = open(LABELS_FILE).read().strip().split("\n")
            np.random.seed(4)
            COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")
            net = cv2.dnn.readNetFromDarknet(CONFIG_FILE, WEIGHTS_FILE)
            # image = cv2.imread(INPUT_FILE)
            image = cv2.imdecode(INPUT_FILE, flags=1)
            (H, W) = image.shape[:2]
            # print(H, W)
            # determine only the *output* layer names that we need from YOLO
            ln = net.getLayerNames()
            ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
            # print("layers====",ln)
            blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
            net.setInput(blob)
            start = time.time()
            layerOutputs = net.forward(ln)
            end = time.time()
            # initialize our lists of detected bounding boxes, confidences, and
            # class IDs, respectively
            boxes = []
            confidences = []
            classIDs = []

            # loop over each of the layer outputs
            for output in layerOutputs:
                # loop over each of the detections
                for detection in output:
                    # extract the class ID and confidence (i.e., probability) of
                    # the current object detection
                    scores = detection[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]
                    # print("confidence==",confidence)

                    # filter out weak predictions by ensuring the detected
                    # probability is greater than the minimum probability
                    if confidence > CONFIDENCE_THRESHOLD:
                        # scale the bounding box coordinates back relative to the
                        # size of the image, keeping in mind that YOLO actually
                        # returns the center (x, y)-coordinates of the bounding
                        # box followed by the boxes' width and height
                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY, width, height) = box.astype("int")

                        # use the center (x, y)-coordinates to derive the top and
                        # and left corner of the bounding box
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))

                        # update our list of bounding box coordinates, confidences,
                        # and class IDs
                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)
                        # print("classIDs===",classIDs,confidences)

            # apply non-maxima suppression to suppress weak, overlapping bounding
            # boxes
            idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD,
                                    CONFIDENCE_THRESHOLD)

            # ensure at least one detection exists
            if len(idxs) > 0:
                # loop over the indexes we are keeping
                for i in idxs.flatten():
                    # extract the bounding box coordinates
                    (x, y) = (boxes[i][0], boxes[i][1])
                    (w, h) = (boxes[i][2], boxes[i][3])

                    color = [int(c) for c in COLORS[classIDs[i]]]

                    cv2.rectangle(image, (x, y), (x + w, y + h), color, 1)
                    text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                    # print(f'predicted class => {text}')
                    predicatedOutput.append(text)
                    cv2.putText(image, text, (x - 20, y - 30), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, color, 2)

                # check range
                filepath = ""
                dateValue = datetime.datetime.today().strftime('%d_%m_%Y_%H_%M_%S_%f')
                imageName = ""
                dst = ""

                # check range
                filepath = ""
                dateValue = datetime.datetime.today().strftime('%d_%m_%Y_%H_%M_%S_%f')
                imageName = ""
                dst = ""
                if range == '5minutes':
                    filepath = config.imagePath5
                    imageName = cmpName + "_" + dateValue + "_" + "5M.png"
                    dst = filepath + imageName
                    id = config.imagePath5_id
                elif range == '15minutes':
                    filepath = config.imagePath15
                    imageName = cmpName + "_" + dateValue + "_" + "15M.png"
                    dst = filepath + imageName
                    id = config.imagePath15_id
                elif range == '30minutes':
                    filepath = config.imagePath30
                    imageName = cmpName + "_" + dateValue + "_" + "30M.png"
                    dst = filepath + imageName
                    id = config.imagePath30_id
                elif range == '2hours':
                    filepath = config.imagePath2H
                    imageName = cmpName + "_" + dateValue + "_" + "2H.png"
                    dst = filepath + imageName
                    id = config.imagePath2H_id
                elif range == 'daily':
                    filepath = config.imagePath1D
                    imageName = cmpName + "_" + dateValue + "_" + "1D.png"
                    dst = filepath + imageName
                    id = config.imagePath1D_id
                elif range == 'weekly':
                    filepath = config.imagePath1W
                    imageName = cmpName + "_" + dateValue + "_" + "1W.png"
                    dst = filepath + imageName
                    id = config.imagePath1W_id

                print("destination===", dst)
                # cv2.imwrite(dst, image)
                destination = 'sample_data/output.png'
                cv2.imwrite(destination, image)
                # print(imageName)
                # print('imageNameType', type(imageName))
                #upload_file(self, service, filename, filepath, folder_id, mime_type):
                self.objGAPI.upload_file(service, str(imageName), destination, id, 'image/png')
                link = 'https://chartink.com/stocks/' + cmpName + '.html'

                rowLst = []
                if predicatedOutput is not None:
                    for row in predicatedOutput:
                        rowLst.append(row.split(':')[0])
                output = ""
                if predicatedOutput is not None:
                    output = ",".join(rowLst)
                print("output=====", output)
                ### writeSheet(self, filenameToRead, list_to_write, sheet_name)
                #writeSheet(self, filenameToRead, list_to_write, sheet_name)
                list_to_write = [str(datetime.datetime.now()), cmpName, cmpName, range, output, link, dst]
                self.objSheet.writeSheet('CIEnotifications', list_to_write, 'ChartlinkNotify')
                # cv2_imshow(image)
                return predicatedOutput
        except Exception as e:
            print("Exception while predicting", e)
            return predicatedOutput
