import cv2
import numpy as np
from matplotlib import pyplot as plt


#  _____ _____ _____
# |     |     |     |
# |  1  |  2  |  4  |
# |_____|_____|_____|
# |     |     |     |
# |  8  |  X  | 16  |
# |_____|_____|_____|
# |     |     |     |
# | 32  | 64  | 128 |
# |_____|_____|_____|



OUTPUT_FILE_NAME = "video_sketch"
MAX_WIDTH = 640.0
MAX_HEIGHT = 480.0

codes = [128, 64, 32, 16, 8, 4, 2, 1]
map_to_go = { 1 : [-1,-1],
              2 : [-1, 0],
              4 : [-1, 1],
              8 : [ 0,-1],
             16 : [ 0, 1],
             32 : [ 1,-1],
             64 : [ 1, 0],
            128 : [ 1, 1]
            }

def codeToGo(node, codes):
    for code in codes:
        if node // code:
            return code
    print "Error codeToGo returns 0"
    return 0

def whereToGo(code_to_go, y, x, map_to_go):
    return y + map_to_go[code_to_go][0], x + map_to_go[code_to_go][1]

img = cv2.imread('apple.jpg', cv2.IMREAD_UNCHANGED)
edges = cv2.Canny(img, 100, 200, apertureSize=3, L2gradient=True)
edges = cv2.bitwise_not(edges)

#MORPHOLOGIC CLEANING
kernel1 = cv2.getStructuringElement(cv2.MORPH_CROSS, (1,1))
kernel5 = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,5))
edges_eroded = cv2.morphologyEx(edges, cv2.MORPH_ERODE, kernel5)
edges_eroded = cv2.morphologyEx(edges_eroded, cv2.MORPH_DILATE, kernel1)

edges = cv2.bitwise_not(edges_eroded)

# edges = 255*np.asarray([[0,1,1,0],
#                         [1,0,0,1],
#                         [1,0,0,1],
#                         [0,1,1,1],
#                         [0,1,0,1]],dtype=np.uint8)
edges_bool = edges.astype(np.bool)

w, h = edges_bool.shape
resizer_coefficient = min(MAX_HEIGHT/h, MAX_WIDTH/w)
h_resized = int(h * resizer_coefficient)
w_resized = int(w * resizer_coefficient)
fourcc = cv2.VideoWriter_fourcc(*'X264')
video = cv2.VideoWriter(OUTPUT_FILE_NAME + ".avi",fourcc,10.0,(w, h))

raw_edges = np.zeros((w+2, h+2), dtype=np.uint8)
raw_edges[1:-1, 1:-1] = edges_bool

recoded_edges = edges_bool * (raw_edges[0:-2, 0:-2] +
                              2 * raw_edges[0:-2, 1:-1] +
                              4 * raw_edges[0:-2, 2:] +
                              8 * raw_edges[1:-1, 0:-2] +
                              16 * raw_edges[1:-1, 2:] +
                              32 * raw_edges[2:, 0:-2] +
                              64 * raw_edges[2:, 1:-1] +
                              128 * raw_edges[2:, 2:])

recoded_buff = np.copy(recoded_edges)
output_image = np.ones((w,h), dtype=np.bool)

video_img = 255 * np.ones((w,h), dtype=np.uint8)
counter = 0
for i in range(h-1):
    for j in range(w-1):
        if recoded_buff[i,j] > 0:
            #print output_image
            #print recoded_buff
            x = j
            y = i
            from_code = 0
            node_buff = recoded_buff[i,j]
            while(node_buff > 0):
                #print output_image
                #print recoded_buff

                output_image[y,x] = 0

                #write to video
                video_img[y, x] = max(0, video_img[y, x] - 80)
                if counter % 1000 == 0:
                    video_to_show = cv2.resize(video_img, (w, h))
                    #if counter % 1000 == 0:
                        #cv2.imwrite("video_img_" + str(counter/100) + ".png", video_to_show)
                    imRGB = cv2.cvtColor(video_to_show, cv2.COLOR_GRAY2RGB)
                    video.write(imRGB)
                counter += 1

                #find code which points next node
                code_to_go = codeToGo(node_buff, codes)

                #erase code_to_go info
                recoded_buff[y, x] &= (255 - code_to_go)

                #code_to_go of previous node and from_code of connected node multiplication is 128
                from_code = 128 / code_to_go
                y, x = whereToGo(code_to_go, y, x, map_to_go)

                #print output_image
                #print recoded_buff
                node_buff = recoded_buff[y,x]

                # erase from_code from next code
                recoded_buff[y, x] &= (255 - from_code)

cv2.destroyAllWindows()
video.release()