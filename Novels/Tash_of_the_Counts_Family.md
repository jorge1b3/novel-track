---
tags:
  - novel
  - Action
  - Adventure
  - Drama
  - Fantasy
  - Martial_Arts
  - Seinen
  - Supernatural
fileClass: novel
aliases:
  - 'T*ash of the Count''s Family'
status: Plan-to-Read
author: 'Yu Ryeo Han'
source-url: 'https://www.novelupdates.com/series/trash-of-the-counts-family/'
total-chapters: 418
current-chapter: 418
side-stories-total: 0
side-stories-read: 0
rating: 4
description: 'When I opened my eyes, I was inside a novel. [The Birth of a Hero] . [The Birth of a Hero] was a novel focused on the adventures of the main character, Choi Han, a high school boy who was transported to a different dimension from Earth, along with the birth of the numerous heroes of the continent. I became a part of that novel as the tr*sh of the Count’s family, the family that oversaw the territory where the first village that Choi Han visits is located. The problem is that Choi Han becomes twisted after that village, and everyone in it, is destroyed by assassins. The bigger problem is the fact that this s*upid tr*sh who I’ve become doesn’t know about what happened in the village and messes with Choi Han, only to get beaten to a pulp. “…This is going to be a headache.” I feel like something serious has happened to me. But it was worth trying to make this my new life.'
genre: []
cssclasses:
  - novel-page
---

# T*ash of the Count's Family

![[covers/Tash_of_the_Counts_Family.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/trash-of-the-counts-family/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c418`, latest `v2c397`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
