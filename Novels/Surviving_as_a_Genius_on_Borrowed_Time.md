---
tags:
  - novel
  - Action
  - Martial_Arts
  - Wuxia
fileClass: novel
aliases:
  - Surviving as a Genius on Borrowed Time
status: Dropped
author: Cheong Shi-so
source-url: https://www.novelupdates.com/series/surviving-as-a-genius-on-borrowed-time/
total-chapters: 829
current-chapter: 32
side-stories-total: 0
side-stories-read: 0
rating: 4
description: With unmatched talent, but a fate sealed by a terminal illness, Jeong Yeon-shin challenges his destined death for a chance to live. Set in a realm where elves and dwarves coexist with martial artists, this is the story of Jeong Yeon-shin, a genius fighting to extend his life against all odds.
genre: []
cssclasses:
  - novel-page
---

# Surviving as a Genius on Borrowed Time

![[covers/Surviving_as_a_Genius_on_Borrowed_Time.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/surviving-as-a-genius-on-borrowed-time/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c32`, latest `c829`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
