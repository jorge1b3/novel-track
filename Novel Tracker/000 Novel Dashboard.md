---
tags:
  - dashboard
---

# Novel Dashboard

---


## Now Reading

```dataviewjs
const novels = dv.pages('#novel')
  .where(p => p.status === "Reading" && p["current-chapter"])
  .sort(p => p.file.name, 'asc');

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
  const chLabel = barRow.createEl("span", { text: `${currentCc}/${currentTc}`, attr: { style: "font-size:0.8em;font-weight:600;white-space:nowrap;color:var(--text-muted);" } });
  const bar = barRow.createEl("div", { attr: { class: "novel-bar-out" } });
  const fill = bar.createEl("div", { attr: { style: `width:${pct}%;height:100%;background:var(--interactive-accent);border-radius:3px;` } });
  const pctLabel = barRow.createEl("span", { text: `${pct}%`, attr: { style: "font-size:0.75em;color:var(--text-faint);white-space:nowrap;" } });

  const updateBar = (newCc, newTc) => {
    currentCc = newCc;
    currentTc = newTc;
    const newPct = currentTc > 0 ? Math.round(currentCc / currentTc * 100) : 0;
    chLabel.textContent = `${currentCc}/${currentTc}`;
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
  const chLabel = barRow.createEl("span", { text: `${currentCc}/${currentTc}`, attr: { style: "font-size:0.8em;font-weight:600;white-space:nowrap;color:var(--text-muted);" } });
  const bar = barRow.createEl("div", { attr: { class: "novel-bar-out" } });
  const fill = bar.createEl("div", { attr: { style: `width:${pct}%;height:100%;background:var(--interactive-accent);border-radius:3px;` } });
  const pctLabel = barRow.createEl("span", { text: `${pct}%`, attr: { style: "font-size:0.75em;color:var(--text-faint);white-space:nowrap;" } });

  const updateBar = (newCc, newTc) => {
    currentCc = newCc;
    currentTc = newTc;
    const newPct = currentTc > 0 ? Math.round(currentCc / currentTc * 100) : 0;
    chLabel.textContent = `${currentCc}/${currentTc}`;
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
  const chLabel = barRow.createEl("span", { text: `${cc}/${tc}`, attr: { style: "font-size:0.8em;font-weight:600;white-space:nowrap;color:var(--text-muted);" } });
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
  const chLabel = barRow.createEl("span", { text: `${cc}/${tc}`, attr: { style: "font-size:0.8em;font-weight:600;white-space:nowrap;color:var(--text-muted);" } });
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
  const chLabel = barRow.createEl("span", { text: `${cc}/${tc}`, attr: { style: "font-size:0.8em;font-weight:600;white-space:nowrap;color:var(--text-muted);" } });
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
