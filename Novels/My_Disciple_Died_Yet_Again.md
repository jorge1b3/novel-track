---
tags:
  - novel
  - Action
  - Adventure
  - Comedy
  - Drama
  - Fantasy
  - Josei
  - Romance
  - Xianxia
fileClass: novel
aliases:
  - My Disciple Died Yet Again
status: Completed
author: Mrs. Ago
source-url: https://www.novelupdates.com/series/my-disciple-died-yet-again/
total-chapters: 393
current-chapter: 393
side-stories-total: 0
side-stories-read: 0
rating: 5
description: Game designer Zhu Yao accidentally gets transmigrated into a new xianxia VR game that is currently in development. There she becomes the disciple of the most beautiful male immortal Yu Yan who had to wait 16 thousand years before finally getting a disciple of his own. Yu Yan carefully teaches Zhu Yao and cherishes her a lot. But when Zhu Yao finally begins to understand some of his teachings, she suddenly dies. Yu Yan then gets a new disciple, the reborn Zhu Yao, and she dies again. He then gets another disciple, and she dies once again…
genre: []
cssclasses:
  - novel-page
---

# My Disciple Died Yet Again

![[covers/My_Disciple_Died_Yet_Again.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/my-disciple-died-yet-again/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c393 (end)`, latest `c31`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
