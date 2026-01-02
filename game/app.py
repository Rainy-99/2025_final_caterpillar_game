import tkinter as tk
import pygame
import pygame.mixer
import os
from game.model import GameState
from game.view import GameView
from game.config import GRID_W, GRID_H, CELL, TICK_MS, COLOR_BG

class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.canvas = tk.Canvas(
            root,
            width=GRID_W * CELL,
            height=GRID_H * CELL,
            bg=COLOR_BG
        )
        self.canvas.pack()

        self.view = GameView(self.canvas)
        self.state: GameState | None = None
        # --- 初始化音效 ---
        pygame.mixer.init()
        base_dir = os.path.dirname(os.path.dirname(__file__))  # 專案根目錄
        assets_dir = os.path.join(base_dir, "sound")

        self.snd_start = pygame.mixer.Sound(os.path.join(assets_dir, "game-start-6104.wav"))

        # 模式狀態
        self.mode = "menu"

        # menu 轉場
        self._menu_offset = 0
        self._menu_dx = 20
        self._menu_dir = 1

        self.root.bind("<Key>", self.on_key)
        self.show_menu()

    # ---------- Menu ----------
    def show_menu(self):
        self.mode = "menu"
        self.canvas.delete("all")
        self._menu_offset = 0

        w = GRID_W * CELL
        h = GRID_H * CELL

        # 固定葉子大小（畫面 1/4）
        leaf_w = w * 0.5
        leaf_h = h * 0.35

        # ===== 左下角葉子 =====
        lx = w * 0.3
        ly = h * 0.8

        self.canvas.create_oval(
            lx - leaf_w / 2, ly - leaf_h / 2,
            lx + leaf_w / 2, ly + leaf_h / 2,
            fill="#228B22",
            outline="",
            tags=("menu",)
        )
        self.canvas.create_line(
            lx - leaf_w * 0.3, ly,
            lx + leaf_w * 0.3, ly,
            fill="#145214",
            width=3,
            tags=("menu",)
        )

        # ===== 右上角葉子 =====
        rx = w * 0.8
        ry = h * 0.2

        self.canvas.create_oval(
            rx - leaf_w / 2, ry - leaf_h / 2,
            rx + leaf_w / 2, ry + leaf_h / 2,
            fill="#228B22",
            outline="",
            tags=("menu",)
        )
        self.canvas.create_line(
            rx - leaf_w * 0.3, ry,
            rx + leaf_w * 0.3, ry,
            fill="#145214",
            width=3,
            tags=("menu",)
        )

        # ===== 固定毛毛蟲（整體裝飾）=====
        worm_x = lx - leaf_w * 0.25
        worm_y = ly - leaf_h * 0.15

        segments = 6
        gap = 32

        for i in range(segments):
            r = 28 if i == 0 else 22
            color = "#F0768B" if i == 0 else "#ffc0cb"
            cx = worm_x - i * gap
            cy = worm_y

            self.canvas.create_oval(
                cx - r, cy - r,
                cx + r, cy + r,
                fill=color,
                outline="",
                tags=("menu",)
            )

        # 眼睛
        self.canvas.create_oval(
            worm_x - 6, worm_y - 6,
            worm_x - 2, worm_y - 2,
            fill="black", outline="",
            tags=("menu",)
        )
        self.canvas.create_oval(
            worm_x + 2, worm_y - 6,
            worm_x + 6, worm_y - 2,
            fill="black", outline="",
            tags=("menu",)
        )

        # ===== Menu 文字 =====
        self.canvas.create_text(
            w // 2, h // 2 - 60,
            text="毛毛蟲大冒險",
            font=("Microsoft JhengHei", 32, "bold"),
            fill="black",
            tags=("menu",)
        )
        self.canvas.create_text(
            w // 2, h // 2 - 10,
            text="按 SPACE / ENTER 開始遊戲",
            font=("Microsoft JhengHei", 16),
            fill="black",
            tags=("menu",)
        )
        self.canvas.create_text(
            w // 2, h // 2 + 20,
            text="方向鍵移動 / P 暫停遊戲 / R 重置遊戲",
            font=("Microsoft JhengHei", 12),
            fill="black",
            tags=("menu",)
        )
        self.canvas.create_text(
            w // 2, h // 2 + 80,
            text="按 ESC 離開遊戲",
            font=("Microsoft JhengHei", 12),
            fill="gray",
            tags=("menu",)
        )

    # ---------- Transition ----------
    def start_transition(self):
        if self.mode != "menu":
            return
        self.mode = "transition"
        self._menu_offset = 0
        self._menu_dir = 1
        self._animate_menu_exit()

    def _animate_menu_exit(self):
        if self.mode != "transition":
            return

        w = GRID_W * CELL
        dx = self._menu_dx * self._menu_dir

        self.canvas.move("menu", dx, 0)
        self._menu_offset += abs(dx)

        if self._menu_offset >= w + 120:
            self.canvas.delete("menu")
            self.start_game()
            return

        self.root.after(16, self._animate_menu_exit)

    # ---------- Start Game ----------
    def start_game(self):
        self.mode = "playing"
        self.state = GameState.new(GRID_W, GRID_H)

        self.tick()

    # ---------- Input ----------
    def on_key(self, event):
        key = event.keysym

        if self.mode == "menu":
            if key in ("space", "Return", "Enter"):
                # 播放遊戲開始音效
                try:
                    self.snd_start.play()
                except Exception:
                    pass  # 靜音也不讓遊戲掛掉

                self.start_transition()
            elif key in ("Escape", "q", "Q"):
                self.root.destroy()
            return

        if self.mode == "transition":
            return

        if key in ("Up", "Down", "Left", "Right"):
            self.state.turn(key)

        if self.mode == "gameover" and key in ("space", "Enter"):
            self.canvas.delete("gameover")
            self.show_menu()
            return

        if self.mode == "playing" and key in ("p", "P"):
            self.mode = "paused"
            self._show_pause_overlay()
            return

        if self.mode == "paused" and key in ("p", "P"):
            self._hide_pause_overlay()
            self.mode = "playing"
            self.tick()
            return


        elif key in ("r", "R"):
            self.state = GameState.new(GRID_W, GRID_H)

    # ---------- Game loop ----------
    def tick(self):
        if self.mode != "playing":
            return

        self.state.step()
        self.view.render(self.state)

        if not self.state.alive:
            self.mode = "gameover"
            self._show_game_over()
            return

        self.root.after(TICK_MS, self.tick)

    # ---------- Pause Overlay ----------
    def _show_pause_overlay(self):
        w = GRID_W * CELL
        h = GRID_H * CELL

        self.canvas.create_rectangle(
            0, 0, w, h,
            fill="black",
            stipple="gray50",
            tags=("pause",)
        )
        self.canvas.create_text(
            w // 2, h // 2,
            text="PAUSED\n按 P 繼續",
            font=("Arial", 28, "bold"),
            fill="white",
            tags=("pause",)
        )
    def _hide_pause_overlay(self):
        self.canvas.delete("pause")

    # ---------- Game Over Overlay ----------
    def _show_game_over(self):
        w = GRID_W * CELL
        h = GRID_H * CELL

        self.canvas.create_rectangle(
            0, 0, w, h,
            fill="black",
            stipple="gray50",
            tags=("gameover",)
        )
        self.canvas.create_text(
            w // 2, h // 2,
            text="GAME OVER\n按空白鍵返回主畫面",
            font=("Arial", 28, "bold"),
            fill="white",
            tags=("gameover",)
        )
