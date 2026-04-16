# 遊戲邀請互動流程與系統架構評估

## 一、互動流程總覽

```
使用者A (發起者)                     系統                          使用者B (受邀者)
    |                                |                                |
    |  1. 選擇好友並發送邀請          |                                |
    |  ──────────────────────────>   |                                |
    |                                |  2. 建立邀請記錄 + 遊戲房間      |
    |                                |  ──────────────────────────>    |
    |                                |  3. 發送推播通知 (FCM/APNs)      |
    |                                |  ──────────────────────────>    |
    |                                |                                |
    |                                |                    4. 收到推播通知
    |                                |                    5. 點擊推播通知
    |                                |   <──────────────────────────  |
    |                                |  6. Deep Link 解析，導向遊戲頁面 |
    |                                |  ──────────────────────────>    |
    |                                |                                |
    |                                |  7. 受邀者接受邀請               |
    |                                |   <──────────────────────────  |
    |  8. 即時通知：朋友已加入        |                                |
    |   <──────────────────────────  |                                |
    |                                |                                |
    |  9. 雙方進入同一遊戲房間開始遊玩  |                               |
    |  <─────────────────────────────────────────────────────────>    |
```

## 二、詳細使用者流程

### 2.1 發起邀請方 (使用者A)

1. 開啟 App，進入好友列表或遊戲大廳
2. 選擇想要一起玩的遊戲
3. 從好友列表中選擇一位或多位好友
4. 點擊「發送邀請」按鈕
5. 等待好友回應（畫面顯示等待狀態）
6. 收到好友接受通知後，雙方同時進入遊戲房間

### 2.2 受邀方 (使用者B)

1. 收到手機推播通知：「使用者A 邀請你一起玩 OO 遊戲！」
2. 點擊推播通知
3. App 透過 Deep Link 開啟並導向對應的邀請頁面
4. 顯示邀請詳情（誰邀請的、什麼遊戲、邀請時間）
5. 選擇「接受」或「拒絕」
6. 接受後自動加入遊戲房間，開始遊玩

## 三、系統架構所需機制

### 3.1 使用者與好友系統

| 機制 | 說明 |
|------|------|
| 使用者認證 | 註冊/登入機制（JWT Token 或 OAuth 2.0） |
| 使用者資料管理 | 暱稱、頭像、線上狀態 |
| 好友關係管理 | 新增好友、刪除好友、好友列表查詢 |
| 線上狀態追蹤 | 透過 WebSocket 心跳或 Presence 機制追蹤使用者是否在線 |

### 3.2 邀請管理服務

| 機制 | 說明 |
|------|------|
| 邀請建立 | 記錄發起者、受邀者、指定遊戲、邀請時間 |
| 邀請狀態管理 | 狀態流轉：`pending` → `accepted` / `declined` / `expired` |
| 邀請過期機制 | 設定 TTL（例如 5 分鐘），超時自動過期 |
| 重複邀請防護 | 避免對同一人重複發送尚未回應的邀請 |

### 3.3 推播通知服務

| 機制 | 說明 |
|------|------|
| FCM (Android) | 透過 Firebase Cloud Messaging 發送推播 |
| APNs (iOS) | 透過 Apple Push Notification Service 發送推播 |
| 裝置 Token 管理 | 使用者登入時註冊裝置 Token，登出時移除 |
| 通知內容組裝 | 包含邀請者名稱、遊戲名稱、Deep Link URL |
| 推播失敗重試 | 發送失敗時的重試與降級策略 |

### 3.4 Deep Link 機制

| 機制 | 說明 |
|------|------|
| URI Scheme | 自訂 scheme，例如 `myapp://invite/{invite_id}` |
| Universal Links (iOS) | 支援 HTTPS 連結直接開啟 App |
| App Links (Android) | 支援 HTTPS 連結直接開啟 App |
| 未安裝 App 導向 | 偵測未安裝時導向 App Store / Google Play |
| 路由解析 | App 端解析 Deep Link 參數並導航至對應頁面 |

### 3.5 遊戲房間管理

| 機制 | 說明 |
|------|------|
| 房間建立 | 發送邀請時自動建立遊戲房間 |
| 房間狀態管理 | `waiting` → `playing` → `finished` |
| 玩家加入/離開 | 管理房間內的玩家列表 |
| 房間銷毀 | 邀請過期或遊戲結束後自動清理 |
| 最大人數限制 | 根據遊戲類型限制房間人數上限 |

### 3.6 即時通訊 (WebSocket)

| 機制 | 說明 |
|------|------|
| 連線管理 | WebSocket 連線建立、心跳維持、斷線重連 |
| 邀請狀態即時同步 | 受邀方回應後即時通知發起方 |
| 遊戲狀態同步 | 遊戲進行中的即時資料交換 |
| 訊息佇列 | 使用 Redis Pub/Sub 或 Message Queue 進行訊息分發 |

## 四、資料模型設計

### 4.1 邀請記錄 (Invitation)

```
Invitation
├── id              (UUID, 主鍵)
├── sender_id       (UUID, 發起者)
├── receiver_id     (UUID, 受邀者)
├── game_id         (UUID, 指定遊戲)
├── room_id         (UUID, 遊戲房間)
├── status          (Enum: pending / accepted / declined / expired)
├── created_at      (Timestamp, 建立時間)
├── expired_at      (Timestamp, 過期時間)
└── responded_at    (Timestamp, 回應時間，可為空)
```

### 4.2 遊戲房間 (GameRoom)

```
GameRoom
├── id              (UUID, 主鍵)
├── game_id         (UUID, 遊戲類型)
├── host_id         (UUID, 房主)
├── status          (Enum: waiting / playing / finished)
├── max_players     (Integer, 最大人數)
├── created_at      (Timestamp)
└── players         (List<UUID>, 目前房間內玩家)
```

### 4.3 裝置推播 Token (DeviceToken)

```
DeviceToken
├── id              (UUID, 主鍵)
├── user_id         (UUID, 使用者)
├── token           (String, 裝置推播 Token)
├── platform        (Enum: ios / android)
└── updated_at      (Timestamp)
```

## 五、API 端點設計

### 5.1 邀請相關

| 方法 | 端點 | 說明 |
|------|------|------|
| POST | `/api/invitations` | 發送遊戲邀請 |
| GET | `/api/invitations/{id}` | 查詢邀請詳情 |
| PATCH | `/api/invitations/{id}/accept` | 接受邀請 |
| PATCH | `/api/invitations/{id}/decline` | 拒絕邀請 |
| GET | `/api/invitations/pending` | 查詢待回應的邀請列表 |

### 5.2 遊戲房間相關

| 方法 | 端點 | 說明 |
|------|------|------|
| POST | `/api/rooms` | 建立遊戲房間 |
| GET | `/api/rooms/{id}` | 查詢房間資訊 |
| POST | `/api/rooms/{id}/join` | 加入房間 |
| POST | `/api/rooms/{id}/leave` | 離開房間 |

### 5.3 WebSocket 端點

| 端點 | 說明 |
|------|------|
| `ws://host/ws/invitations/` | 邀請狀態即時更新頻道 |
| `ws://host/ws/rooms/{room_id}/` | 遊戲房間即時通訊頻道 |

## 六、技術選型建議

| 層級 | 建議技術 |
|------|---------|
| 後端框架 | Django + Django REST Framework 或 FastAPI |
| 即時通訊 | Django Channels (WebSocket) 或 Socket.IO |
| 推播服務 | Firebase Cloud Messaging (FCM) 統一處理雙平台 |
| 訊息佇列 | Redis Pub/Sub 或 RabbitMQ |
| 排程任務 | Celery（處理邀請過期、推播重試） |
| 資料庫 | PostgreSQL（主資料）+ Redis（快取與即時狀態） |
| Deep Link | Firebase Dynamic Links 或自建 Universal Links / App Links |

## 七、需額外考量的邊界情況

1. **使用者離線**：推播送達後使用者未開啟，邀請應在過期前保持有效
2. **App 未安裝**：Deep Link 需處理未安裝情境，導向商店下載
3. **多裝置登入**：同一使用者多台裝置需同步推播與邀請狀態
4. **併發處理**：多人同時對同一使用者發送邀請時的處理邏輯
5. **網路中斷**：WebSocket 斷線重連後的狀態同步機制
6. **邀請取消**：發起方在對方回應前主動取消邀請的處理
7. **遊戲中途離開**：玩家中途退出遊戲的善後處理
8. **推播權限**：使用者未授權推播通知時的替代方案（App 內通知）
