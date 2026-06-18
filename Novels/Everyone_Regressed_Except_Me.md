---
tags:
  - novel
  - Action
  - Fantasy
fileClass: novel
aliases:
  - Everyone Regressed Except Me
status: Plan-to-Read
author: Writing
source-url: https://www.novelupdates.com/series/everyone-regressed-except-me/
total-chapters: 1
current-chapter: 1
side-stories-total: 0
side-stories-read: 0
rating: 4
description: "[Restarting the game.] The words materialized before Hwayoon like a hologram. “I haven’t even started yet. Restart? What is this?” Immediately after that single line appeared, shocking scenes unfolded. Kwaaaaang! An unknown creature appeared in front of Hwayoon. Everyone present wished that the scene unfolding before them was just a dream. [The only player who couldn’t regress: Lee Hwayoon.] [A Special Skill will be provided to maintain the balance of the game.] [Searching for a Special Skill.] “What? Everyone else regressed but me?” Hwayoon, a mercenary who had roamed the battlefields of the world, was well aware of regression. He had already wished countless times to return to the past. However, reality did the exact opposite. [A Special Skill has been found.] [Butterfly Effect Lv.1 – The only one that did not regress. Your actions that change the future are given bonus points.] “The flutter of a butterfly’s wings… can cause a typhoon on the other side of the world…” From the day Hwayoon received that skill… His stats began to rise without stopping."
genre: []
cssclasses:
  - novel-page
---

# Everyone Regressed Except Me

![[covers/Everyone_Regressed_Except_Me.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/everyone-regressed-except-me/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `v1c1`, latest `v1c1`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
