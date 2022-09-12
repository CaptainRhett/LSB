# LSB-隐写术

<p>北京理工大学网络空间安全专业小学期python项目实践</p>
<h1>一、项目背景</h1>
<h2>1、隐写术</h2>
<p>隐写术是一门关于信息隐藏的技巧与科学，所谓信息隐藏指的是不让除预期的接收者之外的任何人知晓信息的传递事件或者信息的内容。</p>
<h2 id="2lsb-隐写术" class="heading h3">2.LSB 隐写术</h2>
<p class="paragraph" data-pm-slice="1 1 []">LSB 隐写术是一种图像隐写术技术，其中通过将每个像素的<strong class="strong">最低有效位</strong>替换为要隐藏的消息位来将消息隐藏在图像中。</p>
<h2 class="paragraph" data-pm-slice="1 1 []">3.实现原理</h2>
<p class="paragraph" data-pm-slice="1 1 []">为了更好地理解，让我们将数字图像视为像素的二维阵列，每个像素包含取决于其类型和深度的值，使用最广泛的颜色模式RGB，这些值的范围为0&ndash;255之间。</p>
<p class="paragraph" data-pm-slice="1 1 []"><img src="https://img2022.cnblogs.com/blog/2966064/202209/2966064-20220909082237848-432441629.png" alt="" /></p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p class="paragraph" data-pm-slice="1 1 []">可以使用 ASCII Table&nbsp;将消息转换为十进制值，然后再转换为二进制。然后，我们逐个迭代像素值，将它们转换为二进制后，我们将每个最低有效位替换为序列中的消息位。</p>
<p class="paragraph">要解码编码图像，我们只需反转该过程，收集并存储每个像素的最后一位，然后将它们分成 8 组，并将其转换回 ASCII 字符以获取隐藏消息。</p>
<h1 class="paragraph">二、项目目标</h1>
<h2 class="paragraph">1.主要目标</h2>
<p class="paragraph" data-pm-slice="1 3 []">编写<strong class="strong">LSB图像隐写程序</strong>，包括：<strong class="strong">加密程序</strong>和<strong class="strong">解密程序</strong>。</p>
<h2 id="2目标分解" class="heading h3">2.目标分解</h2>
<p class="heading h3">a）实现文本信息加密到图像</p>
<p class="heading h3">b）实现图像文件解密到文本</p>
<h1 class="heading h3">三、技术选型</h1>
<h2 class="heading h3">1.问题：如何以二进制方式读写图像文件？</h2>
<p class="heading h3">首先安装pillow库，win+R输入cmd快速打开控制台，直接输入以下代码即可自动安装</p>
<pre class="language-python highlighter-hljs"><code>pip install pillow</code></pre>
<p class="paragraph" data-pm-slice="1 1 []">然后读取图片<br /><br /></p>
<pre class="language-python highlighter-hljs"><code>from PIL import Image #从pillow库（即PIL）中导入Image类
img = Image.open('../xx.jpg') #读取图片存入变量img中
print(img.format) #输出图片格式(str)
print(img.size) #输出图片大小信息 （宽度w，高度h）tuple = (int,int)</code></pre>
<p>获取像素信息</p>
<pre class="language-python highlighter-hljs"><code>#像素载入
pix = img.load()
width = img.size[0] #.size 方法返回的是一个元组 tuple =(int,int) 
height = img.size[1] 
#获取像素点的RGB值
rgb_list = [] #创建一个数组存储RGB值
for y in range(height):#遍历每一个像素点，将图像看作是一个二维数组，
    for x in range(width): #如果x循环在外层输出的图像会发生一个九十度的翻转
        r,g,b =pix[x,y] #此处的r,g,b是像素点pix[x,y]的RGB值
        rgb_list.append(r)
        rgb_list.append(g)
        rgb_list.append(b)</code></pre>
<p>输出图像</p>
<pre class="language-python highlighter-hljs"><code>#输出图像
j = 0
pixels = [] #以[(r1,g1,b1),(r2,g2,b2)]形式存放每个像素点的RGB值，于绘制图像
img_out = Image.new(img.mode,img.size) #生成新图像，以原图的格式和大小
#img_out此时还是一张白纸，下面的代码旨在更新img_out的像素信息
while j&lt;len(rgb_list):    #循环次数高达786432次
    pixels.append((rgb_list[j],rgb_list[j+1],rgb_list[j+2])) #以元组的形式
    j += 3
img_out.putdata(pixels)#放置像素信息
img_out.save("img_out2.png")#将图像保存为，程序运行后会出现在根目录</code></pre>
<h2>2.问题：信息如何转换</h2>
<p>二进制转文本（解密）</p>
<pre class="language-python highlighter-hljs"><code>def bina_to_txt(bina):
    #只要传入一个二进制数组成的序列即可翻译成文本
    tex = []
    for i in bina:
        tex.append(chr(int(i,2)))
    return tex #返回一个单字符序列

#要求bina的格式为['01010101','11111111']</code></pre>
<p>文本转二进制（加密）</p>
<pre class="language-python highlighter-hljs"><code>def txt_to_bina(txt):
    c=[]
    for a in txt:
        c.append("{:0&gt;8}".format(bin(ord(a)).lstrip('0b')))
        #格式化将二进制码保存起来
        #注意要在右侧补齐八位，否则信息会错位
    resultlist = []
    for i in c:
        for j in range(8):
            resultlist.append(i[j])
    return resultlist
#txt 为字符串类型，如 &ldquo;hello world！&rdquo;

#print(txt_to_bina("h"))  输出测试
#test_output:['0', '1', '1', '0', '1', '0', '0', '0']</code></pre>
<p>替换信息位（加密）</p>
<pre class="language-python highlighter-hljs"><code>#替换信息位的信息
i = 0
while i &lt; len(txt_to_bina(txt)):
    temp =list(bin(rgb_list[i])) #用 bin()强制转换，bin()返回一个字符串类型
    temp[-1]=txt_to_bina(txt)[i] #将二进制型的RGB信息的最后一位转换成文本二进制码
    rgb_list[i] = int(''.join(temp),2)
    i += 1
#txt_to_bina()是自定义的一个函数，旨在将文本转化成二进制码，返回一个单字符的序列
#这里是直接用第一个像素的RGB值作为隐写的开头，所以rgb_list和txt_to_bina()[]的index是一样的
#此处可以做一个加密

#特别注意在python中字符串不能直接修改，replace方法不会改变原来的string
#修改字符串要将字符串转换成一个序列，修改序列后在将序列转成字符串，实现代码如下
s = 'abcde'
temp = list(s)
temp[-1] = 'f' #假设要将s的最后一位&ldquo;e&rdquo;修改为&ldquo;f&rdquo;
s = ''.join(temp)</code></pre>
<p>提取信息位信息</p>
<pre class="language-python highlighter-hljs"><code>#这里直接用的是&ldquo;hello world！&rdquo;的长度，后期优化可以加个旗帜识别
c = ''
for i in range(96):
    c += bin(rgb_list[i])[-1] #图像处理后得到rgb_list,取二进制码的最后一位
out_list_bin =[]
for i in range(12):
    out_list_bin.append(c[i*8:(i+1)*8])#每八位为一组转换出文本
print(''.join(bina_to_txt(out_list_bin)))</code></pre>
<p>&nbsp;</p>
