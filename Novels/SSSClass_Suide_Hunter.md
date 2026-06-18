---
tags:
  - novel
  - Action
  - Adventure
  - Comedy
  - Fantasy
  - Martial_Arts
  - Tragedy
fileClass: novel
aliases:
  - SSS-Class Sui**de Hunter
status: On-Hold
author: Sinnoa
source-url: https://www.novelupdates.com/series/sss-class-suicide-hunter/
total-chapters: 272
current-chapter: 272
side-stories-total: 0
side-stories-read: 0
rating: 4
description: I am dying to have a Class S Skill! [You have received a Class S Skill.] [However, you will die if you use the Skill.] ..I didn’t mean it literally.
genre: []
cssclasses:
  - novel-page
---

# SSS-Class Sui**de Hunter

![[covers/SSSClass_Suide_Hunter.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/sss-class-suicide-hunter/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c272`, latest `c269`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
