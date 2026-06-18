<%*
const displayTitle = await tp.system.prompt("Novel title");
const sourceUrl = await tp.system.prompt("Source URL or NovelUpdates Link (optional)") || "";
const totalCh = parseInt(await tp.system.prompt("Total chapters released") || 0);
const currentCh = parseInt(await tp.system.prompt("Last read chapter number") || 0);

// Sanitize filename: only a-zA-Z, spaces → _
const slug = displayTitle.replace(/[^a-zA-Z0-9 ]/g, '').replace(/ /g, '_').replace(/_+/g, '_').replace(/^_|_$/g, '');
if (slug) await tp.file.rename(slug);

let author = "";
let description = "";
let fetchedTags = [];
let coverDownloaded = false;

const vaultPath = app.vault.adapter.getBasePath();
const cp = (typeof require !== 'undefined') ? require('child_process') : window.require('child_process');

if (sourceUrl && sourceUrl.trim() !== "") {
  if (sourceUrl.includes("novelupdates.com/series/")) {
    const scriptPath = vaultPath + "/Novel Tracker/fetch_metadata_api.py";
    const safeUrl = sourceUrl.replace(/"/g, '\\"');
    const safeTitle = displayTitle.replace(/"/g, '\\"');
    
    const stdout = await new Promise((resolve) => {
      cp.exec(`python3 "${scriptPath}" "${safeUrl}" "${safeTitle}"`, (error, stdout, stderr) => {
        resolve(stdout);
      });
    });
    
    try {
      const data = JSON.parse(stdout);
      if (data.author) author = data.author;
      if (data.description) description = data.description;
      if (data.genres) fetchedTags = data.genres;
      if (data.cover_downloaded) coverDownloaded = true;
    } catch (e) {
      console.error("Error parsing fetched metadata:", e);
    }
  }
}

// Fallback prompts if metadata wasn't fetched
if (!author) {
  author = await tp.system.prompt("Author name") || "";
}
if (!description) {
  description = await tp.system.prompt("Short description (optional)") || "";
}

// Fallback cover download if cover was not downloaded via NovelUpdates API
if (!coverDownloaded) {
  const coverUrl = await tp.system.prompt("Novel cover URL (optional)") || "";
  if (coverUrl && coverUrl.trim() !== "") {
    const scriptPath = vaultPath + "/Novel Tracker/download_cover.py";
    const safeUrl = coverUrl.replace(/"/g, '\\"');
    const safeTitle = displayTitle.replace(/"/g, '\\"');
    await new Promise((resolve) => {
      cp.exec(`python3 "${scriptPath}" "${safeUrl}" "${safeTitle}"`, (error, stdout, stderr) => {
        resolve();
      });
    });
  }
}

function yamlStr(s) {
  if (!s || s.trim() === "") return "";
  return "'" + s.replace(/'/g, "''") + "'";
}

let tagsYaml = "tags:\n  - novel";
if (fetchedTags && fetchedTags.length > 0) {
  tagsYaml += "\n" + fetchedTags.map(t => `  - ${t}`).join("\n");
}



tR += `---
fileClass: novel
cssclasses:
  - novel-page
${tagsYaml}
aliases:
  - ${yamlStr(displayTitle)}
status: Reading
type: Web Novel
author: ${yamlStr(author)}
source-url: ${yamlStr(sourceUrl)}
total-chapters: ${totalCh}
current-chapter: ${currentCh}
side-stories-total: 0
side-stories-read: 0
rating:
date-started: 
date-completed: 
description: ${yamlStr(description)}
---

# ${displayTitle}

![[covers/${slug}.webp|100|left]]

${description}

> **Author:** ${author} · [Read Here](${sourceUrl})

| | |
| --- | --- |
| **Status** | \`INPUT[inlineSelect(option(Reading), option(Plan-to-Read), option(Completed), option(Dropped), option(On-Hold)):status]\` |
| **Rating** | \`INPUT[inlineSelect(option(1, ⭐), option(2, ⭐⭐), option(3, ⭐⭐⭐), option(4, ⭐⭐⭐⭐), option(5, ⭐⭐⭐⭐⭐)):rating]\` |
| **Progress** | \`INPUT[number:current-chapter]\` / \`INPUT[number:total-chapters]\` ch |
| **Side Stories** | \`INPUT[number:side-stories-read]\` / \`INPUT[number:side-stories-total]\` ch |
| **Genres** | \`=this.file.tags\` |

---

## Side Stories

```dataview
TABLE status AS "Status", current-chapter AS "Progress", total-chapters AS "Total"
FROM #side-story
WHERE parent = this.file.link
```

---

## Thoughts & Review
* **What I Liked**: 
* **What I Disliked**: 
* **Key Characters / Arcs**: 
* **Overall Impressions**: 
`;
_%>
