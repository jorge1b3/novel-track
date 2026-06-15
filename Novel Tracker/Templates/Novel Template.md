<%*
const displayTitle = await tp.system.prompt("Novel title");
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

let unreadSection = "";
if (currentCh < totalCh) {
  const start = currentCh + 1;
  if (start === totalCh) {
    unreadSection = "\n\n### Unread\n- [ ] Chapter " + totalCh;
  } else {
    unreadSection = "\n\n### Unread\n- [ ] Chapters " + start + "-" + totalCh;
  }
}

const chaptersText = currentCh < totalCh
  ? `Chapters: ${currentCh} / ${totalCh}`
  : `Up to date · Chapter ${totalCh}`;

tR += `---
fileClass: novel
tags:
  - novel
aliases:
  - ${yamlStr(displayTitle)}
status: Reading
type: Web Novel
author: ${yamlStr(author)}
source-url: ${yamlStr(sourceUrl)}
total-chapters: ${totalCh}
current-chapter: ${currentCh}
rating:
description: ${yamlStr(description)}
---

# ${displayTitle}

![[covers/${slug}.webp|100|left]]

${description}

> **Author:** ${author} · **${chaptersText}** · [Read Here](${sourceUrl})

---

## Chapter Log

### Read
- [x] Chapters 1-${currentCh}${unreadSection}
`;
_%>
