---
tags:
  - novel
  - Action
  - Adventure
  - Fantasy
  - Harem
  - Martial_Arts
  - Shounen
fileClass: novel
aliases:
  - Possessing Nothing
status: On-Hold
author: Mogma
source-url: https://www.novelupdates.com/series/possessing-nothing/
total-chapters: 408
current-chapter: 312
side-stories-total: 0
side-stories-read: 0
rating: 4
description: C-class mercenary. Started as a No Class, possessing nothing. 13 years of survival in the depths of the ditches. Somehow, I’ve managed to return to the very beginning of my struggle, but…
genre: []
cssclasses:
  - novel-page
---

# Possessing Nothing

![[covers/Possessing_Nothing.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/possessing-nothing/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c312`, latest `c408`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
