---
tags:
  - novel
  - Action
  - Fantasy
  - Shounen
fileClass: novel
aliases:
  - A Player Who Eats Metal
status: Completed
author: 지점장
source-url: https://www.novelupdates.com/series/a-player-who-eats-metal/
total-chapters: 71
current-chapter: 71
side-stories-total: 0
side-stories-read: 0
rating: 4
description: Lee Hyunwook, who originally had the ability to control steel in the world. He tried to protect the world but ultimately failed and the world was destroyed. Following that, he was given the opportunity to return to his military days and build up efforts to prevent the world from being destroyed one by one. An army + Hunter + Regression + Savior “In this life, I’ll be a real hero.” Will Lee Hyunwook be able to save the world this time?
genre: []
cssclasses:
  - novel-page
---

# A Player Who Eats Metal

![[covers/A_Player_Who_Eats_Metal.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/a-player-who-eats-metal/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c71`, latest `c71`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
