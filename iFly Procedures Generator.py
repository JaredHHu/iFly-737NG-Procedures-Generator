# 外部库
import csv

#基本信息
list_legtype = ['PI', 'HA', 'HF', 'HM', 'FM', 'VM', 'AF', 'CA', 'VA', 'CD', 'VD', 'CF', 'CI', 'VI', 'CR', 'VR', 'DF', 'FA', 'FC', 'FD', 'RF', 'TF', 'IF']

# 软件信息
print("iFly飞行程序数据文件生成器\n")
print("当前版本：0.2.0.0\n")
print("更新日志：")
print("0.1.0.0  2022.04.22  实现坐标的检查、转换、读取和存储")
print("0.2.0.0  2022.04.23  实现程序列表的检查、排序和生成\n")
print("Github仓库和编写教程：https://github.com/JaredHHu/iFly-737NG-Procedures-Generator\n")

# 函数
### 检查输入航路点正确与否
def Checkcoordinate(rawcoordinate):
	checker_coordinate = rawcoordinate.split()
	if checker_coordinate[0] == "READ" or checker_coordinate[0] == "SAVE" or checker_coordinate[0] == "DONE":
		return True
	elif 0 < len(checker_coordinate[0]) <= 5:
		if len(checker_coordinate) == 7:
			if -90 <= int(checker_coordinate[1]) <= 90:
				if 0 <= int(checker_coordinate[2]) < 60:
					if 0 <= float(checker_coordinate[3]) < 60:
						if -180 <= int(checker_coordinate[4]) <= 180:
							if 0 <= int(checker_coordinate[5]) < 60:
								if 0 <= float(checker_coordinate[6]) < 60:
									return True
								else:
									return False
							else:
								return False
						else:
							return False
					else:
						return False
				else:
					return False
			else:
				return False
		elif len(checker_coordinate) == 5:
			if -90 <= int(checker_coordinate[1]) <= 90:
				if 0 <= float(checker_coordinate[2]) < 60:
					if -180 <= int(checker_coordinate[3]) <= 180:
						if 0 <= float(checker_coordinate[4]) < 60:
							return True
						else:
							return False
					else:
						return False
				else:
					return False
			else:
				return False
		else:
			return False
	else:
		return False

### 检查输入程序列表正确与否
def Checkprocedurelist(procedure):
	list_inputproc = procedure.split()
	name = list_inputproc[0]
	if name == "DONE":
		return True
	elif len(list_inputproc) == 2:
		next = list_inputproc[1]
		if 0 < len(name) <= 12:
			if 0 < len(next) <= 12:
				return True
			else:
				return False
		else:
			return False
	else:
		return False

### 航路点处理与存储
def Cookandstorecoordinate(rawcoordinate):
	raw_list = rawcoordinate.split()
	waypointname = raw_list[0]
	if len(raw_list) == 5:
		latitude_raw = int(raw_list[1]) + (float(raw_list[2])) / 60
		longitude_raw = int(raw_list[3]) + (float(raw_list[4])) / 60
		waypointlatitude = '%.6f' % latitude_raw
		waypointlongitude = '%.6f' % longitude_raw
		dict_coordinate [waypointname] = [waypointlatitude, waypointlongitude]
	elif len(raw_list) == 7:
		latitude_raw = int(raw_list[1]) + (int(raw_list[2]) + (float(raw_list[3]) / 60)) / 60
		longitude_raw = int(raw_list[4]) + (int(raw_list[5]) + (float(raw_list[6]) / 60)) / 60
		waypointlatitude = '%.6f' % latitude_raw
		waypointlongitude = '%.6f' % longitude_raw
		dict_coordinate [waypointname] = [waypointlatitude, waypointlongitude]

### 读取csv航路点坐标列表
def Readcoordinates(ICAOcode):
	dict_coordinate = {}
	list_coordinates = []
	dictgenerating = True
	index_key, index_value = 0, 1
	with open("{}.csv".format(ICAOcode), 'r') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			list_coordinates.append(row)
		list_coordinates = [str(value) for item in list_coordinates for value in item]#去除二级列表括号
		while dictgenerating:
			if index_key >= len(list_coordinates) or index_value >= len(list_coordinates):
				dictgenerating = False
			else:
				list_temporary = []
				list_temporary.append(list_coordinates[index_value])
				list_temporary.append(list_coordinates[index_value + 1])
				index_value += 3
				dict_coordinate [list_coordinates[index_key]] = list_temporary
				index_key += 3
	return dict_coordinate

### 导出csv航路点坐标列表
def Savecoordinates(ICAOcode, dict):
	list_coordinates = []
	csvgenerating = True
	index_key, index_value = 0, 0
	list_keys = list(dict.keys())
	list_values = list(dict.values())
	list_values = [str(value) for item in list_values for value in item]#去除二级列表括号
	while csvgenerating:
		list_temporary = []
		list_temporary.append(list_keys[index_key])
		index_key += 1
		list_temporary.append(list_values[index_value])
		list_temporary.append(list_values[index_value+1])
		index_value += 2
		list_coordinates += [list_temporary]
		if index_key == len(list_keys):
			csvgenerating = False
	with open("{}.csv".format(ICAOcode), "w", newline="") as csvfile:
		writer = csv.writer(csvfile)
		writer.writerows(list_coordinates)
	return print("{}航路点坐标列表已成功导出到程序所在目录！".format(ICAOcode))

### 生成程序列表：
def Generateprocedurelist(procedure):
	list_inputproc = procedure.split()
	name = list_inputproc[0]
	next = list_inputproc[1]
	list_tempproc.append("{}.{}".format(name, next))

### 航段类型识别
def Leg_classify(legtype, data):
	if legtype in list_legtype:
		if legtype == 'PI':
			Leg_PI(data)
		elif legtype == 'HA' or legtype == 'HF' or legtype == 'HM':
			Leg_HM(data)
		elif legtype == 'FM' or legtype == 'VM':
			Leg_FM/VM(data)
		elif legtype == 'AF':
			Leg_AF(data)
		elif legtype == 'CA' or legtype == 'VA':
			Leg_CA/VA(data)
		elif legtype == 'CD' or legtype == 'VD':
			Leg_CD/VD(data)
		elif legtype == 'CF':
			Leg_CF(data)
		elif legtype == 'CI' or legtype == 'VI':
			Leg_CI/VI(data)
		elif legtype == 'CR' or legtype == 'VR':
			Leg_CR/VR(data)
		elif legtype == 'DF':
			Leg_DF(data)
		elif legtype == 'FA':
			Leg_FA(data)
		elif legtype == 'FC':
			Leg_FC(data)
		elif legtype == 'FD':
			Leg_FD(data)
		elif legtype == 'RF':
			Leg_RF(data)
		elif legtype == 'TF' or legtype == 'IF':
			Leg_TF/IF(data)

### CA/VA航段
#def Leg_CA/VA():

# 主程序
### 航路点
status_coordinate = True
print('先将航路点名称和坐标录入程序！')
print('在本部分输入如下指令可使用额外功能：')
print('[read]----读取csv航路点列表\n[save]----导出csv航路点列表\n[done]----结束坐标输入并开始编写程序')
print('输入格式：[航路点名称] [纬度 度] [纬度 分] [【此项选填】纬度 秒] [经度 度] [经度 分] [【此项选填】经度 秒]')
print('注意各项之间以空格分开')
print('ovo让我们开始吧：')
dict_coordinate = {'名称':['纬度', '经度']}
while status_coordinate:
	rawcoordinate = input().upper()
	while not Checkcoordinate(rawcoordinate):
		rawcoordinate = input().upper()
	if rawcoordinate == "READ":
		readICAOcode = input("请输入机场ICAO代码：").upper()
		while readICAOcode == "":
			readICAOcode = input("机场ICAO代码不能为空！请重新输入：").upper()
		dict_coordinate = Readcoordinates(readICAOcode)
		print("{}航路点坐标列表读取成功！".format(readICAOcode))
	elif rawcoordinate == "SAVE":
		saveICAOcode = input("请输入机场ICAO代码：").upper()
		while saveICAOcode == "":
			saveICAOcode = input("机场ICAO代码不能为空！请重新输入：").upper()
		Savecoordinates(saveICAOcode, dict_coordinate)
	elif rawcoordinate == "DONE":
		status_coordinate = False
		for key_dict, value_dict in dict_coordinate.items():
			print('{:^5}\t{:^10}\t{:^11}'.format(key_dict, value_dict[0], value_dict[1]))
		print("\n航路点坐标现已暂存，下面开始生成程序列表！")
	else:
		Cookandstorecoordinate(rawcoordinate)

### 生成程序列表
status_list = True
print('在本部分输入如下指令可使用额外功能：')
print('[done]----结束坐标输入并选择模式')
print('输入格式：[当前程序名] [链接的程序或跑道]')
print('注意各项之间以空格分开')
print('ovo让我们开始吧：')
index_procedure = 0
list_procedure = ['[list]']
list_tempproc = []
while status_list:
	procedurelist = input().upper()
	while not Checkprocedurelist(procedurelist):
		procedurelist = input().upper()
	if procedurelist == "DONE":
		list_tempproc.sort()
		for item_tempproc in list_tempproc:
			list_procedure.append("Procedure.{}={}".format(index_procedure, item_tempproc))
			index_procedure += 1
		status_list = False
		for item_procedure in list_procedure:
			print(item_procedure)
		print("\n程序列表现已暂存，下面开始写程序！")
	else:
		Generateprocedurelist(procedurelist)

### 编写程序
#status_leg = True
#status_procdure = True
#print('在本部分输入如下指令可使用额外功能：')
#print('[ok]------结束编写当前程序，开始编写下一程序')
#print('[done]----结束程序编写并导出程序')
#print('ovo让我们开始吧：')
#print('输入①：[当前程序名] [链接的程序或跑道]')
#print('注意各项之间以空格分开')
