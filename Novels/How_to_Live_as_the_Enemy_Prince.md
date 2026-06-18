---
tags:
  - novel
  - Adventure
  - Comedy
  - Drama
  - Fantasy
  - Mystery
  - Shounen
fileClass: novel
aliases:
  - 'How to Live as the Enemy Prince'
status: Plan-to-Read
author: 'Cha Seo Hyeon'
source-url: 'https://www.novelupdates.com/series/how-to-live-as-the-enemy-prince/'
total-chapters: 269
current-chapter: 0
side-stories-total: 0
side-stories-read: 0
rating: 4
description: 'I could hear the hum of life in my ears. It was hard to breathe…. … I raised my gaze and stared into the distance. However, my blurred vision could not see anything. The light began to fade. That was my last memory. When I opened my eyes once again, it was 10 years before that last memory took place. And of all the things I could have become, it was from the enemy country that drove Secretia to ruin – I became Kyris’ third prince Calian.'
genre: []
cssclasses:
  - novel-page
---

# How to Live as the Enemy Prince

![[covers/How_to_Live_as_the_Enemy_Prince.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/how-to-live-as-the-enemy-prince/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `prologue`, latest `c269`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
