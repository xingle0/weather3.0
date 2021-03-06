# coding=utf-8
import urllib.request
import json
# from pymysql import *
import sys
import re
# from pypinyin import *
from PIL import Image,ImageDraw,ImageFont
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
from datetime import datetime,timedelta


# # 利用正则获取目标字符串中的地点和时间
# pattern="(?P<市>\w+市)(?P<区>\w+[区,县])(?P<时间>\w天)天气"
# s = '西安市碑林区今天天气'
# regex = re.compile(pattern)
# it = regex.findall(s)
# print(it)
# localtion1=it[0][0]
# localtion2=it[0][1]

# #利用mysql查询获得城市代码code
# s1=localtion1
# s2=localtion2
# host = '127.0.0.1'
# # port = 3306
# user = 'root'
# password = '123456'
# dbname = 'cityinfo'
# # 将汉字转化成拼音
# test1=pinyin(s1,style=NORMAL)
# print(test1)
# test1=test1[0]+test1[1]
# s1=''.join(test1)
# test2=pinyin(s2,style=NORMAL)
# print(test2)
# test2=test2[0]+test2[1]
# s2=''.join(test2)

def main():

    # try:
    #     conn = connect(host,user,password,dbname)
    # except Exception as e:
    #     print(e)
    # cursor = conn.cursor()
    # sql = 'select id from city where leaderEn = "%s" and cityEn = "%s"'%(s1,s2)
    # print(sql)
    # # sql = 'select id from city where cityEn = "beijing"'
    # try:
    #     cursor.execute(sql)
    # except Exception as e:
    #     print(e)
    #     return
    # result = cursor.fetchone()
    # print(result)
    # cursor.close()
    # conn.close()
    # code = result[0]
    
    # 1.查询城市id 
    s = "碑林"
    #　打开json文件 
    with open("/home/tarena/wea_project/weather/weather_id.json") as f:
        # 读取json文件内容
        city_list = json.load(f)
        #　关闭json文件
        f.close()
    # 根据城市名获取城市id
    for i in city_list:
        if s == i['cityZh'] or s == i['provinceZh']:
            city_id = i['id']
            break   
    code = city_id
    
    # 2.调用天气接口查询天气
    # 将城市id拼接到查询天气的url上
    url='https://www.tianqiapi.com/api/?version=v1&cityid=%s'% code
    # 获取url请求对象
    obj=urllib.request.urlopen(url)
    # 读取url请求内容
    data_b=obj.read()
    # 将url内容的二进制编码转换成utf-8编码类型
    data_s=data_b.decode('utf-8')
    # 将json串转换成dict
    data_dict=json.loads(data_s)
    # # 2. 将查询结果存到文件里
    # with open('/home/tarena/wea_project/weather/wea_request.json','w') as f:
    #     f.write(data_s)
    #     f.close()
    
    # # 读取json文件中的内容
    # with open('/home/tarena/wea_project/weather/wea_request.json') as f:
    #     # 将json字典转换成dict
    #     data_dict = json.load(f)
    #     f.close()
    
    # print(len(data_dict))
    # print(type(data_dict))
    # for k,v in data_dict.items():
    #     print(k,v)
    # print(len(data_dict['data'][0]))
    # print(len(data_dict['data']))
    # print(type(data_dict['data']))
    wea_hour = []
    wea_tem = []
    for w in data_dict['data'][0:3]:
        for h in w['hours']:
            wea_hour.append(h['day'])
            wea_tem.append(h['tem'])
    # for k,v in data_dict['data'][0].items():
    #     print(k,v)
    rt =data_dict['data'][0]
    my_rt=('%s天气：%s,温度范围:%s~%s，当前温度:%s')% (data_dict['city'],rt['wea'],rt['tem2'],rt['tem1'],rt['tem'])
    print(my_rt)
    print([int(hour["day"][-3:-1]) for hour in data_dict['data'][0]['hours']])
    print([int(hour["tem"][:-1]) for hour in data_dict['data'][0]['hours']])

    # 添加背景图片
    im = Image.open("/home/tarena/project/WxRobot/utils/weather/background.jpg")
    # 创建一个新的图片
    txt = Image.new('RGBA',im.size,(0,0,0,0))
    # 新建绘图对象
    draw = ImageDraw.Draw(txt)
    # 获取图像的宽和高
    width,height = txt.size
    # 选择文字的字体和大小
    setFont = ImageFont.truetype('/home/tarena/wea_project/weather/simhei.ttf',20)
    # 设置文字颜色
    fillColor = (255,0,0,255)
    # 写入文字
    draw.text((40,30),'地点:'+data_dict['city'],font=setFont,fill=fillColor)
    draw.text((40,70),'时间:'+rt['date'],font=setFont,fill=fillColor)
    draw.text((40,110),'天气:'+rt['wea'],font=setFont,fill=fillColor)
    draw.text((40,150),'现在温度:'+rt['tem'],font=setFont,fill=fillColor)
    draw.text((40,190),'温度范围:'+rt['tem2']+'-'+rt['tem1'],font=setFont,fill=fillColor)
    draw.text((40,230),'出行建议:'+rt['air_tips'],font=setFont,fill=fillColor)
    # 添加图片
    mark = Image.open("/home/tarena/project/WxRobot/utils/weather/robot.ico")
    txt.paste(mark,(im.size[0]-200,100))
    # 结合背景图和文字
    out = Image.composite(txt,im,txt)
    # 展示图片
    # out.show()
    # 保存图片
    out.save("weather.jpg")

    # 绘制天气折线图
    # 获取数据 
    x = [datetime.strptime(d,'%d日%H时') for d in wea_hour]
    y = [int(tem[:-1]) for tem in wea_tem]
    # 图的标题
    plt.title("未来72h天气折线图")
    # x轴标签
    plt.xlabel("时间/s")
    # y轴标签
    plt.ylabel("温度/℃")
    plt.tick_params(labelsize=10)
    # 设置刻度定位器
    ax = plt.gca()
    # 指定x轴以日期格式(带小时)显示
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d日%H时'))
    # x轴的间隔为小时 
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
    # 设置x轴坐标竖直显示
    ax.xaxis.set_tick_params(rotation=90)
    # 图中显示竖坐标的值
    for xy in zip(x,y):
        plt.annotate(xy[1],xy=xy,xytext=(0,0),textcoords='offset points')
    # 坐标点之间用'-'连接
    plt.plot_date(x,y,color='dodgerblue',linewidth=2,linestyle='-',label='weather')
    # 生成默认图例
    plt.legend()
    # 自动旋转日期标志
    plt.gcf().autofmt_xdate()
    # 紧凑布局
    plt.tight_layout()
    # 保存图片
    plt.savefig('weather.png')
    return(my_rt)

if __name__ == '__main__':
    main()