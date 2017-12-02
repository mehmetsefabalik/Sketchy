import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('apple.jpg', cv2.IMREAD_UNCHANGED)
edges = cv2.Canny(img, 100, 200, apertureSize=3, L2gradient=True)
edges = cv2.bitwise_not(edges)

#MORPHOLOGIC CLEANING
kernel1 = cv2.getStructuringElement(cv2.MORPH_CROSS, (1,1))
kernel5 = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,5))
edges_eroded = cv2.morphologyEx(edges, cv2.MORPH_ERODE, kernel5)
edges_eroded = cv2.morphologyEx(edges_eroded, cv2.MORPH_DILATE, kernel1)

# connected_nums, connected_lines = cv2.connectedComponents(edges)
#
# h,w = edges.shape
# lines_matrix = np.zeros((connected_nums,h,w))
# valid_lines_matrix = np.zeros(edges.shape)
# k = 0
#
#
#
# for i in range(0, h):
#     for j in range(0,w):
#         lines_matrix[connected_lines[i,j],i,j] = 1
#
# k = 0
# for i in range(1,connected_nums):
#     pass



#plt.imshow(connected_lines, cmap=plt.get_cmap("gist_ncar"))
#plt.show()

imToShow = cv2.resize(edges_eroded, None, fx=0.5, fy=0.5)
cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
cv2.imshow('image',imToShow)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("edges_eroded.png", edges_eroded)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()