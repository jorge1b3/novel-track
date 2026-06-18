---
tags:
  - novel
  - Action
  - Adventure
  - Fantasy
  - Mature
  - Mystery
  - Psychological
  - Sci-fi
  - Seinen
  - Supernatural
  - Tragedy
fileClass: novel
aliases:
  - Genius Warlock
status: Plan-to-Read
author: 노란커피
source-url: https://www.novelupdates.com/series/genius-warlock/
total-chapters: 213
current-chapter: 1
side-stories-total: 0
side-stories-read: 0
rating: 4
description: The tale of Oliver. An orphan boy from a Mine in 19th century Europe, filled with Magic.
genre: []
cssclasses:
  - novel-page
---

# Genius Warlock

![[covers/Genius_Warlock.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/genius-warlock/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c1`, latest `c213`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
