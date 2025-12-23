"""
## （時間、輸入、連接 model / view）

### 初始化 TODO

- [ ]  接收 `root`
- [ ]  建立 `Canvas(width=GRID_W*CELL, height=GRID_H*CELL)`
- [ ]  建立 `state = GameState.new(...)`
- [ ]  建立 `view = GameView(canvas)`
- [ ]  `root.bind("<Key>", on_key)`
- [ ]  呼叫 `tick()` 開始迴圈

### 事件 TODO

- [ ]  `on_key(event)`
    - [ ]  方向鍵 → `state.turn(event.keysym)`
    - [ ]  `R` → 重開一局
    - [ ]  （可選）`P` → 暫停

### 主迴圈 TODO

- [ ]  `tick()`
    - [ ]  `state.step()`
    - [ ]  `view.render(state)`
    - [ ]  `root.after(TICK_MS, tick)`

> App 只管「什麼時候做事」，不畫、不定規則。
"""
import tkinter as tk
from game.model import GameState
from game.view import GameView
from game.config import GRID_W, GRID_H, CELL, TICK_MS, COLOR_BG

class App:
    def __init__(self, root: tk.Tk): # 初始化
        self.root = root
        self.canvas = tk.Canvas( # 建立畫布
            root, # 父元件
            width=GRID_W * CELL, # 寬度
            height=GRID_H * CELL, # 高度
            bg=COLOR_BG
        )
        self.canvas.pack() # 顯示畫布

        self.state = GameState.new(GRID_W, GRID_H) # 建立遊戲狀態
        self.view = GameView(self.canvas) # 建立遊戲視圖

        self.root.bind("<Key>", self.on_key) # 綁定鍵盤事件
        self.tick() # 開始主迴圈

    def on_key(self, event): # 鍵盤事件
        if event.keysym in ["Up", "Down", "Left", "Right"]: # 方向鍵
            self.state.turn(event.keysym) # 轉向
        elif event.keysym in ("r", "R"): # 重開一局
            self.state = GameState.new(GRID_W, GRID_H) # 重置遊戲狀態
            self.view.render(self.state) # 重畫畫面

    def tick(self): # 主迴圈
        self.state.step() # 更新遊戲狀態
        self.view.render(self.state) # 重畫畫面
        self.root.after(TICK_MS, self.tick) # 設定下一次呼叫