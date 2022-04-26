# 外部库
import csv
import os

#基本信息
list_legtype = ['PI', 'HA', 'HF', 'HM', 'FM', 'VM', 'AF', 'CA', 'VA', 'CD', 'VD', 'CF',
				'CI', 'VI', 'CR', 'VR', 'DF', 'FA', 'FC', 'FD', 'RF', 'TF', 'IF']
list_filetype = ['TXT', 'SID', 'SIDTRS', 'STAR', 'STARTRS', 'APP', 'APPTRS', 'SUPP']
list_turn = ['', 'L', 'R']
list_one = ['', '1']

# 软件信息
print('iFly Jets ADV Series 飞行程序数据文件生成器\n')
print('当前版本：3.1.3\n')
print('更新日志：')
print('1.0.0  2022.04.22  实现坐标的检查、转换、读取和存储')
print('2.0.0  2022.04.23  实现程序列表的检查、排序和生成')
print('3.0.0  2022.04.23  实现根据航段类型生成程序')
print('                   实现合并数据，分类导出')
print('3.1.0  2022.04.24  实现程序列表的读取和存储')
print('                   修复一堆 bug')
print('3.1.1  2022.04.25  修复程序列表存储后再读取会出现程序重复的问题')
print('3.1.2  2022.04.26  修复部分输入为空时程序闪退的问题')
print('3.1.3  2022.04.27  实现对文件类型、转弯方向、0或1输入的检查与限制')
print('                   修复部分会导致闪退的 bug')
print('                   修复导出类型无法输入的 bug')
print('                   修复不能导出 .apptrs 文件的 bug')
print('                   调整文本排版')

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
	if name == 'DONE' or name == 'OK' or name == 'SAVE' or name == 'READ':
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
	with open('Waypoint_{}.csv'.format(ICAOcode), 'r') as csvfile:
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
	with open('Waypoint_{}.csv'.format(ICAOcode), 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerows(list_coordinates)
	return print('{} 航路点坐标列表已成功导出到程序所在目录！'.format(ICAOcode))

### 读取txt程序列表
def Readproclist(ICAOcode):
	with open('List_{}.txt'.format(ICAOcode, 'r')) as file:
		list_procedure = file.read().splitlines()
		return list_procedure

### 导出txt程序列表
def Saveproclist(ICAOcode, proclist):
	index_procedure = 0
	proclist.sort()
	with open('List_{}.txt'.format(ICAOcode), 'w') as file:
		file.write('[list]')
		file.write('\n')
		for item_tempproc in proclist:
			file.write('Procedure.{}={}'.format(index_procedure, item_tempproc))
			file.write('\n')
			index_procedure += 1

### 生成程序列表：
def Generateprocedurelist(procedure):
	list_inputproc = procedure.split()
	name = list_inputproc[0]
	next = list_inputproc[1]
	list_tempproc.append("{}.{}".format(name, next))

### 航段类型识别
def Leg_classify(legtype):
	if legtype == 'PI':
		print('模式暂不可用')
		legdata = ['{}航段暂无法生成'.format(legtype)]
		#legdata = Leg_PI(legtype)
		return legdata
	elif legtype == 'HA' or legtype == 'HF' or legtype == 'HM':
		legdata = Leg_HAHFHM(legtype)
		return legdata
	elif legtype == 'FM' or legtype == 'VM':
		print('模式暂不可用')
		legdata = ['{}航段暂无法生成'.format(legtype)]
		#legdata = Leg_FMVM(legtype)
		return legdata
	elif legtype == 'AF':
		legdata = Leg_AF(legtype)
		return legdata
	elif legtype == 'CA' or legtype == 'VA':
		legdata = Leg_CAVA(legtype)
		return legdata
	elif legtype == 'CD' or legtype == 'VD':
		print('模式暂不可用')
		legdata = ['{}航段暂无法生成'.format(legtype)]
		#legdata = Leg_CDVD(legtype)
		return legdata
	elif legtype == 'CF':
		legdata = Leg_CF(legtype)
		return legdata
	elif legtype == 'CI' or legtype == 'VI':
		print('模式暂不可用')
		legdata = ['{}航段暂无法生成'.format(legtype)]
		#legdata = Leg_CIVI(legtype)
		return legdata
	elif legtype == 'CR' or legtype == 'VR':
		print('模式暂不可用')
		legdata = ['{}航段暂无法生成'.format(legtype)]
		#legdata = Leg_CRVR(legtype)
		return legdata
	elif legtype == 'DF':
		legdata = Leg_DF(legtype)
		return legdata
	elif legtype == 'FA':
		print('模式暂不可用')
		legdata = ['{}航段暂无法生成'.format(legtype)]
		#legdata = Leg_FA(legtype)
		return legdata
	elif legtype == 'FC':
		print('模式暂不可用')
		legdata = ['{}航段暂无法生成'.format(legtype)]
		#legdata = Leg_FC(legtype)
		return legdata
	elif legtype == 'FD':
		print('模式暂不可用')
		legdata = ['{}航段暂无法生成'.format(legtype)]
		#legdata = Leg_FD(legtype)
		return legdata
	elif legtype == 'RF':
		legdata = Leg_RF(legtype)
		return legdata
	elif legtype == 'TF' or legtype == 'IF':
		legdata = Leg_TFIF(legtype)
		return legdata

### 根据航路点名称自动获取坐标
def Getcoordinate():
	waypoint = input('航路点名称：').upper()
	while waypoint not in dict_coordinate:
		waypoint = input('该航路点不存在于数据库中！航路点名称：').upper()
	list_wpt = ['{}'.format(waypoint)] + dict_coordinate.get(waypoint)
	return list_wpt

### 根据中心点名称自动获取坐标
def Getcentercoordinate():
	centerwaypoint = input('RF航段中心点名称：').upper()
	while centerwaypoint not in dict_coordinate:
		centerwaypoint = input('该航路点不存在于数据库中！RF航段中心点名称：').upper()
	list_ctrwpt = dict_coordinate.get(centerwaypoint)
	return list_ctrwpt

### HA/HF/HM航段
def Leg_HAHFHM(legtype):
	list_legdata = ['Leg={}'.format(legtype)]
	coordinate = Getcoordinate()
	cross = input('*飞越填1：')
	while cross not in list_one:
		cross = input('输入错误！*飞越填1：')
	heading = input('磁航向：')
	while heading == "":
		heading = input('不能为空！磁航向：')
	turn = input('转弯指示(L/R)：').upper()
	while turn not in list_turn:
		turn = input('输入错误！转弯指示(L/R)：').upper()
	altitude = input('*英尺高度：').upper()
	speed = input('*速度限制(节)：').upper()
	dist = input('等待边距离(海里)或时间(分钟×10000)：')
	while dist == '':
		dist = input('不能为空！等待边距离(海里)或时间(分钟×10000)：')
	list_legdata.append('Name={}'.format(coordinate[0]))
	list_legdata.append('Latitude={}'.format(coordinate[1]))
	list_legdata.append('Longitude={}'.format(coordinate[2]))
	list_legdata.append('Heading={}'.format(heading))
	list_legdata.append('Dist={}'.format(dist))
	if cross != '':
		list_legdata.append('CrossThisPoint=1')
	if turn != '':
		list_legdata.append('TurnDirection={}'.format(turn))
	if altitude != '':
		list_legdata.append('Altitude={}'.format(altitude))
	if speed != '':
		list_legdata.append('Speed={}'.format(speed))
	return list_legdata

### AF航段
def Leg_AF(legtype):
	list_legdata = ['Leg=AF']
	coordinate = Getcoordinate()
	frequency = input('DME台代码：').upper()
	while frequency == '':
		frequency = input('不能为空！DME台代码：').upper()
	navdist = input('相对DME台距离(海里)：')
	while navdist == '':
		navdist = input('不能为空！相对DME台距离(海里)：')
	cross = input('*飞越填1：')
	while cross not in list_one:
		cross = input('输入错误！*飞越填1：')
	altitude = input('*英尺高度：').upper()
	speed = input('*速度限制(节)：').upper()
	list_legdata.append('Name={}'.format(coordinate[0]))
	list_legdata.append('Latitude={}'.format(coordinate[1]))
	list_legdata.append('Longitude={}'.format(coordinate[2]))
	list_legdata.append('Frequency={}'.format(frequency))
	list_legdata.append('NavDist={}'.format(navdist))
	if cross != '':
		list_legdata.append('CrossThisPoint=1')
	if altitude != '':
		list_legdata.append('Altitude={}'.format(altitude))
	if speed != '':
		list_legdata.append('Speed={}'.format(speed))
	return list_legdata

### CA/VA航段
def Leg_CAVA(legtype):
	list_legdata = ['Leg={}'.format(legtype)]
	heading = input('磁航向：')
	while heading == '':
		heading = input('不能为空！磁航向：')
	altitude = input('英尺高度：').upper()
	while altitude == '':
		altitude = input('不能为空！英尺高度：').upper()
	speed = input('*速度限制(节)：').upper()
	list_legdata.append('Heading={}'.format(heading))
	list_legdata.append('Altitude={}'.format(altitude))
	if speed != '':
		list_legdata.append('Speed={}'.format(speed))
	return list_legdata

### CF航段
def Leg_CF(legtype):
	list_legdata = ['Leg=CF']
	coordinate = Getcoordinate()
	cross = input('*飞越填1：')
	while cross not in list_one:
		cross = input('输入错误！*飞越填1：')
	heading = input('磁航向：')
	while heading == '':
		heading = input('不能为空！磁航向：')
	altitude = input('*英尺高度：').upper()
	speed = input('*速度限制(节)：').upper()
	list_legdata.append('Name={}'.format(coordinate[0]))
	list_legdata.append('Latitude={}'.format(coordinate[1]))
	list_legdata.append('Longitude={}'.format(coordinate[2]))
	list_legdata.append('Heading={}'.format(heading))
	if cross != '':
		list_legdata.append('CrossThisPoint=1')
	if altitude != '':
		list_legdata.append('Altitude={}'.format(altitude))
	if speed != '':
		list_legdata.append('Speed={}'.format(speed))
	return list_legdata

### DF航段
def Leg_DF(legtype):
	list_legdata = ['Leg=DF']
	coordinate = Getcoordinate()
	cross = input('*飞越填1：')
	while cross not in list_one:
		cross = input('输入错误！*飞越填1：')
	turn = input('*转弯指示(L/R)：').upper()
	while turn not in list_turn:
		turn = input('输入错误！*转弯指示(L/R)：').upper()
	altitude = input('*英尺高度：').upper()
	speed = input('*速度限制(节)：').upper()
	list_legdata.append('Name={}'.format(coordinate[0]))
	list_legdata.append('Latitude={}'.format(coordinate[1]))
	list_legdata.append('Longitude={}'.format(coordinate[2]))
	if cross != '':
		list_legdata.append('CrossThisPoint=1')
	if turn != '':
		list_legdata.append('TurnDirection={}'.format(turn))
	if altitude != '':
		list_legdata.append('Altitude={}'.format(altitude))
	if speed != '':
		list_legdata.append('Speed={}'.format(speed))
	return list_legdata

### RF航段
def Leg_RF(legtype):
	list_legdata = ['Leg=RF']
	coordinate = Getcoordinate()
	heading = input('*磁航向：')
	turn = input('*转弯指示(L/R)：').upper()
	while turn not in list_turn:
		turn = input('输入错误！*转弯指示(L/R)：').upper()
	altitude = input('*英尺高度：').upper()
	speed = input('*速度限制(节)：').upper()
	centercoordinate = Getcentercoordinate()
	list_legdata.append('Name={}'.format(coordinate[0]))
	list_legdata.append('Latitude={}'.format(coordinate[1]))
	list_legdata.append('Longitude={}'.format(coordinate[2]))
	if heading != '':
		list_legdata.append('Heading={}'.format(heading))
	if turn != '':
		list_legdata.append('TurnDirection={}'.format(turn))
	if altitude != '':
		list_legdata.append('Altitude={}'.format(altitude))
	if speed != '':
		list_legdata.append('Speed={}'.format(speed))
	list_legdata.append('CenterLat={}'.format(centercoordinate[0]))
	list_legdata.append('CenterLon={}'.format(centercoordinate[1]))
	return list_legdata

### TF/IF航段
def Leg_TFIF(legtype):
	list_legdata = ['Leg={}'.format(legtype)]
	coordinate = Getcoordinate()
	cross = input('*飞越填1：')
	while cross not in list_one:
		cross = input('输入错误！*飞越填1：')
	altitude = input('*英尺高度：').upper()
	speed = input('*速度限制(节)：').upper()
	mapt = input('*复飞点填1：')
	while mapt not in list_one:
		mapt = input('输入错误！*复飞点填1：')
	slope = input('*航径坡度：')
	list_legdata.append('Name={}'.format(coordinate[0]))
	list_legdata.append('Latitude={}'.format(coordinate[1]))
	list_legdata.append('Longitude={}'.format(coordinate[2]))
	if cross != '':
		list_legdata.append('CrossThisPoint=1')
	if altitude != '':
		list_legdata.append('Altitude={}'.format(altitude))
	if speed != '':
		list_legdata.append('Speed={}'.format(speed))
	if mapt != '':
		list_legdata.append('MAP=1')
	if mapt != '':
		list_legdata.append('Slope={}'.format(slope))
	return list_legdata

### 输出结果
def Outputdata(filetype, ICAOcode, data):
	with open('{}.txt'.format(ICAOcode), 'w') as file_output:
		for item in data:
			file_output.write(item)
			file_output.write('\n')
	if filetype == 'SID':
		os.rename('{}.txt'.format(ICAOcode), '{}.sid'.format(ICAOcode))
		print('数据已保存为 {}.sid'.format(ICAOcode))
	elif filetype == 'SIDTRS':
		os.rename('{}.txt'.format(ICAOcode), '{}.sidtrs'.format(ICAOcode))
		print('数据已保存为 {}.sidtrs'.format(ICAOcode))
	elif filetype == 'STAR':
		os.rename('{}.txt'.format(ICAOcode), '{}.star'.format(ICAOcode))
		print('数据已保存为 {}.star'.format(ICAOcode))
	elif filetype == 'STARTRS':
		os.rename('{}.txt'.format(ICAOcode), '{}.startrs'.format(ICAOcode))
		print('数据已保存为 {}.startrs'.format(ICAOcode))
	elif filetype == 'APP':
		os.rename('{}.txt'.format(ICAOcode), '{}.app'.format(ICAOcode))
		print('数据已保存为 {}.app'.format(ICAOcode))
	elif filetype == 'APPTRS':
		os.rename('{}.txt'.format(ICAOcode), '{}.apptrs'.format(ICAOcode))
		print('数据已保存为 {}.apptrs'.format(ICAOcode))
	else:
		print('数据已保存为 {}.txt'.format(ICAOcode))

# 主程序
### 航路点
status_coordinate = True
print('\n先将航路点名称和坐标录入程序！')
print('在本部分输入如下指令可使用额外功能：')
print('    [read]————读取csv航路点列表\n    [save]————导出csv航路点列表\n    [done]————结束坐标输入并开始编写程序')
print('输入格式：[航路点名称] [纬度 度] [纬度 分] 【纬度 秒】 [经度 度] [经度 分] 【经度 秒】')
print('注意：①秒数据可不填\n     ②各项之间以空格分开')
print('ovo让我们开始吧：')
dict_coordinate = {'名称':['纬度', '经度']}
while status_coordinate:
	rawcoordinate = input().upper()
	while not Checkcoordinate(rawcoordinate):
		rawcoordinate = input().upper()
	if rawcoordinate == 'READ':
		readICAOcode = input('机场ICAO代码：').upper()
		while readICAOcode == '':
			readICAOcode = input('不能为空。机场ICAO代码：').upper()
		dict_coordinate = Readcoordinates(readICAOcode)
		print('{}航路点坐标列表读取成功！'.format(readICAOcode))
	elif rawcoordinate == 'SAVE':
		saveICAOcode = input('机场ICAO代码：').upper()
		while saveICAOcode == '':
			saveICAOcode = input('不能为空！机场ICAO代码：').upper()
		Savecoordinates(saveICAOcode, dict_coordinate)
	elif rawcoordinate == 'DONE':
		status_coordinate = False
		for key_dict, value_dict in dict_coordinate.items():
			print('{:^5}\t{:^10}\t{:^11}'.format(key_dict, value_dict[0], value_dict[1]))
		print('\n航路点坐标现已暂存，下面开始生成程序列表！')
	else:
		Cookandstorecoordinate(rawcoordinate)

### 生成程序列表
status_list = True
print('在本部分输入如下指令可使用额外功能：')
print('    [read]————读取程序列表\n    [save]————导出程序列表\n    [done]————结束坐标输入并选择模式')
print('输入格式：[当前程序名] [链接的程序或跑道]')
print('注意：各项之间以空格分开')
print('针对进近程序代码的说明：[R]--RNP  [I]--ILS  [V]--VOR  [N]--NDB')
print('               示例：[I16]--ILS 16  [I32-Z]--ILSZ 32  [R34]--RNP 34')
print('ovo让我们开始吧：')
index_procedure = 0
list_procedure = ['[list]']
list_tempproc = []
while status_list:
	procedurelist = input().upper()
	while not Checkprocedurelist(procedurelist):
		procedurelist = input().upper()
	if procedurelist == 'DONE':
		list_tempproc.sort()
		for item_tempproc in list_tempproc:
			list_procedure.append('Procedure.{}={}'.format(index_procedure, item_tempproc))
			index_procedure += 1
		status_list = False
		for item_procedure in list_procedure:
			print(item_procedure)
		print('\n程序列表现已暂存，下面开始写程序！')
	elif procedurelist == 'READ':
		readICAOcode = input('机场ICAO代码：').upper()
		while readICAOcode == '':
			readICAOcode = input("不能为空。机场ICAO代码：").upper()
		list_procedure = Readproclist(readICAOcode)
		list_tempproc = []
		print('{}程序列表读取成功！'.format(readICAOcode))
	elif procedurelist == 'SAVE':
		saveICAOcode = input('机场ICAO代码：').upper()
		while saveICAOcode == '':
			saveICAOcode = input("不能为空！机场ICAO代码：").upper()
		Saveproclist(saveICAOcode, list_tempproc)
		print('{} 程序列表已成功导出到程序所在目录！'.format(saveICAOcode))
	else:
		Generateprocedurelist(procedurelist)

### 编写程序
status_leg = True
print('在本部分输入如下指令可使用额外功能：')
print('    [ok]------结束编写当前程序，开始编写下一程序\n    [done]----结束程序编写并导出程序')
#print('[supp]----跳过此步骤，编写补充文件')
print('针对进近程序的代码说明：[R]--RNP  [I]--ILS  [V]--VOR  [N]--NDB')
print('               示例：[I16]--ILS 16  [I32-Z]--ILSZ 32  [R34]--RNP 34')
print('ovo让我们开始吧：')
list_procdata = []
while status_leg:
	status_procdata = True
	index_procdata = 0
	procname = input('程序名称和下一程序或跑道：').upper()
	#if procname == 'SUPP':

	if procname == 'DONE':
		status_leg = False
		print('\n选择想输出的数据类型并导出！')
		break
	while not Checkprocedurelist(procname):
		procname = input('格式错误。程序名称和下一程序或跑道：').upper()
	list_procname = procname.split()
	data_name = list_procname[0]
	data_next = list_procname[1]
	index_data = 0
	while status_procdata:
		legtype = input('航段类型：').upper()
		while legtype not in list_legtype and legtype != 'OK' and legtype != 'DONE':
			legtype = input('类型错误。航段类型：').upper()
		print('带"*"项目选填')
		if legtype == 'OK':
			status_procdata = False
			print('\n此段程序现已暂存，开始输入下一段程序！')
		elif legtype == 'DONE':
			status_procdata = False
			status_leg = False
			print('\n程序现已暂存，下面选择想输出的数据类型并导出！')
		else:
			list_procdata.append('[{}.{}.{}]'.format(data_name, data_next, index_data))
			legdata = Leg_classify(legtype)
			list_procdata.extend(legdata)
			index_data += 1

###输出数据
status_output = True
print('可输出文件类型：\n[txt]--.txt\n[sid]--.sid\n[sidtrs]--.sidtrs\n[star]--.star\n[startrs]--.startrs\n[app]--.app\n[apptrs]--.apptrs')
list_output = []
list_output.extend(list_procedure)
list_output.extend(list_procdata)
filetype = input('输出文件类型：').upper()
while filetype not in list_filetype:
	filetype = input('类型错误！输出文件类型：').upper()
ICAOcode = input('机场ICAO代码：').upper()
while ICAOcode == '':
	ICAOcode = input('不能为空！机场ICAO代码：').upper()
Outputdata(filetype, ICAOcode, list_output)
