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

# python sketchy_lines.py inputFile outputFile threshold1 threshold2 lineWidth opacity lengthOftheVideo

OUTPUT_FILE_NAME = "video_sketch" #TODO: output name

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

img = cv2.imread('human.jpg', cv2.IMREAD_UNCHANGED)#TODO:
edges = cv2.Canny(img, 150, 300, apertureSize=3, L2gradient=True) #TODO:

#MORPHOLOGIC CLEANING
kernel1 = cv2.getStructuringElement(cv2.MORPH_CROSS, (1,1))
kernel5 = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,5))#TODO: kalinlik
edges_eroded = cv2.morphologyEx(edges, cv2.MORPH_DILATE, kernel5)
edges = cv2.morphologyEx(edges_eroded, cv2.MORPH_ERODE, kernel1)

# edges = 255*np.asarray([[0,1,1,0],
#                         [1,0,0,1],
#                         [1,0,0,1],
#                         [0,1,1,1],
#                         [0,1,0,1]],dtype=np.uint8)
edges_bool = edges.astype(np.bool)

h, w = edges_bool.shape

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
video = cv2.VideoWriter(OUTPUT_FILE_NAME + ".avi",1,10.0,(w, h))

raw_edges = np.zeros((h+2, w+2), dtype=np.uint8)
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
output_image = np.ones((h,w), dtype=np.bool)

line_dict = dict()
line_ordered = list()

video_img = 255 * np.ones((h,w), dtype=np.uint8)
dot_number = 0
for i in range(h):
    for j in range(w):
        if recoded_buff[i,j] > 0:
            #print output_image
            #print recoded_buff
            x = j
            y = i
            from_code = 0
            node_buff = recoded_buff[i,j]
            line_list = list()
            while(node_buff > 0):
                #print output_image
                #print recoded_buff

                output_image[y,x] = 0

                line_list.append((x,y))

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

            line_list_len = len(line_list)
            dot_number += line_list_len
            if line_list_len not in line_dict:
                line_dict[len(line_list)] = list()
            line_dict[len(line_list)].append(line_list)
            line_ordered.append((line_list_len, line_list))
            pass


counter = 0
outline_line_size = int(len(line_dict.keys())/7)
line_dict_keys = sorted(line_dict.keys(), reverse=True)[0:outline_line_size]
for key in line_dict_keys:
    for points_batch in line_dict[key]:
        for x, y in points_batch:
            #write to video
            video_img[y, x] = max(0, video_img[y, x] - 40)#TODO: opacitiy
            if counter % int(dot_number/500) == 0: #TODO:
                #video_to_show = cv2.resize(video_img, (w, h))
                #if counter % 1000 == 0:
                    #cv2.imwrite("video_img_" + str(counter/100) + ".png", video_to_show)
                imRGB = cv2.cvtColor(video_img, cv2.COLOR_GRAY2RGB)
                video.write(imRGB)
            counter += 1


for line_len, points_batch in line_ordered:
    if line_len < line_dict_keys[-1]:
        for x, y in points_batch:
            #write to video
            video_img[y, x] = max(0, video_img[y, x] - 40) #TODO: opacitiy
            if counter % int(dot_number/500) == 0: #TODO: length of the video
                #video_to_show = cv2.resize(video_img, (w, h))
                #if counter % 1000 == 0:
                    #cv2.imwrite("video_img_" + str(counter/100) + ".png", video_to_show)
                imRGB = cv2.cvtColor(video_img, cv2.COLOR_GRAY2RGB)
                video.write(imRGB)
            counter += 1

cv2.destroyAllWindows()
video.release()