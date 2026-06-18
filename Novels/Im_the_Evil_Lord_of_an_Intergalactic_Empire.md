---
tags:
  - novel
  - Action
  - Adventure
  - Comedy
  - Ecchi
  - Fantasy
  - Mecha
  - Sci-fi
  - Shounen
fileClass: novel
aliases:
  - I'm the Evil Lord of an Intergalactic Empire!
status: On-Hold
author: Mishima Yomu
source-url: https://www.novelupdates.com/series/im-the-evil-lord-of-an-intergalactic-empire/
total-chapters: 15
current-chapter: 11
side-stories-total: 0
side-stories-read: 0
rating: 4
description: Liam Sera Banfield is a reincarnator. He had reincarnated into a fantasy world of magic and swords, but at the time the civilization had already been making advancements into outer space. The setting takes place in an intergalactic empire, a space opera-like universe where humanoid weapons and spaceships battle. Liam, who had been reborn into an aristocratic family in a monarchic society, has the ambition to one day become an evil lord. In his previous life, Liam had unfortunately lost everything and died in despair. — It’s foolish to live for others. — I will live for myself. Keeping those feelings in his heart, he has decided to fulfill his goal, but is instead worshipped as a virtuous ruler due to his difference in values. Will Liam be able to become an evil lord?
genre: []
cssclasses:
  - novel-page
---

# I'm the Evil Lord of an Intergalactic Empire!

![[covers/Im_the_Evil_Lord_of_an_Intergalactic_Empire.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/im-the-evil-lord-of-an-intergalactic-empire/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `v11c13`, latest `v15c16`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
