---
tags:
  - novel
  - Action
  - Comedy
  - Drama
  - Martial_Arts
  - Mature
  - Romance
  - School_Life
fileClass: novel
aliases:
  - Awakening
status: Dropped
author: 令狐BEYOND
source-url: https://www.novelupdates.com/series/awakening/
total-chapters: 316
current-chapter: 189
side-stories-total: 0
side-stories-read: 0
rating: 4
description: Similar to that of a Phoenix, a martial arts expert who was from the Song Dynasty had reincarnated after his death. The body he now possessed belonged to a bullied Japanese high schooler, one that had complicated family issues.
genre: []
cssclasses:
  - novel-page
---

# Awakening

![[covers/Awakening.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/awakening/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c189`, latest `c316`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
