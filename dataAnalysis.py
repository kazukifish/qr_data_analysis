# This program is a simple visualization of QRCodes data

import matplotlib.pyplot as plt
# import numpy as np

# read
readFileList = []

# write
outputList = []
maxInterval = 30
standardInterval = 25

with open("","r",encoding="utf-8") as f:
    readFileList = f.readlines()

for line in readFileList:
    newDate = int(line[5:7])*3600+int(line[7:9])*60+int(line[9:11]) # date of latest data
    if not line in outputList: # prevent duplication
        if not outputList: # outputList is empty
            data1 = line[11:17]
            data2 = line[17:23]
            data3 = line[23:29]
            data4 = line[29:35]
            data5 = line[35:41]
            for i in data1,data2,data3,data4,data5: # negative or positive
                if i[0] == "1": # index0 = 1 → negative
                    i = float(i[1:])/(-100)
                else:
                    i = float(i[1:])/(100)
                outputList.append(i)
            oldDate = newDate
        else: # there is one or more data in outputList
            difTime = newDate - oldDate
            if difTime <= maxInterval: # no missing value
                data1 = line[11:17]
                data2 = line[17:23]
                data3 = line[23:29]
                data4 = line[29:35]
                data5 = line[35:41]
                for i in data1,data2,data3,data4,data5:
                    if i[0] == "1":
                        i = float(i[1:])/(-100)
                    else:
                        i = float(i[1:])/(100)
                    outputList.append(i)
                oldDate = newDate
            else: # there is one or more missing value
                countLostQr = difTime//standardInterval
                for _ in range(countLostQr):
                    for _ in range(5):
                        outputList.append(-1.0) # insert -1.0 the number of missing value
                data1 = line[11:17]
                data2 = line[17:23]
                data3 = line[23:29]
                data4 = line[29:35]
                data5 = line[35:41]
                for i in data1,data2,data3,data4,data5:
                    if i[0] == "1":
                        i = float(i[1:])/(-100)
                    else:
                        i = float(i[1:])/(100)
                    outputList.append(i)
                oldDate = newDate
    
# 1: simple plot
print(len(outputList))
indexList = [i/12 for i in range(len(outputList))] # 平均データではない場合
# indexList2 = [i*5/12 for i in range(len(outputList))] # 平均5データの場合
plt.scatter(indexList,outputList,s=1)
plt.xlabel("Time(min)")
plt.ylabel("Output current (nA)")
plt.show()

#2: average plot
# cnt = 0
# aveData = 0
# averageList = []
# for ave in outputList: # Create a list that stores the average value of 5 data
#     aveData += ave
#     cnt += 1
#     if cnt == 5:
#         aveData = aveData/5
#         averageList.append(aveData)
#         aveData = 0
#         cnt = 0
# aveIdList = [i/12 for i in range(len(averageList))]
# plt.scatter(aveIdList,averageList,s=1)
# plt.xlabel("time(min)")
# plt.ylabel("output current(nA)")
# plt.show()

# 3: vector and rate of change
# cnt = 0
# aveData = 0
# averageList = []
# rcList = []
# baseVal = (outputList[0]+outputList[1]+outputList[2]+outputList[3]+outputList[4])/5
# for ave in outputList: # Create a list that stores the average value of 5 data
#     aveData += ave
#     cnt += 1
#     if cnt == 5:
#         aveData = aveData/5
#         averageList.append(aveData)
#         rc = "{:.2f}".format(aveData/baseVal)
#         rcList.append(float(rc))
#         aveData = 0
#         cnt = 0
# rcList = rcList[1:]
# vaList = []
# aveIdList = [i/12 for i in range(len(averageList))]
# lenList = len(aveIdList)-1

# # ここはpandasで実装できる？
# compList = []
# for id,data in zip(aveIdList,averageList):
#     list = [id,data]
#     compList.append(list)

# npCompList = np.array(compList)
# for i in range(lenList):
#     vec = npCompList[i+1]-npCompList[i]
#     vecAngle = np.arctan2(vec[0],vec[1])
#     va = vecAngle.tolist()
#     va = "{:.3f}".format(float(va))
#     vaList.append(float(va))
#     rc = rcList[i]
#     with open("231208_ocsvm_v.txt","a",encoding="utf-8") as f:
#         print("tan2:",va,"rc",rc,file=f)
# plt.scatter(rcList,vaList,s=1)
# plt.xlabel("rate of change from base value")
# plt.ylabel("angle")
# plt.show()