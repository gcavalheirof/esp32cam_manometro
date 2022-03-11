import cv2
import argparse
import time
import urllib.request
import numpy as np

'''
Funcao para obter as extreminades de um componente da image
'''
def center_crop(img, dim):
	width, height = img.shape[1], img.shape[0]

	# process crop width and height for max available dimension
	crop_width = dim[0] if dim[0]<img.shape[1] else img.shape[1]
	crop_height = dim[1] if dim[1]<img.shape[0] else img.shape[0] 
	mid_x, mid_y = int(width/2), int(height/2)
	cw2, ch2 = int(crop_width/2), int(crop_height/2) 
	crop_img = img[mid_y-ch2:mid_y+ch2, mid_x-cw2:mid_x+cw2]
	return crop_img
 
# read image
while True:
  img_resp=urllib.request.urlopen('http://10.100.89.123/cam-lo.jpg')
  imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
  image=cv2.imdecode(imgnp,-1)

  cv2.imshow("original", image)
  cropped_img = center_crop(image, (100, 100))
  #cv2.imshow("cropped", cropped_img)


# convert to gray and blur
  gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)

  gray = cv2.equalizeHist(gray)

  gray = cv2.medianBlur(gray, 7)

# compute threshold
  th = gray.copy()
  th[gray<31] = 255
  th[gray>30] = 0

  #cv2.imshow("threshold", th)
  #cv2.waitKey()

# peforme an erosion
  kernel = np.ones((5,5), np.uint8)
  th = cv2.erode(th, kernel)

  cv2.imshow("threshold", th)
  #cv2.waitKey()
  
  contours, hier = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(th, (x, y), (x+w, y+h), (0, 255, 0), 2)
    # get the min area rect
    rect = cv2.minAreaRect(c)
    _a,_b , ang = cv2.minAreaRect(c)
    if _b[0] + _b[1] >= 80:
        print("--- Novo Retângulo ---")
        #print("Centro: ", _a[0])
        #print("Dimensoes: ", _b)
        #print("Angulo: ", ang)
        if _b[1] > _b[0]:
                if _a[0] > 50:
                        res_ang = (ang-45)/10.38
                        print("Quadrante 1")
                        print("Pressao:  ", res_ang)
                else:
                        res_ang = (ang+135)/10.38
                        print("Quadrante 3")
                        print("Pressao:  ", res_ang)
        else:
                if _a[0] > 50:
                        res_ang = (ang+45)/10.38
                        print("Quadrante 2")
                        print("Pressao:  ", res_ang)
                else:
                        res_ang = (ang+225)/10.38
                        print("Quadrante 4")
                        print("Pressao:  ", res_ang)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(cropped_img, [box], 0, (0, 0, 255))
    
  cv2.imshow("resultado", cropped_img)
  cv2.waitKey()
  time.sleep(1)
