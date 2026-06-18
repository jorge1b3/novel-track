---
tags:
  - novel
  - Action
  - Adventure
  - Fantasy
  - Harem
  - Martial_Arts
  - Romance
  - School_Life
  - Seinen
fileClass: novel
aliases:
  - 'The Master of the Brave'
status: Plan-to-Read
author: 'Mitsuoka You'
source-url: 'https://www.novelupdates.com/series/the-master-of-the-brave/'
total-chapters: 1
current-chapter: 1
side-stories-total: 0
side-stories-read: 0
rating: 4
description: 'After losing his parents, he yearns to become a Knight, the poor boy Wynn Byrd diligently trained himself. However, it was hopeless for him to become a Knight, because his magical power was too low, he can’t pass the Knight examination so he was labeled with the unpleasant title of 『Eternal Knight Cadet』. But one day the Brave defeated the Demon King and saved the world. The Brave was a peerless beauty and she gained attention from the entire world. However, the Brave declared to the world. 「I will return to my Master’s (Teacher) side, Wynn Byrd.」 This is the story about a boy who somehow changed his class from 『Eternal Knight Cadet』 to 『Brave’s Master』.'
genre: []
cssclasses:
  - novel-page
---

# The Master of the Brave

![[covers/The_Master_of_the_Brave.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/the-master-of-the-brave/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `v1c1 part1`, latest `v1c2`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
