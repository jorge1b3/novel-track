---
fileClass: novel
cssclasses:
  - novel-page
tags:
  - novel
  - Action
  - Adventure
  - Fantasy
  - Psychological
  - Sci-fi
  - Shounen
  - Space
aliases:
  - Level 4 Human in a Ruined World
status: Dropped
type: Web Novel
author: Oetu
source-url: https://www.novelupdates.com/series/level-4-human-in-a-ruined-world/
total-chapters: 659
current-chapter: 300
side-stories-total: 0
side-stories-read: 0
rating: 3
description: 'Level 4 Human in a Destroyed World (멸망한 세계 de la 4급 인간) is a dark comedy, apocalyptic sci-fi web novel that subverts traditional "system" tropes through a unique cosmic lens.The Plot: The apocalypse hits Earth because half of humanity secretly desires the destruction of the world. A cosmic system initiates a "Vote of Extinction," allowing people to cast negative karma at those they hate. However, the catch is that those voted down return as vengeful, mutated monsters.The Protagonist: Jung Youngwoo, a 34-year-old factory worker, is chosen as a brand ambassador by Dogo, an infamous intergalactic arms-dealing corporation. Armed with absurdly powerful sci-fi weapons, he takes control of Seoul by intentionally choosing to distribute rewards and karma evenly to survivors rather than hoarding them.The Scale: The story starts as an urban survival struggle featuring bizarres outfits, corrupted chaebols, and a mother who mutates into a massive dragon. However, it quickly escalates into a massive space opera when the protagonist literally converts the entire Solar System into a giant spaceship to sail across the universe and make alliances with alien worlds.'
---

# Level 4 Human in a Ruined World

![[covers/Level_4_Human_in_a_Ruined_World.webp|100|left]]

**_Level 4 Human in a Destroyed World_** is an action-packed apocalyptic sci-fi novel with dark comedy elements that follows Jung Youngwoo, a pragmatic 34-year-old factory worker who survives a unique, malice-driven system apocalypse by becoming a brand ambassador for an intergalactic arms-dealing corporation. The story starts as a gritty urban survival struggle in South Korea where public perception dictates power, but it quickly subverts traditional tropes by escalating into a massive space opera filled with sci-fi weaponry, planetary politics, and cosmic exploration.

> **Author:** Oetu · [Read Here](https://www.novelupdates.com/series/level-4-human-in-a-ruined-world/)

|              |                                                                                                                          |
| ------------ | ------------------------------------------------------------------------------------------------------------------------ |
| **Status**   | `INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]` |
| **Rating**   | `INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]`             |
| **Progress** | `INPUT[number:current-chapter]` / `INPUT[number:total-chapters]` ch                                                      |
| **Side Stories** | `INPUT[number:side-stories-read]` / `INPUT[number:side-stories-total]` ch |
| **Genres**   | `=this.file.tags`                                                                                                        |

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```
