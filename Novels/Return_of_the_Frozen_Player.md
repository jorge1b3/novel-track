---
tags:
  - novel
  - Action
  - Adventure
  - Fantasy
  - Psychological
  - Supernatural
fileClass: novel
aliases:
  - Return of the Frozen Player
status: Dropped
author: JerryM
source-url: https://www.novelupdates.com/series/return-of-the-frozen-player/
total-chapters: 275
current-chapter: 275
side-stories-total: 0
side-stories-read: 0
rating: 4
description: 5 years after the world changed, the final boss appeared. [The final boss for area Earth, the Frost Queen, has appeared.] The final boss! If we can just defeat her, our lives will go back to normal! The top five players in the world, including Specter Seo Jun-ho, finally defeated the Frost Queen… But they fell into a deep slumber. 25 years passed. “A second floor? It didn’t end when the Frost Queen died? Specter awakes from his slumber.
genre: []
cssclasses:
  - novel-page
---

# Return of the Frozen Player

![[covers/Return_of_the_Frozen_Player.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/return-of-the-frozen-player/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c275`, latest `c87`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
