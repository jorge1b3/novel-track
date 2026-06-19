<%*
const displayTitle = await tp.system.prompt("Side Story title");
const parentNovel = await tp.system.prompt("Parent Novel title or [[Link]]");
const author = await tp.system.prompt("Author name");
const sourceUrl = await tp.system.prompt("Source URL");
const totalCh = parseInt(await tp.system.prompt("Total chapters released") || 0);
const currentCh = parseInt(await tp.system.prompt("Last read chapter number") || 0);
const description = await tp.system.prompt("Short description (optional)") || "";

// Sanitize filename: only a-zA-Z, spaces → _
const slug = displayTitle.replace(/[^a-zA-Z0-9 ]/g, '').replace(/ /g, '_').replace(/_+/g, '_').replace(/^_|_$/g, '');
if (slug) await tp.file.rename(slug);

function yamlStr(s) {
  if (!s || s.trim() === "") return "";
  return "'" + s.replace(/'/g, "''") + "'";
}

let parentLink = parentNovel.trim();
if (parentLink && !parentLink.startsWith("[[")) {
  parentLink = "[[" + parentLink + "]]";
}



tR += `---
fileClass: side-story
cssclasses:
  - novel-page
tags:
  - side-story
aliases:
  - ${yamlStr(displayTitle)}
parent: ${parentLink}
status: Reading
author: ${yamlStr(author)}
source-url: ${yamlStr(sourceUrl)}
total-chapters: ${totalCh}
current-chapter: ${currentCh}
rating:
date-started: 
date-completed: 
description: ${yamlStr(description)}
---

# ${displayTitle}

> **Parent Novel:** ${parentLink}
> **Author:** ${author} · [Read Here](${sourceUrl})

| | |
| --- | --- |
| **Status** | \`INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]\` |
| **Rating** | \`INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]\` |
| **Progress** | \`INPUT[number:current-chapter]\` / \`INPUT[number:total-chapters]\` ch |

---

## Thoughts & Review
* **What I Liked**: 
* **What I Disliked**: 
* **Key Characters / Arcs**: 
* **Overall Impressions**: 
`;
_%>
