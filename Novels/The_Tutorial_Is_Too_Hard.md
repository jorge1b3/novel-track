---
tags:
  - novel
  - Action
  - Adventure
  - Fantasy
  - Psychological
  - Seinen
  - Supernatural
  - Tragedy
fileClass: novel
aliases:
  - The Tutorial Is Too Hard
status: On-Hold
author: Gandara
source-url: https://www.novelupdates.com/series/the-tutorial-is-too-hard/
total-chapters: 53
current-chapter: 40
side-stories-total: 0
side-stories-read: 0
rating: 4
description: "On a normal boring day, a message appears, inviting him to a Tutorial. A tale about Lee Ho Jae and his escape from the Tutorial. But he just happened to choose the hardest possible difficulty: Hell…"
genre: []
cssclasses:
  - novel-page
---

# The Tutorial Is Too Hard

![[covers/The_Tutorial_Is_Too_Hard.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/the-tutorial-is-too-hard/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c1`, latest `ss 53`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
