# Obsidian Web Novel Tracker

A premium, highly interactive Obsidian vault configuration designed to track your web novel reading progress, log side stories, display automated statistics, and organize your library with customized aesthetics.

---

## 📂 Vault Structure

* **`000 Novel Dashboard.md`**: The central homepage located at the root of the vault. It displays reading stats, recommended next reads, status-based novel card lists, and quick-increment action buttons.
* **`Novels/`**: The folder containing all your individual novel markdown notes.
* **`covers/`**: Stores downloaded cover images, automatically optimized and converted to `.webp` format.
* **`Novel Tracker/`**:
  * **`Templates/`**:
    * `Novel Template.md`: The creation workflow for main novels. Features automatic NovelUpdates scraping and manual fallbacks.
    * `Side Story Template.md`: The creation workflow for large spin-offs and sequels, linking them directly to their parent novels.
  * **`fetch_metadata_api.py`**: Scrapes NovelUpdates for description, author, genres, and cover url when triggered by Templater.
  * **`download_cover.py`**: Downloads and converts manual cover URLs into the `.webp` asset folder.
  * **`import-nu.py` / `main.py`**: Python utilities to import/convert NovelUpdates JSON exported reading lists into notes.

---

## ✨ Features

### 📊 Real-Time Analytics & Recommendations
* **Dynamic Stats Panel**: Flexbox grid on the dashboard showing Total Chapters Read, Active Reading count, Completed count, Plan-to-Read count, and Average Rating (Completed only).
* **Next Reads Suggester**: An algorithm card grid suggesting high-priority novels to read next from your `Plan-to-Read` list.

### 🤖 Automatic Metadata Extraction
* When creating a new novel, pasting a NovelUpdates link automatically fetches:
  * **Author name** & **short description** (skips prompts).
  * **Genre tags** (automatically converted into native tag boxes).
  * **Cover image** (automatically downloaded, converted to WebP, and formatted).
* Leaves manual inputs as a seamless fallback if no URL is provided.

### 📚 Side Story Tracking
* **Short Side Stories (Option B)**: Embedded directly inside the main novel's metadata table. Displayed on the dashboard cards next to main progress (e.g. `150/150 (+1/2 side)`).
* **Large Side Stories (Option C)**: Created as separate notes using the `Side Story Template.md`. Tagged as `#side-story` to prevent main dashboard clutter, and automatically queried and listed inside a Dataview table at the bottom of the parent novel's note.

### 🎨 Custom CSS Aesthetic
* Custom styling in `.obsidian/snippets/novel-page.css` makes tags render as beautiful colored pills/chips matching the dark theme of the vault.
* Auto-hides Dataview separating commas inside metadata tables for a clean grid layout.

---

## ⚙️ Requirements & Installation

1. **Obsidian Plugins**:
   * **Templater** (Enable "User System Commands" and configure templates).
   * **Dataview** (Enable JavaScript queries).
   * **Meta Bind** (Used for inline selects, rating stars, and chapter increment buttons).
2. **System Dependencies**:
   * **Python 3** (Used for API scraping and download scripts).
   * **ImageMagick** (Requires the `convert` CLI utility to be installed globally on your path to handle WebP conversions).

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
