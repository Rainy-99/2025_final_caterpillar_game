# 🐛 毛毛蟲大冒險（Caterpillar Game）

使用 **Python + Tkinter** 製作的單人毛毛蟲（貪食蛇）遊戲。  
玩家控制毛毛蟲在地圖中移動，吃到葉子會成長並累積分數，若撞牆或撞到自己則遊戲結束。

---

## 遊戲特色
- 開始畫面（Menu）與滑動轉場動畫
- 同時存在多顆葉子
- 暫停 / 遊戲結束畫面
- 音效播放（遊戲開始音效）
- 使用 model / view / app 分離架構，方便擴充

---

## ⌨ 操作方式
| 按鍵 | 功能 |
| --- | --- |
| ↑ ↓ ← → | 控制毛毛蟲移動 |
| Space / Enter | 從開始畫面進入遊戲 |
| R | 重置遊戲 |
| P | 暫停 / 繼續 |
| Esc | 離開遊戲 |

---

## 📁 專案結構
caterpillar_game/
├─ main.py # 程式入口，建立視窗
├─ game/
│ ├─ init.py
│ ├─ app.py # 控制中心（Canvas、鍵盤、主迴圈）
│ ├─ model.py # 遊戲狀態與規則
│ ├─ view.py # 畫面渲染（Canvas）
│ └─ config.py # 遊戲設定（尺寸、顏色、數量）
└─ README.md

---

## 遊戲核心設計

### GameState（model.py）
- `body: list[Point]`：毛毛蟲身體座標（頭在 index 0）
- `leaves: list[Point]`：多顆葉子座標
- `direction / pending`：移動方向與下一步方向（避免反向）
- `score`：分數
- `alive`：是否存活
- `w / h`：地圖大小（格子數）

### 遊戲邏輯流程
每一幀會執行：
1. 套用方向輸入（禁止 180 度反向）
2. 計算新頭部位置
3. 檢查撞牆或撞到自己
4. 插入新頭部
5. 吃到葉子則加分並生成新葉子
6. 未吃到葉子則移除尾巴

---

## 🖼 畫面渲染（view.py）
使用 Tkinter `Canvas` 繪製：
- 毛毛蟲（頭與身體不同顏色）
- 多顆葉子
- 左上角即時分數顯示  
畫面以「格子 × CELL 像素」轉換為實際座標。

---

## 遊戲流程控制（app.py）

### 模式狀態
- `menu`：開始畫面
- `transition`：Menu 滑出轉場動畫
- `playing`：遊戲進行中
- `paused`：暫停狀態
- `gameover`：遊戲結束畫面

### 主迴圈
使用 Tkinter `after()` 建立固定更新的主迴圈：
1. 更新遊戲狀態（`state.step()`）
2. 重新渲染畫面（`view.render()`）
3. 排程下一幀更新

---

## 開始畫面與轉場動畫
- Menu 物件皆使用 `tag="menu"` 管理
- 按下 Space / Enter 進入轉場模式
- 使用 `canvas.move("menu", dx, 0)` 讓所有物件滑出畫面
- 轉場完成後進入正式遊戲

---

## 音效
使用 `pygame.mixer` 播放音效：
- 遊戲開始時播放音效
- 音效邏輯集中於 `app.py`，不影響核心遊戲邏輯

---

## 執行方式

### 安裝套件
```bash
pip install pygame