// ============================================================
// NU Reading List → JSON Exporter
// ============================================================
// 1. Log in to novelupdates.com
// 2. Go to your reading list: https://www.novelupdates.com/reading-list/
// 3. Make sure you're on the list tab you want (Reading, Finish, etc.)
// 4. Open browser console (F12 → Console)
// 5. Paste this entire script and press Enter
// 6. A JSON file will download automatically
// ============================================================

const novels = [];

document.querySelectorAll('tr.rl_links').forEach(row => {
  const title = row.getAttribute('data-title') || '';
  const rating = row.getAttribute('data-rate') || '';
  const genreIds = (row.getAttribute('data-genreid') || '').replace(/,/g, ' ').trim();

  // Series URL from the title link in column 2
  const titleLink = row.querySelector('td.title_shorten a, td:nth-child(2) a');
  const url = titleLink ? titleLink.href : '';

  // My chapter
  const myChEl = row.querySelector('a.chp-release:not(.latest)');
  const myChapter = myChEl ? myChEl.textContent.trim() : '';

  // Latest chapter
  const latestEl = row.querySelector('a.chp-release.latest');
  const latestChapter = latestEl ? latestEl.textContent.trim() : '';

  novels.push({ title, url, myChapter, latestChapter, rating, genreIds });
});

console.log(`Found ${novels.length} novels`);

if (novels.length > 0) {
  const blob = new Blob([JSON.stringify(novels, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'nu-reading-list.json';
  a.click();
  console.log('Downloaded nu-reading-list.json');
} else {
  console.warn('No novels found. Make sure you are on the reading list page and logged in.');
}
