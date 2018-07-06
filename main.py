import sys
import os
sys.path.append(os.path.abspath("libs/"))
from util import *


fileNames = getFilesFromFolder(FOLDER_IMGS)
lines = readFile(IMG_INFO)
lines = getLineInfo(lines)



labels = getDistinctClass(lines)
makeFolders(FOLDER_CROPPED, labels)
makeFolders(FOLDER_MARKED, labels)

for line in lines:
    markRegion(line)
print "MARKED COMPLETE"

for line in lines:
    crop(line)
print "CROP COMPLETE"
