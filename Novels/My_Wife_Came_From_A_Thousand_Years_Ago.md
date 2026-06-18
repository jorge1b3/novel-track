---
tags:
  - novel
  - Comedy
  - Drama
  - Martial_Arts
  - Mature
  - Romance
  - Slice_of_Life
fileClass: novel
aliases:
  - My Wife Came From A Thousand Years Ago
status: Dropped
author: 花还没开
source-url: https://www.novelupdates.com/series/my-wife-came-from-a-thousand-years-ago/
total-chapters: 201
current-chapter: 1
side-stories-total: 0
side-stories-read: 0
rating: 4
description: “I want to go home.” “You may not be able to go back.” “Why?” “Because it’s a long way to your house.” “How far is it?” “About twelve hundred years away,” Xu Qing directed a sympathetic gaze towards the young girl who hailed from the Tang Dynasty, “Everything you knew has become history.” Family, friends, and enemies— all silenced twelve hundred years ago…
genre: []
cssclasses:
  - novel-page
---

# My Wife Came From A Thousand Years Ago

![[covers/My_Wife_Came_From_A_Thousand_Years_Ago.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/my-wife-came-from-a-thousand-years-ago/)

|              |                                                                                                                          |
| ------------ | ------------------------------------------------------------------------------------------------------------------------ |
| **Status**   | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating**   | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]`             |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch                                                      |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres**   | `=this.file.tags`                                                                                                        |

_NU: my chapter `c1`, latest `c201`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
