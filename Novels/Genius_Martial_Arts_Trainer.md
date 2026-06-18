---
tags:
  - novel
  - Action
  - Comedy
  - Fantasy
  - Harem
  - Martial_Arts
  - Shounen
  - Wuxia
fileClass: novel
aliases:
  - Genius Martial Arts Trainer
status: Completed
author: 크루크루
source-url: https://www.novelupdates.com/series/genius-martial-arts-trainer/
total-chapters: 375
current-chapter: 375
side-stories-total: 0
side-stories-read: 0
rating: 4
description: Cho Kang-hyuk, the owner of a large fitness center, woke up to find himself as a young disciple at Shaolin Temple.
genre: []
cssclasses:
  - novel-page
---

# Genius Martial Arts Trainer

![[covers/Genius_Martial_Arts_Trainer.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/genius-martial-arts-trainer/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c56`, latest `c372`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
