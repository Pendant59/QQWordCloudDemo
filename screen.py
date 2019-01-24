# -*- coding: utf-8 -*-
import jieba
from wordcloud import WordCloud # 生成词云
import matplotlib.pyplot as plt # plt 用于显示图片预览
import codecs
import re
from collections import Counter # 统计list各个元素出现的次数

plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False # 用来正常显示负号

def screen(filenname = 'record'):
	""" 数据清洗 """
	# 读取记录文件
	try:
		file = codecs.open('./resource/' + filenname + '.txt', 'r', 'utf-8')
		line_list = [line for line in file]
		file.close()
	except Exception as e:
		print(e)
		return 
	
	# 内容
	content = codecs.open('./result_txt/content.txt', 'w', 'utf-8')
	# 时间
	time = codecs.open('./result_txt/time.txt', 'w', 'utf-8')
	# 用户
	user = codecs.open('./result_txt/user.txt', 'w', 'utf-8')
	# 用户群等级
	lv	= codecs.open('./result_txt/lv.txt', 'w', 'utf-8')
	# 获取 日期 时间 昵称 规则 
	header_rule = re.compile(r'(201[89]-\d{2}-\d{2})\s(\d{2}:\d{2}:\d{2})\s(【.*?】){0,1}(.*?)[\(<]')
	# 获取内容 规则
	content_rule = re.compile(r'(?!201)(?=\S)(.*)\r')
	# 去掉记录前8行文件说明
	for v in line_list[8:]:
		header_res = header_rule.findall(v)
		if header_res:  # 头部逻辑
			# 写入时间
			time.write(header_res[0][1][0:2] + '\n')
			# 写入用户 - 去除从开头包含6个以上数字的昵称(QQ?) 去除没有昵称的(已退群)
			if not re.match(r'\d{6,}', header_res[0][3]) and header_res[0][3] and header_res[0][3] != 'null' :
				user.write(header_res[0][3] + '\n')
			# 用户群等级
			if  header_res[0][2]:
				lv.write(header_res[0][2] + '\n')
		else:  # 内容逻辑
			content_res = content_rule.match(v)
			if content_res:
				content.write(content_res.group(0))

	content.close()
	time.close()
	user.close()
	lv.close()

def cloud(img_type='content'):
	""" 词云统计 """

	if img_type not in ['content', 'user']:
		return "Only 'content' and  'user' are available"

	file = codecs.open('./result_txt/'+img_type+'.txt', 'r', 'utf-8')
	cut_text="".join(jieba.cut(file.read()))

	#词云背景图片白底 
	wordcloud = WordCloud(
		width = 600,
		height = 800,
		background_color = "white",
		font_path = "./resource/simhei.ttf",
		stopwords = ['图片', '表情', '系统消息'],
		max_words = 200).generate_from_text(cut_text)
	
	wordcloud.to_file('./result_img/'+img_type+'.jpg')
	
	# 生成预览图片
	# plt.figure()
	# plt.imshow(wordcloud)  # 用plt显示图片
	# plt.axis('off')# 不显示坐标轴
	# plt.show()  # 显示图片

def line_broken(line_type='user'):
	""" 活跃度折线图 """
	if line_type == 'user':
		x_name = '活跃成员前10'
		y_name = '发言次数'
		title = '2018/5-2019/1群成员活跃度'
		img = './user_active.jpg'

		max_num = 10

	elif line_type == 'lv':
		x_name = '群等级'
		y_name = '发言次数'
		title = '2018/5-2019/1群内等级活跃度'
		img = './lv_active.jpg'

		max_num = None

	elif line_type == 'time':
		x_name = '24小时制'
		y_name = '发言次数'
		title = '2018/5-2019/1每日时段活跃度'
		img = './time_active.jpg'

		max_num = 24
	else:
		print('Useless'+line_type)
		return

	file = codecs.open('./result_txt/' + line_type + '.txt', 'r', 'utf-8')
	# 用户名集合
	line_list = [line.rstrip("\n") for line in file]
	file.close()

	# 统计数据 
	if not max_num:
		max_num = len(set(line_list))
	count_res = Counter(line_list).most_common(max_num)
	
	# 统计数据结果
	lv_dict = dict()
	for v in count_res:
		lv_dict[v[0].replace(' ','')] = v[1]
	# 时间排序
	if line_type == 'time':
		lv_dict	= { v:lv_dict[v] for v in sorted(lv_dict)}

	plt.figure() 

	x_ticks = list(lv_dict.keys())
	y_ticks = list(lv_dict.values())

	fig, axs = plt.subplots(1, 1, figsize=(12, 4), dpi=100)
	# 设置坐标轴名称
	plt.xlabel(x_name)
	plt.ylabel(y_name)
	# 画柱状图
	axs.plot(x_ticks, y_ticks)
	
	plt.title(title)
	plt.savefig(img)
	plt.close()



if __name__ == '__main__':
	pass
	# 处理群数据
	screen('record')
	# 生成内容词云
	cloud('content')
	# 生成活跃用户词云
	cloud('user')
	# 生成 用户-级别-活跃时间折线，柱状图
	line_broken('user')
	line_broken('lv')
	line_broken('time')
