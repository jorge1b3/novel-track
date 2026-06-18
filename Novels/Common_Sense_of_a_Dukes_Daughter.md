---
tags:
  - novel
  - Drama
  - Fantasy
  - Romance
  - Shoujo
  - Slice_of_Life
fileClass: novel
aliases:
  - Common Sense of a Duke's Daughter
status: Dropped
author: Reia
source-url: https://www.novelupdates.com/series/common-sense-of-a-dukes-daughter/
total-chapters: 267
current-chapter: 1
side-stories-total: 0
side-stories-read: 0
rating: 4
description: When a young woman is killed in a traffic accident on her way home from work at a tax bureau, she suddenly finds herself transported to the world of the otome game she was playing the night before – but instead of the heroine, she’s been reincarnated as the villainess! Using her knowledge of the game, “Iris” manages to avert personal disaster and decides to rebuild her life with her modern-day economic know-how. This is one mean girl who isn’t going to let her perceived reputation stop her from being a heroine!
genre: []
cssclasses:
  - novel-page
---

# Common Sense of a Duke's Daughter

![[covers/Common_Sense_of_a_Dukes_Daughter.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/common-sense-of-a-dukes-daughter/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `v1c1`, latest `c267`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
