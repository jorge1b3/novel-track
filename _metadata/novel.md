---
tags:
  - novel
fields:
  - name: status
    type: Select
    options:
      source: ValuesList
      values:
        - Reading
        - On-Hold
        - Completed
        - Plan-to-Read
        - Dropped
  - name: type
    type: Select
    options:
      source: ValuesList
      values:
        - Web Novel
        - Light Novel
        - Korean Web Novel
        - Chinese Web Novel
        - Japanese Light Novel
  - name: author
    type: Input
  - name: source-url
    type: Input
  - name: total-chapters
    type: Number
    options:
      min: 0
      step: 1
  - name: current-chapter
    type: Number
    options:
      min: 0
      step: 1
  - name: rating
    type: Number
    options:
      min: 0
      max: 5
      step: 0.5
  - name: description
    type: Input
  - name: cover
    type: Input
  - name: genre
    type: Multi
    options:
      source: ValuesList
      values:
        - Action
        - Adventure
        - Comedy
        - Drama
        - Fantasy
        - Romance
        - Sci-Fi
        - Slice of Life
        - Horror
        - Mystery
        - Thriller
        - Isekai
        - Reincarnation
        - Magic
        - Martial Arts
        - Harem
        - System
        - Dungeon
        - Kingdom Building
        - School Life
genre: []
---

# novel

File class for novel tracking.
