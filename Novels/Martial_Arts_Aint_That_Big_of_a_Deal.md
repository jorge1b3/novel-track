---
tags:
  - novel
  - Action
  - Adventure
  - Comedy
  - Harem
  - Martial_Arts
  - Wuxia
fileClass: novel
aliases:
  - Martial Arts Ain't That Big of a Deal
status: Plan-to-Read
author: Suerte
source-url: https://www.novelupdates.com/series/martial-arts-aint-that-big-of-a-deal/
total-chapters: 30
current-chapter: 1
side-stories-total: 0
side-stories-read: 0
rating: 4
description: I fell into a wannabe murim. But apparently martial arts is supposed to be difficult? Hm… Is it really that bad?
genre: []
cssclasses:
  - novel-page
---

# Martial Arts Ain't That Big of a Deal

![[covers/Martial_Arts_Aint_That_Big_of_a_Deal.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/martial-arts-aint-that-big-of-a-deal/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c1`, latest `c30`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
