---
tags:
  - novel
  - Action
  - Comedy
  - Fantasy
  - Slice_of_Life
fileClass: novel
aliases:
  - The Greatest Estate Designer
status: Dropped
author: BK_Moon
source-url: https://www.novelupdates.com/series/the-greatest-estate-designer/
total-chapters: 194
current-chapter: 1
side-stories-total: 0
side-stories-read: 0
rating: 4
description: The only son of a country side baron, who is called tr*sh and hated by his family, subordinates, and every citizen of the fief. One day, he suddenly loses consciousness, and when he opens his eyes… Inside his body was… a Korean civil engineer.
genre: []
cssclasses:
  - novel-page
---

# The Greatest Estate Designer

![[covers/The_Greatest_Estate_Designer.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/the-greatest-estate-designer/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c1`, latest `c194`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
