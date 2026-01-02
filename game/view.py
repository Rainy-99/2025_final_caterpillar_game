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
            15, 10, anchor="nw", text=f"分數: {state.score}", fill="black", font=("Microsoft JhengHei", 24)
        )
        # 畫 Game Over
        # if not state.alive:
        #     w = state.w * CELL 
        #     h = state.h * CELL 
        #     self.canvas.create_text(
        #         w // 2, h // 2 - 30, text="遊戲結束", fill="red", font=("Microsoft JhengHei", 32, "bold")
        #     )
        #     self.canvas.create_text(
        #         w // 2, h // 2 + 80, text="按 R 重新開始", fill="grey", font=("Microsoft JhengHei", 24)
        #     )

    def _rect(self, gx: int, gy: int, fill: str) -> None:
        x1 = gx * CELL
        y1 = gy * CELL
        x2 = x1 + CELL
        y2 = y1 + CELL
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="")