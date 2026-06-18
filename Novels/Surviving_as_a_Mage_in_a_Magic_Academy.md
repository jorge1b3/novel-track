---
tags:
  - novel
  - Comedy
  - Fantasy
  - School_Life
  - Shounen
  - Slice_of_Life
fileClass: novel
aliases:
  - Surviving as a Mage in a Magic Academy
status: Plan-to-Read
author: Writing Machine
source-url: https://www.novelupdates.com/series/surviving-as-a-mage-in-a-magic-academy/
total-chapters: 1038
current-chapter: 1
side-stories-total: 0
side-stories-read: 0
rating: 4
description: Graduate student Yi-han finds himself reborn in another world as the youngest child of a mage family. “I’m never attending school, ever again!” “What do you wish to achieve in life?” “I wish to play around and live comfortab-.” “You must be aware of your talent. Now go attend Einrogard!” “Patriarch!” My future will be secured once I graduate. For my future!
genre: []
cssclasses:
  - novel-page
---

# Surviving as a Mage in a Magic Academy

![[covers/Surviving_as_a_Mage_in_a_Magic_Academy.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/surviving-as-a-mage-in-a-magic-academy/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c1`, latest `c1038`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
