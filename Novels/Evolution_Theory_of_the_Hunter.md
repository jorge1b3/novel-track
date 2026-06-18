---
tags:
  - novel
  - Action
  - Adventure
  - Drama
  - Fantasy
  - Harem
  - Mystery
  - Psychological
  - Romance
  - Seinen
  - Supernatural
fileClass: novel
aliases:
  - Evolution Theory of the Hunter
status: Dropped
author: 음란파괴왕
source-url: https://www.novelupdates.com/series/evolution-theory-of-the-hunter/
total-chapters: 201
current-chapter: 99
side-stories-total: 0
side-stories-read: 0
rating: 4
description: In a world of dungeons and monsters you can become strong if you merely have enough money. Rare skillbooks that can magically upgrade your skills in an instant are sold at exorbitant prices. So only the privileged and rich are able to buy their way to become hunters – a much revered occupation that allows one to enter dungeons and hunt monsters. Our MC is a porter, a sort of caddie for hunters. He dreams of one day becoming a hunter when he comes into possession of a skillbook. But the skill is a level 0. Something unheard of. No one wants it. People laugh at it. But he learns the skill – only to find that it may be the most amazing one yet.
genre: []
cssclasses:
  - novel-page
---

# Evolution Theory of the Hunter

![[covers/Evolution_Theory_of_the_Hunter.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/evolution-theory-of-the-hunter/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c99`, latest `c201`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
