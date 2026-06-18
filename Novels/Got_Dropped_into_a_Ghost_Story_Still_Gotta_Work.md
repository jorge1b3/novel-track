---
tags:
  - novel
  - Action
  - Adventure
  - Comedy
  - Drama
  - Horror
  - Mature
  - Mystery
  - Psychological
  - Seinen
  - Supernatural
fileClass: novel
aliases:
  - 'Got Dropped into a Ghost Story, Still Gotta Work'
status: Plan-to-Read
author: 'Baek Deok-su'
source-url: 'https://www.novelupdates.com/series/got-dropped-into-a-ghost-story-still-gotta-work/'
total-chapters: 298
current-chapter: 1
side-stories-total: 0
side-stories-read: 0
rating: 4
description: 'NOW HIRING — URGENT — Ghost Story Specialist Corporation Daydream Inc. (Ltd.) Insane Benefits – Come to Work Immediately ※ Note : The company is not liable for any injuries or fatalities that may occur during the course of the employee’s duties. —— A pop-up event for some ‘modern fantasy’ media I loved so much that I even took a precious day off work to attend. On that day, I ended up transmigrating as a character in that very fantasy world. As none other than a newly hired employee at a famous large corporation! A dream job with great benefits, an excellent salary, and even kind and competent bosses. I’m using the information I know about the world to rise through the ranks at lightning speed! Am I happy, you ask? Please, just let me go home. I’m begging you. ※ Note : The genre is horror.'
genre: []
cssclasses:
  - novel-page
---

# Got Dropped into a Ghost Story, Still Gotta Work

![[covers/Got_Dropped_into_a_Ghost_Story_Still_Gotta_Work.webp|100|left]]

> [Read Here](https://www.novelupdates.com/series/got-dropped-into-a-ghost-story-still-gotta-work/)

| | |
| --- | --- |
| **Status** | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating** | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]` |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres** | `=this.file.tags` |

_NU: my chapter `c1 part1`, latest `c298`_

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
