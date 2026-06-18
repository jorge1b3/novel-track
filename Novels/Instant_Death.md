---
tags:
  - novel
  - Action
  - Adventure
  - Comedy
  - Fantasy
  - Shounen
fileClass: novel
aliases:
  - Instant Death
status: Dropped
author: Tsuyoshi Fujitaka
source-url: https://www.novelupdates.com/series/instant-death/
total-chapters: 5
current-chapter: 1
side-stories-total: 0
side-stories-read: 0
rating: 4
description: Growth cheats? Infinite magic power? The ability to utilize all archetypes? What’s the point if instant death ends everything with a single attack? High school senior Yogiri Takatou was on a school field trip when he woke up to a dragon assaulting his sightseeing bus, with the only ones still on the bus being him and his female classmate, the panicking Tomochika Dannoura. Apparently the rest of his classmates had been given special powers by Sion, a woman who introduced herself as Sage, and escaped from the dragon, leaving those that hadn’t received any special powers behind as dragon bait. And so Yogiri was thrown into a parallel universe full of danger, with no idea of what just happened. Likewise, Sion had no way of knowing just what kind of being she had summoned to her world.
genre: []
cssclasses:
  - novel-page
---

# Instant Death

![[covers/Instant_Death.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/instant-death/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `v1c1`, latest `after 5`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
