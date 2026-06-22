# 日本経済指標 — API・指標調査メモ

調査日: 2026-06-06

---

## 1. 利用可能なAPI比較

| API | 登録 | 日本語データ | 更新頻度 | 特徴 |
|---|---|---|---|---|
| **FRED（セントルイス連銀）** | APIキー必要（無料） | OECD経由で豊富 | 月次 | シリーズIDが明確、JSON取得が簡単 |
| **e-Stat（政府統計ポータル）** | アプリIDが必要（無料） | 内閣府公式データ | 月次 | 景気動向指数の一次ソース、APIがやや複雑 |
| **World Bank API v2** | 不要 | 年次データ中心 | 年次 | app.pyで利用済みだが指標は年次のみ |

**推奨: FRED API** — 登録1回のみ、シリーズIDが明確、月次データが揃っている。

---

## 2. 推奨指標一覧

### 先行指標（景気より先に動く）

| 指標 | ソース / シリーズID | 説明 |
|---|---|---|
| 景気動向指数 先行CI | e-Stat `0003446461` | 内閣府公式の先行指数（最も代表的） |
| 機械受注 | FRED `JPNPRMNTO01IXOBSAM` | 設備投資の先行き（3〜6ヶ月先行） |
| 新規求人数 | e-Stat（厚労省） | 雇用の先行き |
| 東証株価指数(TOPIX) | Yahoo Finance 等 | 市場の期待値 |

### 実績指標（景気と同時に動く）

| 指標 | ソース / シリーズID | 説明 |
|---|---|---|
| 鉱工業生産指数 | FRED `JPNPROINDMISMEI` | 製造業活動の代表指標（OECD提供） |
| 完全失業率 | FRED `LRUN64TTJPM156S` | 雇用の実態（月次・15〜64歳） |
| CPI（消費者物価） | FRED `JPNCPIALLMINMEI` | インフレ動向（全品目） |
| 景気動向指数 一致CI | e-Stat `0003446461` | 内閣府公式の一致指数 |

---

## 3. 実装方針案

### 案A: FRED APIのみ（推奨）

**対象指標（3つ）:**
1. 鉱工業生産指数 `JPNPROINDMISMEI` — 景気の体温計（実績）
2. 完全失業率 `LRUN64TTJPM156S` — 雇用の健全度（実績）
3. CPI 全品目 `JPNCPIALLMINMEI` — インフレ動向（実績）

**メリット:**
- APIキー1つで完結
- エンドポイントが単純（`https://api.stlouisfed.org/fred/series/observations?series_id=XXX&api_key=KEY&file_type=json`）
- app.pyの既存パターン（`requests.get` + `@st.cache_data`）と同じ構造で追加できる

**デメリット:**
- 先行指標（景気動向指数）は含まれない

### 案B: FRED API + e-Stat API（先行指標も含める場合）

**追加指標:**
- 景気動向指数 先行CI / 一致CI（内閣府・e-Stat）

**デメリット:**
- APIキーが2種類必要（FRED + e-Stat）
- e-Stat のレスポンス構造がやや複雑

---

## 4. FRED APIエンドポイント仕様（参考）

```
GET https://api.stlouisfed.org/fred/series/observations
  ?series_id={SERIES_ID}
  &api_key={API_KEY}
  &file_type=json
  &observation_start=2000-01-01
  &observation_end=2026-12-31
```

レスポンス例（`observations` 配列）:
```json
{
  "observations": [
    { "date": "2000-01-01", "value": "98.5" },
    ...
  ]
}
```

値が欠損の場合は `"."` が入るため、`pd.to_numeric(errors='coerce')` で処理が必要。

---

## 5. e-Stat APIエンドポイント仕様（参考）

```
GET https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData
  ?appId={APP_ID}
  &statsDataId=0003446461   # 景気動向指数 長期系列
  &cdCat01=...              # 先行CI / 一致CI のカテゴリコード
```

- アプリID取得: https://www.e-stat.go.jp/api/
- 統計表ID `0003446461`: 景気動向指数（先行・一致・遅行 の長期系列）

---

## 6. 参考リンク

- [FRED — JPNPROINDMISMEI（鉱工業生産指数）](https://fred.stlouisfed.org/series/JPNPROINDMISMEI)
- [FRED — LRUN64TTJPM156S（完全失業率）](https://fred.stlouisfed.org/series/LRUN64TTJPM156S)
- [FRED — JPNCPIALLMINMEI（CPI）](https://fred.stlouisfed.org/series/JPNCPIALLMINMEI)
- [e-Stat — 景気動向指数](https://www.e-stat.go.jp/statistics/00100406)
- [内閣府経済社会総合研究所 — 景気動向指数](https://www.esri.cao.go.jp/jp/stat/di/di.html)
- [The Conference Board — LEI for Japan](https://www.conference-board.org/topics/business-cycle-indicators/japan/)
