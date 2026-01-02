# 遊戲邏輯
from __future__ import annotations # 允許類別內部引用自身類型

import random
from dataclasses import dataclass
from game.config import START_LENGTH, LEAVES_COUNT, START_DIRECTION

Point = tuple[int, int]

DIRS = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0),
}

OPPOSITE = {
    "Up": "Down",
    "Down": "Up",
    "Left": "Right",
    "Right": "Left",
}

@dataclass
class GameState:
    body: list[Point]
    direction: str
    pending: str | None
    leaves: list[Point]   # 多顆葉子
    score: int
    alive: bool
    w: int
    h: int

    @staticmethod
    def new(w: int, h: int) -> GameState:
        mid_x = w // 2
        mid_y = h // 2
        body = [(mid_x - i, mid_y) for i in range(START_LENGTH)]
        leaves = GameState._spawn_leaves(body, w, h, LEAVES_COUNT)
        return GameState(body, START_DIRECTION, None, leaves, 0, True, w, h)

    def turn(self, key: str) -> None:
        # 只接受四個方向鍵，禁止 180 度反向
        if key in OPPOSITE and OPPOSITE.get(self.direction) != key:
            self.pending = key

    def step(self) -> None:
        if not self.alive:
            return

        # 套用 pending
        if self.pending:
            if OPPOSITE.get(self.direction) != self.pending:
                self.direction = self.pending
            self.pending = None

        head_x, head_y = self.body[0]
        dx, dy = DIRS[self.direction]
        new_head = (head_x + dx, head_y + dy)

        # 撞牆
        x, y = new_head
        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            self.alive = False
            return

        # 撞自己
        if new_head in self.body:
            self.alive = False
            return

        # 把新頭塞進去
        self.body.insert(0, new_head)

        # 檢查是否吃到葉子
        ate_index = -1
        for i, p in enumerate(self.leaves):
            if p == new_head:
                ate_index = i
                break

        if ate_index != -1:
            # 吃到：加分、長大
            self.score += 1

            # 移除被吃掉的那顆葉子
            self.leaves.pop(ate_index)

            # 補一顆新的葉子（避免跟 body / 其他葉子重疊）
            new_leaf = GameState._spawn_one_leaf(self.body, self.leaves, self.w, self.h)
            self.leaves.append(new_leaf)
        else:
            # 沒吃到：正常移動（尾巴 pop）
            self.body.pop()

    @staticmethod
    def _spawn_one_leaf(body: list[Point], leaves: list[Point], w: int, h: int) -> Point:
        # 不能生成在 body 或其他 leaves 上
        occupied = set(body) | set(leaves)
        empty_positions = [(x, y) for x in range(w) for y in range(h) if (x, y) not in occupied]

        if not empty_positions:
            # 沒地方放葉子了（理論上代表你佔滿地圖）
            return (-1, -1)

        return random.choice(empty_positions)

    @staticmethod
    def _spawn_leaves(body: list[Point], w: int, h: int, count: int) -> list[Point]:
        leaves: list[Point] = []
        for _ in range(count):
            p = GameState._spawn_one_leaf(body, leaves, w, h)
            leaves.append(p)
        return leaves
