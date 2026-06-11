# Taiwan Education Expo Radar

一個供 Codex 使用的 Skill，用來搜尋、驗證並追蹤全台與 **3–12 歲兒童學習**相關的展會與合作活動，並將資料同步到飛書／Lark 試算表。

## 追蹤範圍

- 教育科技、STEAM、科學與創客
- 童書、繪本、閱讀與語文
- 私立學校、國際學校、實驗教育
- 幼教、早教、特色教育與親子共學
- 教材、教具、教育新創與合作型活動
- 全台各縣市，不限政府或大型會展主辦

## 專案結構

```text
SKILL.md                         Codex Skill 核心流程
agents/openai.yaml               Skill 顯示資訊
references/sources-and-rules.md  搜尋來源與判斷規則
scripts/feishu_sync.py           飛書試算表同步工具
config/                          安全的設定範例
assets/                          追蹤表與同步資料範例
docs/                            飛書串接說明
```

## 安裝 Skill

將此儲存庫複製到 Codex Skills 目錄：

```bash
git clone <repository-url> ~/.codex/skills/taiwan-education-expo-radar
```

之後可以對 Codex 說：

```text
使用 $taiwan-education-expo-radar 搜尋全台近期適合參展的 3–12 歲兒童學習活動。
```

## 設定飛書同步

1. 複製設定範例：

```bash
cp config/feishu-sync-config.example.json config/feishu-sync-config.json
```

2. 在私人設定檔填入飛書試算表網址，並以環境變數提供憑證：

```bash
export FEISHU_APP_ID="your-app-id"
export FEISHU_APP_SECRET="your-app-secret"
```

3. 執行同步：

```bash
python3 scripts/feishu_sync.py \
  --config config/feishu-sync-config.json \
  --data assets/feishu-expo-data.example.json
```

同步會依活動名稱更新資料，並保留飛書中的 `是否參展`、`負責人`、`預算`、`內部備註`。

詳細設定請見 `docs/飛書串接設定說明.md`。

## 安全

- 不要提交 `App Secret`、私人試算表網址或 Webhook。
- 私人設定檔已由 `.gitignore` 排除。
- 首次同步前，請先以 `--dry-run` 驗證資料。
