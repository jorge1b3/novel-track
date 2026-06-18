---
tags:
  - novel
  - Action
  - Adventure
  - Comedy
  - Fantasy
  - Scifi
  - Shounen
  - Slice_of_Life
fileClass: novel
aliases:
  - Reader
status: Dropped
author: Kang Cheol-Mil
source-url: https://www.novelupdates.com/series/reader/
total-chapters: 292
current-chapter: 0
side-stories-total: 0
side-stories-read: 0
rating: 4
description: While reading a book, a sparkle of light disappeared. And, as it did, a message appeared. [Wisdom increased by 1]
genre: []
cssclasses:
  - novel-page
---

# Reader

![[covers/Reader.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/reader/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `prologue`, latest `c292`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
