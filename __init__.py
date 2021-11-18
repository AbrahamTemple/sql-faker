# https://dormousehole.readthedocs.io/en/latest/quickstart.html
from flask import Flask, request, render_template
from faker import Faker 
import json
import hashlib
import random
import os

# https://www.cnblogs.com/python666666/p/9980243.html
# https://zhuanlan.zhihu.com/p/87203290
fake = Faker(locale='zh_CN')  

# 随机生成验证码
def verify():
    code_list = []
    for i in range(2):
        random_num = random.randint(0, 9) # 随机生成0-9的数字
        # 利用random.randint()函数生成一个随机整数a，使得65<=a<=90
        # 对应从“A”到“Z”的ASCII码
        a = random.randint(65, 90)
        b = random.randint(97, 122)
        random_uppercase_letter = chr(a)
        random_lowercase_letter = chr(b)
        code_list.append(str(random_num))
        code_list.append(random_uppercase_letter)
        code_list.append(random_lowercase_letter)
    verification_code = ''.join(code_list)
    return verification_code

# 策略方法：选择假数据值可以重复且不需要确定长度
def strategy(cmd) :
	if cmd == 1:
		return fake.name()
	elif cmd == 2:
		return fake.address()
	elif cmd == 3:
		return fake.phone_number()
	elif cmd == 4:
		return fake.ssn(min_age=18, max_age=90)
	elif cmd == 5:
		return fake.random_int(100,999)
	else:
		return None
		
# 返回最终字典
def build(li=[],idx=[]) :
	fake_list = list(map(strategy, li))
	fake_dict = dict(zip(idx,fake_list))
	return fake_dict
	# arr = list(map(strategy, li))
	# return list(filter(None, arr)) # 去除空元素的列表

app = Flask(__name__)

# 表单页面
@app.route('/')
@app.route('/<name>')
def faker_home(name=None):
	return render_template('form.html', name=name)
	
# 下载页面
@app.route('/down', methods=['POST', 'GET'])
def faker_down(cmd=[], feild=[], count=0):
	if request.method == "GET":
		cmd = request.args.getlist("c")
		feild = request.args.getlist("n")
		count = int(request.args.get("count"))
	li = list(map(int,cmd))
	builds = []
	for i in range(0,count):
		builds.append(build(li,feild))
	filename = "faker_json/{}.json".format(hashlib.md5(verify().encode(encoding='UTF-8')).hexdigest())
	with open(filename,'w+') as fw:
		json.dump(builds,fw,ensure_ascii=False)
	link = "http://localhost:5000/file/{}".format(filename)
	return render_template('down.html', link=link)

@app.route('/file/string:<filename>', methods=['POST', 'GET'])
def faker_file(filename):
	return f'{escape(filename)}'
	#return send_from_directory(os.path.dirname(__file__),filename=request.args.getlist("path"),as_attachment=True)

@app.route('/fake', methods={'POST','GET'})
def faker_build(cmd=[], feild=[], count=0):
	if request.method == "GET":
		cmd = request.args.getlist("c")
		feild = request.args.getlist("n")
		count = int(request.args.get("count"))
	li = list(map(int,cmd))
	builds = []
	for i in range(0,count):
		builds.append(build(li,feild))
	return "{}".format(builds) #json字符串

if __name__ == "__main__":
    app.run(port=5000, debug=True)