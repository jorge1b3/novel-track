---
tags:
  - novel
  - Action
  - Adventure
  - Comedy
  - Fantasy
  - Harem
fileClass: novel
aliases:
  - Overgeared
status: On-Hold
author: Park Saenal
source-url: https://www.novelupdates.com/series/overgeared/
total-chapters: 3000
current-chapter: 1729
side-stories-total: 0
side-stories-read: 0
rating: 4
description: As Shin Youngwoo had an unfortunate life and is now stuck carrying bricks on construction sites. He even had to do labor in the most popular VR game, Satisfy! However, luck would soon enter his hopeless life. His character, ‘Grid’, would discover the Northern End Cave for a quest, and in that place, he would find ‘Pagma’s Rare Book’ and will become a legend…
genre: []
cssclasses:
  - novel-page
---

# Overgeared

![[covers/Overgeared.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/overgeared/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c1729`, latest `c1`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
