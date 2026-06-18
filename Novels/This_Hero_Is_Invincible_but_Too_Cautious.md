---
tags:
  - novel
  - Action
  - Adventure
  - Comedy
  - Fantasy
  - Romance
fileClass: novel
aliases:
  - This Hero Is Invincible but Too Cautious
status: Dropped
author: Tsuchihi Light
source-url: https://www.novelupdates.com/series/this-hero-is-invincible-but-too-cautious/
total-chapters: 4
current-chapter: 1
side-stories-total: 0
side-stories-read: 0
rating: 4
description: "Lista, a Goddess from the God’s realm, has a huge task to accomplish. She must save the world Geabrande (with a S-rank difficulty salvation) from evil threats. To perform this task, she summons a hero from Planet Earth called Ryuguuin Seiya. This hero is exceptional and fully capable, but has one major problem: he is unbelievably cautious."
genre: []
cssclasses:
  - novel-page
---

# This Hero Is Invincible but Too Cautious

![[covers/This_Hero_Is_Invincible_but_Too_Cautious.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/this-hero-is-invincible-but-too-cautious/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `v1c0`, latest `v4c198 part2`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
