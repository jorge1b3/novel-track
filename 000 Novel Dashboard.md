---
tags:
  - dashboard
---

# Novel Dashboard

```dataviewjs
const allNovels = dv.pages('#novel');
const completed = allNovels.where(p => p.status === "Completed");
const reading = allNovels.where(p => p.status === "Reading");
const onHold = allNovels.where(p => p.status === "On-Hold");
const planToRead = allNovels.where(p => p.status === "Plan-to-Read");

const totalChapters = allNovels.values.reduce((sum, p) => sum + (p["current-chapter"] || 0), 0);
const ratedCompleted = completed.where(p => p.rating);
const avgRating = ratedCompleted.length > 0 ? (ratedCompleted.values.reduce((sum, p) => sum + p.rating, 0) / ratedCompleted.length).toFixed(1) : "N/A";

const container = dv.container.createEl("div", { attr: { style: "display:flex;gap:12px;margin:15px 0 25px 0;flex-wrap:wrap;" } });

function createStatCard(label, val, color) {
  const card = container.createEl("div", { attr: { style: `flex:1;min-width:140px;background:var(--background-secondary);border:1px solid var(--background-modifier-border);border-radius:6px;padding:12px;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,0.1);` } });
  card.createEl("div", { text: label, attr: { style: "font-size:0.75em;color:var(--text-muted);font-weight:600;text-transform:uppercase;letter-spacing:0.5px;" } });
  card.createEl("div", { text: val, attr: { style: `font-size:1.7em;font-weight:700;color:${color || 'var(--text-normal)'};margin-top:6px;` } });
}

createStatCard("Total Read", `${totalChapters} ch`, "var(--interactive-accent)");
createStatCard("Reading", reading.length, "var(--text-accent)");
createStatCard("Completed", completed.length, "var(--color-green)");
createStatCard("Plan to Read", planToRead.length, "var(--text-muted)");
createStatCard("Avg Rating", avgRating + " ★", "var(--color-yellow)");
```

---

## Next Reads (Suggestions)

```dataviewjs
const planToRead = dv.pages('#novel')
  .where(p => p.status === "Plan-to-Read");

const suggestions = planToRead
  .sort(p => p.rating || 0, 'desc')
  .slice(0, 3);

if (suggestions.length > 0) {
  const sugDiv = dv.container.createEl("div", { attr: { style: "display:flex;gap:12px;flex-wrap:wrap;margin:10px 0 20px 0;" } });
  for (const s of suggestions) {
    const item = sugDiv.createEl("div", { attr: { style: "flex:1;min-width:200px;background:var(--background-secondary);border:1px solid var(--background-modifier-border);border-radius:6px;padding:12px;box-shadow:0 1px 3px rgba(0,0,0,0.05);" } });
    
    const titleLink = item.createEl("strong").createEl("a", { text: s.file.name, attr: { href: s.file.path, class: "internal-link" } });
    titleLink.style.color = "var(--text-accent)";
    titleLink.style.textDecoration = "none";
    
    if (s.author) {
      item.createEl("div", { text: `by ${s.author}`, attr: { style: "font-size:0.85em;color:var(--text-muted);margin-top:4px;" } });
    }
    
    const footer = item.createEl("div", { attr: { style: "display:flex;align-items:center;justify-content:space-between;margin-top:8px;" } });
    if (s.rating) {
      footer.createEl("span", { text: "★".repeat(s.rating) + "☆".repeat(5-s.rating), attr: { style: "color:var(--color-yellow);font-size:0.8em;" } });
    } else {
      footer.createEl("span", { text: "No rating", attr: { style: "color:var(--text-faint);font-size:0.8em;font-style:italic;" } });
    }
    
    const genre = s.file.tags.filter(t => t !== "#novel").map(t => t.replace("#", ""))[0];
    if (genre) {
      footer.createEl("span", { text: genre, attr: { style: "font-size:0.7em;background:rgba(255,255,255,0.05);padding:2px 6px;border-radius:4px;color:var(--text-muted);" } });
    }
  }
} else {
  dv.paragraph("_No novels in Plan to Read list._");
}
```

---


## Now Reading

```dataviewjs
const novels = dv.pages('#novel')
  .where(p => p.status === "Reading" && p["current-chapter"])
  .sort(p => p.file.name, 'asc');

const formatCh = (cc, tc, item) => `${cc}/${tc}` + (item["side-stories-total"] > 0 ? ` (+${item["side-stories-read"] || 0}/${item["side-stories-total"]} side)` : "");

function resolveCover(novelPath) {
  const slug = novelPath.split('/').pop().replace(/\.md$/, '');
  for (const ext of ['.jpg', '.png', '.jpeg', '.webp']) {
    const p = `covers/${slug}${ext}`;
    const f = app.vault.getAbstractFileByPath(p);
    if (f) return app.vault.getResourcePath(f);
  }
  return null;
}

for (const n of novels) {
  let currentCc = n["current-chapter"] || 0;
  let currentTc = n["total-chapters"] || 0;
  const pct = currentTc > 0 ? Math.round(currentCc / currentTc * 100) : 0;

  const card = dv.container.createEl("div", { attr: { class: "novel-card" } });
  const displayTitle = n.aliases && n.aliases.length > 0 ? n.aliases[0] : n.file.name;

  // Cover
  const src = resolveCover(n.file.path);
  if (src) {
    const img = card.createEl("img", { attr: { class: "novel-cover" } });
    img.src = src;
  } else {
    const initials = displayTitle
      .split(/[\s_—\-]+/)
      .map(w => w[0])
      .join('')
      .slice(0, 3)
      .toUpperCase();
    card.createEl("div", { text: initials, attr: { class: "novel-cover-fallback" } });
  }

  // Info
  const info = card.createEl("div", { attr: { style: "flex:1;min-width:0;" } });

  // Title row
  const titleRow = info.createEl("div", { attr: { style: "display:flex;align-items:center;gap:8px;flex-wrap:wrap;" } });
  titleRow.createEl("a", { text: displayTitle, attr: { href: n.file.path, class: "internal-link novel-title" } });

  if (currentCc >= currentTc && currentTc > 0) {
    titleRow.createEl("span", { text: "✓", attr: { style: "font-size:0.85em;color:var(--color-green);font-weight:700;" } });
  }

  if (n.rating) {
    const stars = Math.round(n.rating);
    titleRow.createEl("span", { text: "★".repeat(stars) + "☆".repeat(5 - stars), attr: { style: "font-size:0.8em;color:var(--text-accent);" } });
  }

  // Meta
  const meta = [];
  if (n.author) meta.push("✍ " + n.author);
  if (n.type) meta.push(n.type);
  meta.push(n.status);
  info.createEl("div", { text: meta.join(" · "), attr: { class: "novel-meta" } });

  // Progress bar
  const barRow = info.createEl("div", { attr: { class: "novel-bar-wrap" } });
  const chLabel = barRow.createEl("span", { text: formatCh(currentCc, currentTc, n), attr: { style: "font-size:0.8em;font-weight:600;white-space:nowrap;color:var(--text-muted);" } });
  const bar = barRow.createEl("div", { attr: { class: "novel-bar-out" } });
  const fill = bar.createEl("div", { attr: { style: `width:${pct}%;height:100%;background:var(--interactive-accent);border-radius:3px;` } });
  const pctLabel = barRow.createEl("span", { text: `${pct}%`, attr: { style: "font-size:0.75em;color:var(--text-faint);white-space:nowrap;" } });

  const updateBar = (newCc, newTc) => {
    currentCc = newCc;
    currentTc = newTc;
    const newPct = currentTc > 0 ? Math.round(currentCc / currentTc * 100) : 0;
    chLabel.textContent = formatCh(newCc, newTc, n);
    fill.style.width = `${newPct}%`;
    pctLabel.textContent = `${newPct}%`;
  };

  // Genres (tags)
  const tags = n.file.tags.filter(t => t !== "#novel").map(t => t.replace("#", ""));
  if (tags.length > 0) {
    const tagRow = info.createEl("div", { attr: { style: "margin-top:3px;" } });
    tags.forEach(t => tagRow.createEl("span", { text: t, attr: { class: "novel-tag" } }));
  }

  // Buttons
  const btnRow = info.createEl("div", { attr: { style: "margin-top:6px;display:flex;gap:4px;" } });
  const decBtn = btnRow.createEl("button", { text: "−", attr: { class: "novel-btn" } });
  decBtn.addEventListener("click", async () => {
    const file = app.vault.getAbstractFileByPath(n.file.path);
    const updatedCc = Math.max(0, currentCc - 1);
    await app.fileManager.processFrontMatter(file, fm => {
      fm["current-chapter"] = updatedCc;
    });
    updateBar(updatedCc, currentTc);
  });

  const incBtn = btnRow.createEl("button", { text: "+", attr: { class: "novel-btn" } });
  incBtn.addEventListener("click", async () => {
    const file = app.vault.getAbstractFileByPath(n.file.path);
    const updatedCc = currentCc + 1;
    let updatedTc = currentTc;
    if (currentCc >= currentTc) {
      updatedTc = currentTc + 1;
    }
    await app.fileManager.processFrontMatter(file, fm => {
      fm["current-chapter"] = updatedCc;
      if (currentCc >= (fm["total-chapters"] || 0)) {
        fm["total-chapters"] = updatedTc;
      }
    });
    updateBar(updatedCc, updatedTc);
  });

  if (n["source-url"]) {
    btnRow.createEl("a", { text: "🔗 Source", attr: { href: n["source-url"], style: "font-size:0.85em;margin-left:auto;color:var(--text-accent);text-decoration:none;" } });
  }
}
```

---

## On Hold

```dataviewjs
const novels = dv.pages('#novel')
  .where(p => p.status === "On-Hold")
  .sort(p => p.file.name, 'asc');

const formatCh = (cc, tc, item) => `${cc}/${tc}` + (item["side-stories-total"] > 0 ? ` (+${item["side-stories-read"] || 0}/${item["side-stories-total"]} side)` : "");

function resolveCover(novelPath) {
  const slug = novelPath.split('/').pop().replace(/\.md$/, '');
  for (const ext of ['.jpg', '.png', '.jpeg', '.webp']) {
    const p = `covers/${slug}${ext}`;
    const f = app.vault.getAbstractFileByPath(p);
    if (f) return app.vault.getResourcePath(f);
  }
  return null;
}

for (const n of novels) {
  let currentCc = n["current-chapter"] || 0;
  let currentTc = n["total-chapters"] || 0;
  const pct = currentTc > 0 ? Math.round(currentCc / currentTc * 100) : 0;

  const card = dv.container.createEl("div", { attr: { class: "novel-card" } });
  const displayTitle = n.aliases && n.aliases.length > 0 ? n.aliases[0] : n.file.name;

  const src = resolveCover(n.file.path);
  if (src) {
    const img = card.createEl("img", { attr: { class: "novel-cover" } });
    img.src = src;
  } else {
    const initials = displayTitle
      .split(/[\s_—\-]+/)
      .map(w => w[0])
      .join('')
      .slice(0, 3)
      .toUpperCase();
    card.createEl("div", { text: initials, attr: { class: "novel-cover-fallback" } });
  }

  const info = card.createEl("div", { attr: { style: "flex:1;min-width:0;" } });

  const titleRow = info.createEl("div", { attr: { style: "display:flex;align-items:center;gap:8px;flex-wrap:wrap;" } });
  titleRow.createEl("a", { text: displayTitle, attr: { href: n.file.path, class: "internal-link novel-title" } });

  if (currentCc >= currentTc && currentTc > 0) {
    titleRow.createEl("span", { text: "✓", attr: { style: "font-size:0.85em;color:var(--color-green);font-weight:700;" } });
  }

  if (n.rating) {
    const stars = Math.round(n.rating);
    titleRow.createEl("span", { text: "★".repeat(stars) + "☆".repeat(5 - stars), attr: { style: "font-size:0.8em;color:var(--text-accent);" } });
  }

  const meta = [];
  if (n.author) meta.push("✍ " + n.author);
  if (n.type) meta.push(n.type);
  meta.push(n.status);
  info.createEl("div", { text: meta.join(" · "), attr: { class: "novel-meta" } });

  const barRow = info.createEl("div", { attr: { class: "novel-bar-wrap" } });
  const chLabel = barRow.createEl("span", { text: formatCh(currentCc, currentTc, n), attr: { style: "font-size:0.8em;font-weight:600;white-space:nowrap;color:var(--text-muted);" } });
  const bar = barRow.createEl("div", { attr: { class: "novel-bar-out" } });
  const fill = bar.createEl("div", { attr: { style: `width:${pct}%;height:100%;background:var(--interactive-accent);border-radius:3px;` } });
  const pctLabel = barRow.createEl("span", { text: `${pct}%`, attr: { style: "font-size:0.75em;color:var(--text-faint);white-space:nowrap;" } });

  const updateBar = (newCc, newTc) => {
    currentCc = newCc;
    currentTc = newTc;
    const newPct = currentTc > 0 ? Math.round(currentCc / currentTc * 100) : 0;
    chLabel.textContent = formatCh(newCc, newTc, n);
    fill.style.width = `${newPct}%`;
    pctLabel.textContent = `${newPct}%`;
  };

  // Genres (tags)
  const tags = n.file.tags.filter(t => t !== "#novel").map(t => t.replace("#", ""));
  if (tags.length > 0) {
    const tagRow = info.createEl("div", { attr: { style: "margin-top:3px;" } });
    tags.forEach(t => tagRow.createEl("span", { text: t, attr: { class: "novel-tag" } }));
  }

  const btnRow = info.createEl("div", { attr: { style: "margin-top:6px;display:flex;gap:4px;" } });
  const decBtn = btnRow.createEl("button", { text: "−", attr: { class: "novel-btn" } });
  decBtn.addEventListener("click", async () => {
    const file = app.vault.getAbstractFileByPath(n.file.path);
    const updatedCc = Math.max(0, currentCc - 1);
    await app.fileManager.processFrontMatter(file, fm => {
      fm["current-chapter"] = updatedCc;
    });
    updateBar(updatedCc, currentTc);
  });

  const incBtn = btnRow.createEl("button", { text: "+", attr: { class: "novel-btn" } });
  incBtn.addEventListener("click", async () => {
    const file = app.vault.getAbstractFileByPath(n.file.path);
    const updatedCc = currentCc + 1;
    let updatedTc = currentTc;
    if (currentCc >= currentTc) {
      updatedTc = currentTc + 1;
    }
    await app.fileManager.processFrontMatter(file, fm => {
      fm["current-chapter"] = updatedCc;
      if (currentCc >= (fm["total-chapters"] || 0)) {
        fm["total-chapters"] = updatedTc;
      }
    });
    updateBar(updatedCc, updatedTc);
  });

  if (n["source-url"]) {
    btnRow.createEl("a", { text: "🔗 Source", attr: { href: n["source-url"], style: "font-size:0.85em;margin-left:auto;color:var(--text-accent);text-decoration:none;" } });
  }
}
```

---

## Plan to Read

```dataviewjs
const novels = dv.pages('#novel')
  .where(p => p.status === "Plan-to-Read")
  .sort(p => p.file.name, 'asc');

const formatCh = (cc, tc, item) => `${cc}/${tc}` + (item["side-stories-total"] > 0 ? ` (+${item["side-stories-read"] || 0}/${item["side-stories-total"]} side)` : "");

function resolveCover(novelPath) {
  const slug = novelPath.split('/').pop().replace(/\.md$/, '');
  for (const ext of ['.jpg', '.png', '.jpeg', '.webp']) {
    const p = `covers/${slug}${ext}`;
    const f = app.vault.getAbstractFileByPath(p);
    if (f) return app.vault.getResourcePath(f);
  }
  return null;
}

for (const n of novels) {
  const cc = n["current-chapter"] || 0;
  const tc = n["total-chapters"] || 0;
  const pct = tc > 0 ? Math.round(cc / tc * 100) : 0;

  const card = dv.container.createEl("div", { attr: { class: "novel-card" } });
  const displayTitle = n.aliases && n.aliases.length > 0 ? n.aliases[0] : n.file.name;

  const src = resolveCover(n.file.path);
  if (src) {
    const img = card.createEl("img", { attr: { class: "novel-cover" } });
    img.src = src;
  } else {
    const initials = displayTitle
      .split(/[\s_—\-]+/)
      .map(w => w[0])
      .join('')
      .slice(0, 3)
      .toUpperCase();
    card.createEl("div", { text: initials, attr: { class: "novel-cover-fallback" } });
  }

  const info = card.createEl("div", { attr: { style: "flex:1;min-width:0;" } });

  const titleRow = info.createEl("div", { attr: { style: "display:flex;align-items:center;gap:8px;flex-wrap:wrap;" } });
  titleRow.createEl("a", { text: displayTitle, attr: { href: n.file.path, class: "internal-link novel-title" } });

  if (cc >= tc && tc > 0) {
    titleRow.createEl("span", { text: "✓", attr: { style: "font-size:0.85em;color:var(--color-green);font-weight:700;" } });
  }

  if (n.rating) {
    const stars = Math.round(n.rating);
    titleRow.createEl("span", { text: "★".repeat(stars) + "☆".repeat(5 - stars), attr: { style: "font-size:0.8em;color:var(--text-accent);" } });
  }

  const meta = [];
  if (n.author) meta.push("✍ " + n.author);
  if (n.type) meta.push(n.type);
  meta.push(n.status);
  info.createEl("div", { text: meta.join(" · "), attr: { class: "novel-meta" } });

  const barRow = info.createEl("div", { attr: { class: "novel-bar-wrap" } });
  const chLabel = barRow.createEl("span", { text: formatCh(cc, tc, n), attr: { style: "font-size:0.8em;font-weight:600;white-space:nowrap;color:var(--text-muted);" } });
  const bar = barRow.createEl("div", { attr: { class: "novel-bar-out" } });
  const fill = bar.createEl("div", { attr: { style: `width:${pct}%;height:100%;background:var(--interactive-accent);border-radius:3px;` } });
  const pctLabel = barRow.createEl("span", { text: `${pct}%`, attr: { style: "font-size:0.75em;color:var(--text-faint);white-space:nowrap;" } });

  // Genres (tags)
  const tags = n.file.tags.filter(t => t !== "#novel").map(t => t.replace("#", ""));
  if (tags.length > 0) {
    const tagRow = info.createEl("div", { attr: { style: "margin-top:3px;" } });
    tags.forEach(t => tagRow.createEl("span", { text: t, attr: { class: "novel-tag" } }));
  }

  const btnRow = info.createEl("div", { attr: { style: "margin-top:6px;display:flex;gap:4px;" } });
  const startBtn = btnRow.createEl("button", { text: "▶ Start Reading", attr: { class: "novel-btn" } });
  startBtn.addEventListener("click", async () => {
    const file = app.vault.getAbstractFileByPath(n.file.path);
    await app.fileManager.processFrontMatter(file, fm => {
      fm["status"] = "Reading";
      if ((fm["current-chapter"] || 0) === 0) {
        fm["current-chapter"] = 1;
      }
    });
    startBtn.textContent = "📖 Reading...";
    startBtn.style.color = "var(--color-green)";
  });

  if (n["source-url"]) {
    btnRow.createEl("a", { text: "🔗 Source", attr: { href: n["source-url"], style: "font-size:0.85em;margin-left:auto;color:var(--text-accent);text-decoration:none;" } });
  }
}
```

---

## Completed

```dataviewjs
const novels = dv.pages('#novel')
  .where(p => p.status === "Completed")
  .sort(p => p.file.name, 'asc');

const formatCh = (cc, tc, item) => `${cc}/${tc}` + (item["side-stories-total"] > 0 ? ` (+${item["side-stories-read"] || 0}/${item["side-stories-total"]} side)` : "");

function resolveCover(novelPath) {
  const slug = novelPath.split('/').pop().replace(/\.md$/, '');
  for (const ext of ['.jpg', '.png', '.jpeg', '.webp']) {
    const p = `covers/${slug}${ext}`;
    const f = app.vault.getAbstractFileByPath(p);
    if (f) return app.vault.getResourcePath(f);
  }
  return null;
}

for (const n of novels) {
  const cc = n["current-chapter"] || 0;
  const tc = n["total-chapters"] || 0;
  const pct = tc > 0 ? Math.round(cc / tc * 100) : 100;

  const card = dv.container.createEl("div", { attr: { class: "novel-card" } });
  const displayTitle = n.aliases && n.aliases.length > 0 ? n.aliases[0] : n.file.name;

  const src = resolveCover(n.file.path);
  if (src) {
    const img = card.createEl("img", { attr: { class: "novel-cover" } });
    img.src = src;
  } else {
    const initials = displayTitle
      .split(/[\s_—\-]+/)
      .map(w => w[0])
      .join('')
      .slice(0, 3)
      .toUpperCase();
    card.createEl("div", { text: initials, attr: { class: "novel-cover-fallback" } });
  }

  const info = card.createEl("div", { attr: { style: "flex:1;min-width:0;" } });

  const titleRow = info.createEl("div", { attr: { style: "display:flex;align-items:center;gap:8px;flex-wrap:wrap;" } });
  titleRow.createEl("a", { text: displayTitle, attr: { href: n.file.path, class: "internal-link novel-title" } });

  titleRow.createEl("span", { text: "✓", attr: { style: "font-size:0.85em;color:var(--color-green);font-weight:700;" } });

  if (n.rating) {
    const stars = Math.round(n.rating);
    titleRow.createEl("span", { text: "★".repeat(stars) + "☆".repeat(5 - stars), attr: { style: "font-size:0.8em;color:var(--text-accent);" } });
  }

  const meta = [];
  if (n.author) meta.push("✍ " + n.author);
  if (n.type) meta.push(n.type);
  meta.push(n.status);
  info.createEl("div", { text: meta.join(" · "), attr: { class: "novel-meta" } });

  const barRow = info.createEl("div", { attr: { class: "novel-bar-wrap" } });
  const chLabel = barRow.createEl("span", { text: formatCh(cc, tc, n), attr: { style: "font-size:0.8em;font-weight:600;white-space:nowrap;color:var(--text-muted);" } });
  const bar = barRow.createEl("div", { attr: { class: "novel-bar-out" } });
  const fill = bar.createEl("div", { attr: { style: `width:${pct}%;height:100%;background:var(--color-green);border-radius:3px;` } });
  const pctLabel = barRow.createEl("span", { text: `${pct}%`, attr: { style: "font-size:0.75em;color:var(--text-faint);white-space:nowrap;" } });

  // Genres (tags)
  const tags = n.file.tags.filter(t => t !== "#novel").map(t => t.replace("#", ""));
  if (tags.length > 0) {
    const tagRow = info.createEl("div", { attr: { style: "margin-top:3px;" } });
    tags.forEach(t => tagRow.createEl("span", { text: t, attr: { class: "novel-tag" } }));
  }

  if (n["source-url"]) {
    const btnRow = info.createEl("div", { attr: { style: "margin-top:6px;display:flex;" } });
    btnRow.createEl("a", { text: "🔗 Source", attr: { href: n["source-url"], style: "font-size:0.85em;margin-left:auto;color:var(--text-accent);text-decoration:none;" } });
  }
}
```

---

## Dropped

```dataviewjs
const novels = dv.pages('#novel')
  .where(p => p.status === "Dropped")
  .sort(p => p.file.name, 'asc');

const formatCh = (cc, tc, item) => `${cc}/${tc}` + (item["side-stories-total"] > 0 ? ` (+${item["side-stories-read"] || 0}/${item["side-stories-total"]} side)` : "");

function resolveCover(novelPath) {
  const slug = novelPath.split('/').pop().replace(/\.md$/, '');
  for (const ext of ['.jpg', '.png', '.jpeg', '.webp']) {
    const p = `covers/${slug}${ext}`;
    const f = app.vault.getAbstractFileByPath(p);
    if (f) return app.vault.getResourcePath(f);
  }
  return null;
}

for (const n of novels) {
  const cc = n["current-chapter"] || 0;
  const tc = n["total-chapters"] || 0;
  const pct = tc > 0 ? Math.round(cc / tc * 100) : 0;

  const card = dv.container.createEl("div", { attr: { class: "novel-card" } });
  const displayTitle = n.aliases && n.aliases.length > 0 ? n.aliases[0] : n.file.name;

  const src = resolveCover(n.file.path);
  if (src) {
    const img = card.createEl("img", { attr: { class: "novel-cover" } });
    img.src = src;
  } else {
    const initials = displayTitle
      .split(/[\s_—\-]+/)
      .map(w => w[0])
      .join('')
      .slice(0, 3)
      .toUpperCase();
    card.createEl("div", { text: initials, attr: { class: "novel-cover-fallback" } });
  }

  const info = card.createEl("div", { attr: { style: "flex:1;min-width:0;" } });

  const titleRow = info.createEl("div", { attr: { style: "display:flex;align-items:center;gap:8px;flex-wrap:wrap;" } });
  titleRow.createEl("a", { text: displayTitle, attr: { href: n.file.path, class: "internal-link novel-title" } });

  if (cc >= tc && tc > 0) {
    titleRow.createEl("span", { text: "✓", attr: { style: "font-size:0.85em;color:var(--color-green);font-weight:700;" } });
  }

  if (n.rating) {
    const stars = Math.round(n.rating);
    titleRow.createEl("span", { text: "★".repeat(stars) + "☆".repeat(5 - stars), attr: { style: "font-size:0.8em;color:var(--text-accent);" } });
  }

  const meta = [];
  if (n.author) meta.push("✍ " + n.author);
  if (n.type) meta.push(n.type);
  meta.push(n.status);
  info.createEl("div", { text: meta.join(" · "), attr: { class: "novel-meta" } });

  const barRow = info.createEl("div", { attr: { class: "novel-bar-wrap" } });
  const chLabel = barRow.createEl("span", { text: formatCh(cc, tc, n), attr: { style: "font-size:0.8em;font-weight:600;white-space:nowrap;color:var(--text-muted);" } });
  const bar = barRow.createEl("div", { attr: { class: "novel-bar-out" } });
  const fill = bar.createEl("div", { attr: { style: `width:${pct}%;height:100%;background:var(--interactive-accent);border-radius:3px;` } });
  const pctLabel = barRow.createEl("span", { text: `${pct}%`, attr: { style: "font-size:0.75em;color:var(--text-faint);white-space:nowrap;" } });

  // Genres (tags)
  const tags = n.file.tags.filter(t => t !== "#novel").map(t => t.replace("#", ""));
  if (tags.length > 0) {
    const tagRow = info.createEl("div", { attr: { style: "margin-top:3px;" } });
    tags.forEach(t => tagRow.createEl("span", { text: t, attr: { class: "novel-tag" } }));
  }

  const btnRow = info.createEl("div", { attr: { style: "margin-top:6px;display:flex;gap:4px;" } });
  const resumeBtn = btnRow.createEl("button", { text: "↺ Resume Reading", attr: { class: "novel-btn" } });
  resumeBtn.addEventListener("click", async () => {
    const file = app.vault.getAbstractFileByPath(n.file.path);
    await app.fileManager.processFrontMatter(file, fm => {
      fm["status"] = "Reading";
    });
    resumeBtn.textContent = "📖 Reading...";
    resumeBtn.style.color = "var(--color-green)";
  });

  if (n["source-url"]) {
    btnRow.createEl("a", { text: "🔗 Source", attr: { href: n["source-url"], style: "font-size:0.85em;margin-left:auto;color:var(--text-accent);text-decoration:none;" } });
  }
}
```

---

## All Novels

```dataview
TABLE status AS "Status", current-chapter AS "Ch.", total-chapters AS "Total", choice(total-chapters > 0, round((current-chapter / total-chapters) * 100), 0) AS "%"
FROM #novel
SORT status ASC, file.name ASC
```
