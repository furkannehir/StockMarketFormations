from fastdtw import dtw, fastdtw
from scipy.spatial.distance import euclidean

x = [2,4,6,4,2]
y = [4,6,8,6,4]
z = [6,5,4,3,2,1]

dType = euclidean

result, path = dtw(x, y, dist=dType)
print(result)
print(path)

result, path = fastdtw(x, z, dist=dType)
print(result)
print(path)

result, path = fastdtw(y, z, dist=dType)
print(result)
print(path)