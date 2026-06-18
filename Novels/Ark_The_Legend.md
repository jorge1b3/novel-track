---
tags:
  - novel
  - Action
  - Adventure
  - Comedy
  - Drama
  - Fantasy
  - Scifi
  - Seinen
  - Slice_of_Life
fileClass: novel
aliases:
  - Ark The Legend
status: Plan-to-Read
author: Yoo Seong
source-url: https://www.novelupdates.com/series/ark-the-legend/
total-chapters: 16
current-chapter: 16
side-stories-total: 0
side-stories-read: 0
rating: 4
description: A new game which the nation has dived into. From the bloody battlefields to the pyramids of ancient times, head into the colourful world of Galaxian. The glorious days of the legendary gamer Ark is over. From finding a job to saving the party from a humiliating death, nothing is easily solved……
genre: []
cssclasses:
  - novel-page
---

# Ark The Legend

![[covers/Ark_The_Legend.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/ark-the-legend/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `v16c9 part2`, latest `c13`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
