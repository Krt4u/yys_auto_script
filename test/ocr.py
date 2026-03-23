from paddleocr import PaddleOCR

# 初始化OCR（离线使用时，指定本地模型路径，见下方注释）
ocr = PaddleOCR(use_angle_cls=False, lang='ch')  # lang='ch' 为中文

# 读取图片并识别
result = ocr.ocr('../src/data/awaking/1_awaking.png', cls=False)

# 解析结果
for line in result[0]:
    # line 的格式: [ [[x1,y1],[x2,y2],[x3,y3],[x4,y4]], ('文字', 置信度) ]
    bbox = line[0]          # 四个点坐标列表
    text = line[1][0]       # 识别的文字
    confidence = line[1][1] # 置信度
    print(f"文字: {text}\t位置: {bbox}\t置信度: {confidence}")