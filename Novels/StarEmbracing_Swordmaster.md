---
tags:
  - novel
  - Action
  - Adventure
  - Fantasy
  - Romance
  - Shounen
fileClass: novel
aliases:
  - Star-Embracing Swordmaster
status: Dropped
author: Q10
source-url: https://www.novelupdates.com/series/star-embracing-swordmaster/
total-chapters: 14
current-chapter: 14
side-stories-total: 0
side-stories-read: 0
rating: 4
description: Vlad, a destitute youngster from the slums, held an unwavering admiration for knights. Following an encounter with a bolt of black lightning, he started hearing a mysterious voice. One fateful day, a knight cloaked in the shimmering glow of the blue moonlight appeared, completely upending Vlad’s existence in the back alleys. This extraordinary event proved that even a faint star concealed among the darkest corners of the nocturnal firmament can still radiate its brilliance, should it yearn to shine.
genre: []
cssclasses:
  - novel-page
---

# Star-Embracing Swordmaster

![[covers/StarEmbracing_Swordmaster.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/star-embracing-swordmaster/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c14 part2`, latest `ss8`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
