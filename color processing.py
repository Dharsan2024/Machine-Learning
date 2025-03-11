import cv2
import pandas as pd
import numpy as np
import os

image_path = r"X:\programmig\PYTHON\ML\image color processing\sist (1).jpg"
csv_path = r"X:\programmig\PYTHON\ML\image color processing\colors.csv"

if not os.path.exists(image_path):
    print("Error: Image file not found. Check the file path!")
    exit()

if not os.path.exists(csv_path):
    print("Error: colors.csv file not found. Check the file path!")
    exit()

img = cv2.imread(image_path)

screen_width = 1280
screen_height = 720
aspect_ratio = img.shape[1] / img.shape[0]
if img.shape[1] > screen_width or img.shape[0] > screen_height:
    if aspect_ratio > 1:
        img = cv2.resize(img, (screen_width, int(screen_width / aspect_ratio)))
    else:
        img = cv2.resize(img, (int(screen_height * aspect_ratio), screen_height))

imgWidth = img.shape[1] - 40

index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv(csv_path, header=None, names=index)

r = g = b = xpos = ypos = 0
clicked = False

def getRGBvalue(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDOWN:  
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]  
        b = int(b)
        g = int(g)
        r = int(r)

def colorname(B, G, R):
    minimum = float('inf')
    cname = "Unknown"
    for i in range(len(df)):
        d = abs(B - int(df.loc[i, "B"])) + abs(G - int(df.loc[i, "G"])) + abs(R - int(df.loc[i, "R"]))
        if d < minimum:
            minimum = d
            cname = df.loc[i, "color_name"] + " Hex: " + df.loc[i, "hex"]
    return cname

cv2.namedWindow("Image")
cv2.setMouseCallback("Image", getRGBvalue)

while True:
    cv2.imshow("Image", img)

    if clicked:
        cv2.rectangle(img, (20, 20), (imgWidth, 60), (b, g, r), -1)

        
        text = colorname(b, g, r) + ' | R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

       
        text_color = (255, 255, 255) if r + g + b < 600 else (0, 0, 0)
        cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, text_color, 2, cv2.LINE_AA)

        clicked = False  

    
    if cv2.waitKey(20) & 0xFF == 27:
        break


cv2.destroyAllWindows()
