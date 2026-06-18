---
tags:
  - novel
  - Action
  - Adventure
  - Scifi
  - Slice_of_Life
fileClass: novel
aliases:
  - 'Ranker''s Return'
status: Plan-to-Read
author: 'Yeong Biram'
source-url: 'https://www.novelupdates.com/series/rankers-return/'
total-chapters: 8
current-chapter: 1
side-stories-total: 0
side-stories-read: 0
rating: 4
date-started: 
date-completed: 
description: 'The early days of the virtual reality game, Arena. Meleegod was the strongest ranked player! He deleted his character and suddenly left. In order to restore his bankrupt family, he returned to Arena! “Do you want to create a character?”'
genre: []
cssclasses:
  - novel-page
---

# Ranker's Return

![[covers/Rankers_Return.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/rankers-return/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `prologue+c1`, latest `v8c82`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```

## Thoughts & Review
* **What I Liked**: 
* **What I Disliked**: 
* **Key Characters / Arcs**: 
* **Overall Impressions**: 
