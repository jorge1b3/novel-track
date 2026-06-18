---
tags:
  - novel
  - Action
  - Adventure
  - Comedy
  - Fantasy
  - Harem
  - Mystery
  - Sci-fi
  - Shounen
  - Supernatural
fileClass: novel
aliases:
  - 'Everyone Else is a Returnee'
status: Completed
author: 'Toika'
source-url: 'https://www.novelupdates.com/series/everyone-else-is-a-returnee/'
total-chapters: 25
current-chapter: 25
side-stories-total: 0
side-stories-read: 0
rating: 4
description: 'Yu Ilhan was always the one left behind. Left out of cliques in school. Left out of social invitations. Just…always left out. Except now he’s been left behind for real. When Earth’s future is threatened, Yu Ilhan stays behind while the rest of the population flees to other planets for safety. It’s up to Yu Ilhan to save our planet before it’s too late!'
genre: []
cssclasses:
  - novel-page
---

# Everyone Else is a Returnee

![[covers/Everyone_Else_is_a_Returnee.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/everyone-else-is-a-returnee/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `ss 25`, latest `prologue`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
