# 運行遊戲主程式
import tkinter as tk
from game.app import App
def main():
    root = tk.Tk() # 建立主視窗
    root.title("Caterpillar Game") 
    app = App(root) # 建立應用程式
    root.mainloop() # 開始事件迴圈
if __name__ == "__main__":
    main()