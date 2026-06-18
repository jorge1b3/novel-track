---
tags:
  - novel
  - Action
  - Adventure
  - Fantasy
  - Mature
  - Psychological
  - Seinen
  - Supernatural
fileClass: novel
aliases:
  - 'Dungeon Hunter'
status: Completed
author: 'Onhu'
source-url: 'https://www.novelupdates.com/series/dungeon-hunter/'
total-chapters: 242
current-chapter: 242
side-stories-total: 0
side-stories-read: 0
rating: 4
description: 'I failed and will challenge again. There is no room for failure in my second life! 72 dungeons and their owners that appeared on earth. And the Awakened. I am a hunter that will devour all of them.'
genre: []
cssclasses:
  - novel-page
---

# Dungeon Hunter

![[covers/Dungeon_Hunter.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/dungeon-hunter/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c242`, latest `c242`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
