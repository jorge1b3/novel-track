---
tags:
  - novel
  - Action
  - Adventure
  - Fantasy
  - School_Life
fileClass: novel
aliases:
  - 'Academy''s Genius Swordsman'
status: Reading
author: 'Seogwando'
source-url: 'https://www.novelupdates.com/series/academys-genius-swordsman/'
total-chapters: 329
current-chapter: 115
side-stories-total: 0
side-stories-read: 0
rating: 4
description: 'The Swordmaster who has returned by chance to save the world!'
genre: []
cssclasses:
  - novel-page
---

# Academy's Genius Swordsman

![[covers/Academys_Genius_Swordsman.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/academys-genius-swordsman/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c115`, latest `c329`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
