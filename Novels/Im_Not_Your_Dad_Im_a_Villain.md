---
tags:
  - novel
  - Action
  - Harem
  - Romance
  - Supernatural
fileClass: novel
aliases:
  - I'm Not Your Dad, I'm a Villain
status: Dropped
author: 글로벌레
source-url: https://www.novelupdates.com/series/im-not-your-dad-im-a-villain/
total-chapters: 105
current-chapter: 25
side-stories-total: 0
side-stories-read: 0
rating: 4
description: Until the day the promised time comes. I will play the role of her father.
genre: []
cssclasses:
  - novel-page
---

# I'm Not Your Dad, I'm a Villain

![[covers/Im_Not_Your_Dad_Im_a_Villain.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/im-not-your-dad-im-a-villain/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c25`, latest `c105`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
