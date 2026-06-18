---
tags:
  - novel
  - Action
  - Adventure
  - Comedy
  - Drama
  - Fantasy
  - Martial_Arts
  - Scifi
fileClass: novel
aliases:
  - "MMORPG: Martial Gamer"
status: Dropped
author: Immortal Iron Bull
source-url: https://www.novelupdates.com/series/mmorpg-martial-gamer/
total-chapters: 138
current-chapter: 1
side-stories-total: 0
side-stories-read: 0
rating: 4
description: Catching arrows, running up walls, crushing boulders and bending metal, these are but petty parlour tricks in the eyes of martial artists. But where can a genuine martial artist stand in an era where martial artists are nothing more than a myth? Wang Yu, the most peerless martial prodigy the world has ever seen, elopes with his wife to escape an arranged marriage that was set for him as a child. Now aimless and living off his wife, Wang Yu explores the world of “Rebirth,” to seek a living. Rebirth is a world where dragons, demons and immortals are more than just legends, and Wang Yu is set to make a legend of his own.
genre: []
cssclasses:
  - novel-page
---

# MMORPG: Martial Gamer

![[covers/MMORPG_Martial_Gamer.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/mmorpg-martial-gamer/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c1`, latest `c138`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
