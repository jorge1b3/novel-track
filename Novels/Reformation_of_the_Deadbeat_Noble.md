---
tags:
  - novel
  - Action
  - Adventure
  - Drama
  - Fantasy
  - Romance
  - Shounen
fileClass: novel
aliases:
  - Reformation of the Deadbeat Noble
status: Dropped
author: Ideungbyeol
source-url: https://www.novelupdates.com/series/reformation-of-the-deadbeat-noble/
total-chapters: 387
current-chapter: 118
side-stories-total: 0
side-stories-read: 0
rating: 4
description: Airen Parreira is a boy who sleeps to run away from reality. People mocked him, calling him a ‘deadbeat’, but he had no wish to change. Until one day, he dreamt of a swordsman… It was a dream about a talentless man who had been training by swinging his sword for decades.
genre: []
cssclasses:
  - novel-page
---

# Reformation of the Deadbeat Noble

![[covers/Reformation_of_the_Deadbeat_Noble.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/reformation-of-the-deadbeat-noble/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c118`, latest `c387`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
