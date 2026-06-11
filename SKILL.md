---
name: taiwan-education-expo-radar
description: Search, verify, deduplicate, and track upcoming Taiwan exhibitions and public-facing events relevant to learning for children aged 3–12, including preschool and elementary education, private education providers, experimental education, education technology, children's books, reading, STEAM, parent-child learning, educational toys, and learning content. Use when the user asks to find Taiwan events that reach children aged 3–12, their parents, teachers, schools, or education partners; update an exhibition tracker; check registration deadlines; monitor event changes; prepare Feishu/Lark spreadsheet updates; or generate exhibition reminders.
---

# Taiwan Education Expo Radar

Maintain a reliable Taiwan exhibition tracker for a children's education business. Prefer official sources, preserve uncertainty, and never invent dates or attendance figures.

The primary target audience is children aged 3–12, covering preschool through elementary school.

## Workflow

1. Read `references/sources-and-rules.md`.
2. Determine the monitoring window. Default to the previous 30 days through the next 18 months and cover all Taiwan counties and cities.
3. Open and inspect every source in the mandatory watchlist, even if search results do not surface it.
4. Search for additional events using the reference search queries.
5. Keep events relevant to at least one target segment:
   - Education technology, digital learning, AI education
   - Children's books, picture books, reading, publishing
   - Early childhood education, teaching materials, STEAM
   - Parent-child products or family experiences with educational value
   - Cultural IP, licensing, or content useful to children's education
   - Regional reading festivals, children's festivals, learning fairs, teacher events, and STEAM activities with exhibitor, sponsor, partnership, or booth opportunities
   - Private schools, international schools, cram schools, education franchises, education startups, foundations, NGOs, and private learning brands
   - Experimental education, alternative education, homeschooling, non-school-based experimental education, forest schools, and democratic education
   - Early childhood education, preschool, daycare, childcare, infant development, Montessori, Reggio Emilia, and parent education
   - Elementary learning, literacy, language, mathematics, science, coding, arts, social-emotional learning, physical development, and inquiry-based learning
6. Verify each material fact using an official organizer, venue, government, or association source.
7. Deduplicate events by organizer, event name, venue, and date.
8. Update the supplied spreadsheet. If none is supplied, copy `assets/展會追蹤表範本.xlsx` and update the copy.
9. Summarize new events, changed facts, deadlines, and uncertain items.

Maintain two opportunity types:

- `標準參展`: Public exhibitor application, booth package, or formal招商.
- `合作型參與`: Sponsorship, curated booth, workshop, content partnership, or organizer invitation.

Do not omit a high-fit 3–12 learning event merely because it lacks a standard booth application. Record it as a partnership candidate and identify the organizer contact path.

## Required Columns

Preserve these columns:

- 活動名稱
- 活動開始日期
- 活動結束日期
- 參展報名開始日
- 參展報名截止日
- 地點
- 面向
- 往年人潮
- 人潮年份
- 官方網站
- 資訊狀態
- 距報名截止日
- 提醒狀態
- 優先級
- 備註
- 最後更新日
- 前一屆開始日期
- 前一屆結束日期
- 前一屆日期來源
- 建議啟動規劃日
- 目標年齡
- 3–12歲適配度
- 學習領域

Use real date values in spreadsheets. Leave an unannounced value blank and set `資訊狀態` to `待公告` or `待確認`.

For every event, search for the immediately preceding edition and record its verified start date, end date, and source. Use the preceding edition only as a planning reference, not as the current edition's predicted date. Set `建議啟動規劃日` to approximately 180 days before the preceding edition's start date unless the user specifies a different lead time.

## Verification Rules

- Browse the web because exhibition information changes frequently.
- Do not rely only on search-engine results. Directly open every mandatory-watchlist domain on each run.
- On `edtech.tw`, inspect the homepage and EdTech latest-news pages for 招商, 參展, 報名, 展覽資訊, and 成果.
- Search both semantic variants such as `童書展` and `兒童書展`; never assume one wording covers the other.
- Check major private exhibition organizers because relevant consumer exhibitions may not appear on government or venue calendars promptly.
- Inspect official news releases, activity-topic pages, downloadable posters, and event images. Important dates may exist only inside an image.
- Keep relevant events that ended within the previous 30 days and label them `已結束`; use them to discover recurring future editions and organizers.
- Prefer official event pages over ticket platforms, media, blogs, and social posts.
- Record attendance only when a credible source explicitly reports it.
- If only a qualitative estimate exists, write it in `備註`; do not place it in `往年人潮`.
- Distinguish visitor dates from exhibitor registration dates.
- Do not carry a previous year's dates into a future edition.
- Keep previous-edition dates in dedicated columns and clearly separate them from current-edition dates.
- If the preceding edition cannot be verified, leave its dates blank and record `待查` in the source field.
- Add the year to event names when known.
- Treat renamed, postponed, relocated, and cancelled events as material changes.

## Priority Rules

Set `優先級`:

- `高`: Direct education, children's books, reading, early childhood, or strong teacher/school audience.
- `中`: Parent-child consumer, cultural IP, AI, innovation, or technology with a plausible education fit.
- `低`: Weak education relevance or limited commercial opportunity.

Exclude general markets, performances, and consumer events without meaningful education, reading, child-development, or partnership value.

Exclude events aimed only at infants under age 3, teenagers, university students, adult professional training, or general recruitment unless they contain a clearly relevant 3–12 segment.

Set `3–12歲適配度`:

- `高`: The event directly targets preschool or elementary children, their parents, or their teachers.
- `中`: The event has a meaningful children's learning section or strong channel-partner value.
- `低`: The connection is indirect; keep only when partnership value is credible.

## Regional Coverage

Every run must cover all Taiwan regions:

- 北部：基隆、臺北、新北、桃園、新竹、宜蘭
- 中部：苗栗、臺中、彰化、南投、雲林
- 南部：嘉義、臺南、高雄、屏東
- 東部與離島：花蓮、臺東、澎湖、金門、連江

Do not treat `展覽` as the only valid event label. Also detect `博覽會`, `教育節`, `閱讀節`, `書展`, `兒童節`, `親子嘉年華`, `科學節`, `STEAM`, `創客`, `論壇`, `教學成果展`, and `招商`.

For smaller regional activities, include them only when they offer a booth, exhibitor application, sponsorship, brand collaboration, educator outreach, or meaningful audience exposure.

## Private-Education Coverage

Do not require a government organizer or the word `展覽`. Include privately organized events such as:

- 招生博覽會、選校說明會、學校市集、教育品牌聯展
- 實驗教育論壇、成果展、嘉年華、共學聚會
- 幼教展、早教展、托育展、教保論壇、親職教育活動
- 補教加盟展、教育創業展、教育品牌合作會

Search organizer websites, Facebook/Instagram event announcements, ACCUPASS, KKTIX, Eventbrite, and venue calendars for discovery. Verify material facts against the organizer's official page or account before recording them.

## Reminder Rules

Set `提醒狀態` based on the exhibitor registration deadline:

- No deadline: `待確認截止日`
- Deadline passed: `報名已截止`
- 0–7 days remaining: `7日內截止`
- 8–30 days remaining: `30日內截止`
- More than 30 days: `持續追蹤`

In the final summary, surface:

1. Newly discovered high-priority events
2. Registration deadlines within 30 days
3. Date, venue, or deadline changes
4. Events still missing official dates or exhibitor information
5. High-fit recurring events expected in the requested months but not yet announced

## Feishu/Lark Handling

When a writable Feishu/Lark spreadsheet connector or URL is available, update it directly. Otherwise, update and return the Excel tracker for manual import.

Do not claim that the skill itself runs on a schedule. For unattended daily or weekly monitoring, create a separate automation that invokes this skill.

When the user's Feishu app credentials and spreadsheet URL are configured, generate `assets/feishu-expo-data.json` and run:

```bash
python3 scripts/feishu_sync.py --config <private-config-path> --data assets/feishu-expo-data.json
```

Never expose or commit the Feishu app secret. Preserve the user's manual columns: `是否參展`, `負責人`, `預算`, and `內部備註`.
