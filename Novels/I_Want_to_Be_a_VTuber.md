---
tags:
  - novel
  - Comedy
  - Drama
  - Gender_Bender
  - Psychological
  - School_Life
  - Shounen
  - Slice_of_Life
fileClass: novel
aliases:
  - I Want to Be a VTuber
status: Plan-to-Read
author: 플라나리아햄버거
source-url: https://www.novelupdates.com/series/i-want-to-be-a-vtuber/
total-chapters: 30
current-chapter: 30
side-stories-total: 0
side-stories-read: 0
rating: 4
description: I definitely just wanted to be a VTuber… But when I came to my senses, I had become an actor.
genre: []
cssclasses:
  - novel-page
---

# I Want to Be a VTuber

![[covers/I_Want_to_Be_a_VTuber.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/i-want-to-be-a-vtuber/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c30`, latest `c0`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
