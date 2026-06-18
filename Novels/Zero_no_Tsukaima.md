---
tags:
  - novel
  - Action
  - Adventure
  - Comedy
  - Drama
  - Ecchi
  - Fantasy
  - Harem
  - Romance
  - School_Life
  - Seinen
fileClass: novel
aliases:
  - 'Zero no Tsukaima'
status: Completed
author: 'Shimizu Yū'
source-url: 'https://www.novelupdates.com/series/zero-no-tsukaima/'
total-chapters: 22
current-chapter: 22
side-stories-total: 0
side-stories-read: 0
rating: 4
description: 'At the Tristain Magic Academy, her classmates call bumbling witch-in-training Louise Francoise le Blanc de la Valliere “Louise the Zero.” During an important coming-of-age ritual, when each student must summon their own witch’s familiar, Louise confirms her classmates’ opinion by accidentally conjuring up a normal teenage boy from Japan. Whether the two of them like it or not, the laws of magic bind them as master and servant forever! A hilarious novel with romance interwined.'
genre: []
cssclasses:
  - novel-page
---

# Zero no Tsukaima

![[covers/Zero_no_Tsukaima.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/zero-no-tsukaima/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `v22 epilogue`, latest `v22 epilogue`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
