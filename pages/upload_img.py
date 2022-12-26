from pywebio.input import *
from pywebio.output import *
import time
import os

imgs_path = "./imgs/"
select_ls = [
    {"label": "画作", "value": "画作", "selected":False, "disabled":False},
    {"label": "插画", "value": "插画", "selected":False, "disabled":False},
    {"label": "立绘", "value": "立绘", "selected":False, "disabled":False},
    {"label": "截图", "value": "截图", "selected":False, "disabled":False},
    {"label": "AI", "value": "AI", "selected":False, "disabled":False},
    {"label": "表情包", "value": "表情包", "selected":False, "disabled":False},
    {"label": "其他", "value": "其他", "selected":False, "disabled":False}
]

def handle_data(data) -> bool:
    # 创建子目录
    column = data['column'] + ": "
    current_time = time.strftime('%Y-%m-%d %T',time.localtime(time.time()))    
    exact_path = imgs_path + column + current_time
    if os.path.exists(exact_path):
        # 如果子目录存在则等一秒后再创建
        time.sleep(1000)
        current_time = time.strftime('%Y-%m-%d %T',time.localtime(time.time()))
        exact_path = imgs_path + column + current_time
    os.mkdir(exact_path)
    # 保存文本数据(栏目，作者，邮箱)
    info = f"时间：{current_time}\n栏目：{data['column']}作者：{data['author']}\n联系邮箱：{data['email']}"
    with open(exact_path+'/'+"info.json", "w", encoding="utf-8") as fp:
        fp.write(info)
    # 遍历数据，保存图片
    for img_data in data['img']:
        img_name = exact_path + "/" + img_data['filename'] + img_data["mime_type"].split("/")[-1]
        with open(img_name, 'wb') as fp:
            fp.write(img_data['content'])
    return True, info

def upload_img():
    """上传图片
    
    ...
    """
    # 构建输入组
    data = input_group("图片信息",[
    select('栏目', name='column', options=select_ls),
    input('作者', name='author', placeholder="选填", required=False),
    input('联系邮箱', name='email', placeholder="选填", required=False),
    file_upload('点击上传', name='img', placeholder="可上传多张图片", accept="image/*", multiple=True)
    ])
    try:
        info = handle_data(data)
        put_success(f"上传成功！\n{info}")
    except Exception as e:
        put_error(f"上传失败！请重试或联系管理员解决(qq:756796457)\n错误信息：{repr(e)}")