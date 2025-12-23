"""
- [ ]  定義格子大小：`CELL`
- [ ]  定義地圖尺寸：`GRID_W`, `GRID_H`
- [ ]  定義更新速度：`TICK_MS`
- [ ]  （可選）定義顏色常數：蟲身、蟲頭、葉子、背景
- [ ]  （可選）定義起始長度、起始方向
"""
CELL = 20 # 每格像素大小
GRID_W = 50 # 寬度格子數
GRID_H = 35 # 高度格子數
TICK_MS = 150 # 每幀更新時間（毫秒）
# 顏色常數
COLOR_BG = "#F0F8FF"
COLOR_HEAD = "#F0768B"
COLOR_BODY = "#ffc0cb"
COLOR_LEAF = "#228B22"

START_LENGTH = 5
START_DIRECTION = "Right"  # "Up", "Down", "Left", "Right
LEAVES_COUNT = 8
