"""
## 負責畫

### 初始化 TODO

- [ ]  建立 `GameView(canvas)`
- [ ]  保存 canvas 引用

### 渲染 TODO

- [ ]  `render(state)`：每幀重畫
    - [ ]  `canvas.delete("all")`
    - [ ]  畫葉子（綠色方塊）
    - [ ]  畫毛毛蟲（頭一色、身體一色）
    - [ ]  畫分數文字
    - [ ]  若 `not alive` → 畫 Game Over 文字

### 工具 TODO

- [ ]  `_rect(gx, gy, fill=...)`：格子座標 → 像素 → 畫矩形

"""
from game.model import GameState
from game.config import CELL, COLOR_HEAD, COLOR_BODY, COLOR_LEAF
class GameView:
    def __init__(self, canvas) -> None:
        self.canvas = canvas

    def render(self, state: GameState) -> None:
        self.canvas.delete("all")
        # 畫葉子
        for leaf_x, leaf_y in state.leaves:
            self._rect(leaf_x, leaf_y, fill=COLOR_LEAF)
        # 畫毛毛蟲
        for i, (bx, by) in enumerate(state.body):
            color = COLOR_HEAD if i == 0 else COLOR_BODY
            self._rect(bx, by, fill=color)
        # 畫分數
        self.canvas.create_text(
            10, 10, anchor="nw", text=f"Score: {state.score}", fill="black", font=("Arial", 16)
        )
        # 畫 Game Over
        if not state.alive:
            w = state.w * CELL
            h = state.h * CELL
            self.canvas.create_text(
                w // 2, h // 2, text="GAME OVER", fill="red", font=("Arial", 32)
            )
            self.canvas.create_text(
                w // 2, h // 2 + 60, text="Press R to restart", fill="black", font=("Arial", 24)
            )

    def _rect(self, gx: int, gy: int, fill: str) -> None:
        x1 = gx * CELL
        y1 = gy * CELL
        x2 = x1 + CELL
        y2 = y1 + CELL
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="")