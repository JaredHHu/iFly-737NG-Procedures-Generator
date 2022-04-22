#外部库
import csv

#基础项
dict_coordinate = {'名称':['纬度', '经度']}
judge_coordinate = True

#软件信息
print("iFly飞行程序数据文件生成器\n")
print("当前版本：0.1.0.0\n")
print("更新日志：")
print("0.1.0.0  2022.04.22  实现坐标的检查、转换与存储\n")
print("Github仓库：https://github.com/JaredHHu/iFly-737NG-Procedures-Generator\n")

#函数
###检查输入航路点正确与否
def Checkcoordinate(rawcoordinate):
	checker_coordinate = rawcoordinate.split()
	if checker_coordinate[0] == "READ" or checker_coordinate[0] == "SAVE" or checker_coordinate[0] == "FINISH":
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

###航路点处理与存储
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
	return

###读取csv航路点坐标列表
def Readcoordinates(readICAOcode):
	dict_coordinate = {}
	list_coordinates = []
	dictgenerating = True
	index_key, index_value = 0, 1
	with open("{}.csv".format(readICAOcode), 'r') as csvfile:
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
	print(dict_coordinate)
	print("{}航路点坐标列表读取成功！".format(readICAOcode))
	return dict_coordinate

###导出csv航路点坐标列表
def Savecoordinates(saveICAOcode, data):
	list_coordinates = []
	csvgenerating = True
	index_key, index_value = 0, 0
	list_keys = list(data.keys())
	list_values = list(data.values())
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
	with open("{}.csv".format(saveICAOcode), "w", newline="") as csvfile:
		writer = csv.writer(csvfile)
		writer.writerows(list_coordinates)
	return print("{}航路点坐标列表已成功导出到程序所在目录！".format(saveICAOcode))

#主程序
###航路点
print('先将航路点名称和坐标录入程序！')
print('在本部分输入如下指令可使用额外功能：')
print('[read]----读取csv航路点列表\n[save]----导出csv航路点列表\n[finish]--结束坐标输入并开始编写程序')
print('输入格式：[航路点名称] [纬度 度] [纬度 分] [【此项选填】纬度 秒] [经度 度] [经度 分] [【此项选填】经度 秒]')
print('注意各项之间以空格分开')
print('让我们开始吧ovo\n请输入航点和坐标：')
status_coordinate = True
while status_coordinate:
	rawcoordinate = input().upper()
	while not Checkcoordinate(rawcoordinate):
		rawcoordinate = input().upper()
	if rawcoordinate == "READ":
		readICAOcode = input("请输入机场ICAO代码：").upper()
		while readICAOcode == "":
			readICAOcode = input("机场ICAO代码不能为空！请重新输入：").upper()
		dict_coordinate = Readcoordinates(readICAOcode)
	elif rawcoordinate == "SAVE":
		saveICAOcode = input("请输入机场ICAO代码：").upper()
		while saveICAOcode == "":
			ICAOcode = input("机场ICAO代码不能为空！请重新输入：").upper()
		Savecoordinates(saveICAOcode, dict_coordinate)
	elif rawcoordinate == "FINISH":
		for key_dict, value_dict in dict_coordinate.items():
			print('{:^5}\t{:^10}\t{:^11}'.format(key_dict, value_dict[0], value_dict[1]))
			status_coordinate = False
	Cookandstorecoordinate(rawcoordinate)
