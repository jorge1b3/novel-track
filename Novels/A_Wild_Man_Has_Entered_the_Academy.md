---
tags:
  - novel
  - Action
  - Adventure
  - Comedy
  - Fantasy
  - Harem
  - Romance
  - School_Life
  - Shounen
fileClass: novel
aliases:
  - A Wild Man Has Entered the Academy
status: Plan-to-Read
author: 두부두부
source-url: https://www.novelupdates.com/series/a-wild-man-has-entered-the-academy/
total-chapters: 166
current-chapter: 166
side-stories-total: 0
side-stories-read: 0
rating: 4
description: Typically, most novels begin in a city, but I ended up in a forest.
genre: []
cssclasses:
  - novel-page
---

# A Wild Man Has Entered the Academy

![[covers/A_Wild_Man_Has_Entered_the_Academy.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/a-wild-man-has-entered-the-academy/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c166`, latest `c20`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
