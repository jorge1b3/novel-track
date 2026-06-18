---
tags:
  - Action
  - Comedy
  - Drama
  - Fantasy
  - Harem
  - Psychological
  - Romance
  - School_Life
  - Shounen
  - novel
fileClass: novel
aliases:
  - A Villain's Will to Survive
status: Completed
author: Jee Gab Song
source-url: https://www.novelupdates.com/series/a-villains-will-to-survive/
total-chapters: 361
current-chapter: 361
side-stories-total: 0
side-stories-read: 0
rating: 3
description: "The middle boss of the AAA-class game produced by the company. The villain who dies 999 times out of 1,000 times. Deculein. That person, was me now. “You’re going to die on almost every route.” Dyein, like all villains, inevitably dies. [First and foremost survival goal: Be what the game requires you to be] I’ll have to survive even if it means twisting my fate if I am destined to die."
genre: []
cssclasses:
  - novel-page
---

# A Villain's Will to Survive

![[covers/A_Villains_Will_to_Survive.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/a-villains-will-to-survive/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c361`, latest `c20`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
