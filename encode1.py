from PIL import Image
#文本转二进制
def txt_to_bina(txt):
    c=[]
    for a in txt:
        c.append("{:0>8}".format(bin(ord(a)).lstrip('0b')))
    resultlist = []
    for i in c:
        for j in range(8):
            resultlist.append(i[j])
    return resultlist
#打开图片文件并创建输出图片框架
img = Image.open("encode_image.png")
img_out = Image.new(img.mode,img.size)
#定义文本
txt = 'hello world!'
#像素载入
pix = img.load()
width = img.size[0]
height = img.size[1]
r_list,g_list,b_list = [],[],[]
#获取像素点的RGB值
for y in range(height):
    for x in range(width):
        r,g,b =pix[x,y] #此处的r,g,b是像素点pix[x,y]的RGB值
        r_list.append(r)#建立序列分别收集所有像素点的RGB值：或许可以只用一个序列？？？？//分列三个序列最终合并的时候循环次数更低
        g_list.append(g)
        b_list.append(b)
#替换信息位的信息
i = 0
r_flag = 0
g_flag = 1
b_flag = 2
temp = ''
while r_flag < len(txt_to_bina(txt)):
    temp = bin(r_list[i])
    r_list[i] = int(temp[-1].replace(temp[-1],txt_to_bina(txt)[r_flag]),2)
    i += 1
    r_flag += 3
while r_flag < len(txt_to_bina(txt)):
    temp = bin(g_list[i])
    g_list[i] = int(temp[-1].replace(temp[-1],txt_to_bina(txt)[g_flag]),2)
    i += 1
    g_flag += 3
while b_flag < len(txt_to_bina(txt)):
    temp = bin(b_list[i])
    b_list[i] = int(temp[-1].replace(temp[-1],txt_to_bina(txt)[b_flag]),2)
    i += 1
    b_flag += 3
# 输出图像
j = 0
pixels = []
while j<(width*height):    
    pixels.append((r_list[j],g_list[j],b_list[j]))
    j += 1
img_out.putdata(pixels)
img_out.save("img_out1.png")

