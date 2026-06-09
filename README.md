# LaserStorm Force Builder

A single-page army-list builder for the tabletop wargame **LaserStorm (2nd Edition)**.
Design your own units, assemble them into task forces and armies, and print
game-ready reference sheets - all in one file, in your browser, online or off.

![A task force in the builder](docs/images/taskforce.png)

## What it is

The whole app is a single HTML file. There's no sign-up, no server, and nothing
to install - everything you create is saved right in your browser. Work through
five connected layers:

> **Units** → **Task Forces** → **Armies** → **Expeditionary Forces** → **Print**

Build custom units, group them into rules-aware task forces, field those as
armies organized into battle groups, optionally bundle armies into larger
expeditionary forces, then print clean reference sheets for the table.

## Features

- **Unit builder** with live points costing - stats, stand traits, and multiple
  weapons, with the cost for every deployment type (Unit, Independent,
  Commander, Hero) calculated as you go.
- **Factions** - group your units under custom factions with their own colors,
  icons, and faction traits, alongside the five built-in factions.
- **Unit library** - browse, search, filter, and clone every built-in and
  custom unit.
- **Task forces** - fill role slots (core / specialist / command / support),
  assign a commander and a tactical asset, and mechanize infantry with transports.
- **Armies & battle groups** - task-force armies or free-pick armies, organized
  into named battle groups with symbols.
- **Expeditionary forces** - collect several armies into army groups for a
  campaign.
- **Printing** - color or grayscale, Letter or A4, with auto-pagination.
- **Sharing & backups** - export anything from a single army to your whole
  collection as JSON, and import what others share with you.
- **Works fully offline** and from `file://` - fonts and icons are built in.
- **Undo** (Ctrl/Cmd+Z) and a backup reminder so you don't lose your work.

## Getting started

1. **Open the app.** Double-click `army-builder.html`, or serve the folder (see
   below) and open it in any modern browser.
2. **Build a unit** in the *Unit Builder*, then **Save to Library**.
3. **Create a Task Force** and add your units to its role slots.
4. **Create an Army**, drop the task force into its pool, and sort the units
   into **Battle Groups**.
5. **Print** a reference sheet - and **export a backup** to keep your work safe.

There's a full step-by-step walkthrough, with screenshots, in the
**[User Guide → Quick start](docs/USER_GUIDE.md#2-quick-start-build-your-first-army)**.

## Running it

The app is one static file with no build step.

- **Simplest:** open `army-builder.html` directly in your browser.
- **Served locally** (recommended if anything looks blocked by the browser):

  ```bash
  python3 -m http.server 3000
  # then open http://localhost:3000/army-builder.html
  ```

## Works offline

Once the page has loaded once, it needs no network at all - the fonts and icons
are embedded in the file. On a phone or tablet you can use **"Add to Home
Screen"** to keep it one tap away at the table.

## Your data lives in your browser

Everything you create is stored in your browser's local storage on **this device,
in this browser** - it isn't synced to any account or cloud. Clearing your
browser data, or switching to another browser or device, won't carry it over.

**Export a backup regularly** from the **Data** tab (*Full Backup*). The app will
also nudge you once you've built up some work. See
[User Guide → Backing up your data](docs/USER_GUIDE.md#11-backing-up-your-data).

## Documentation

📖 **[Full User Guide](docs/USER_GUIDE.md)** - concepts, a quick-start
walkthrough, and a reference for every page and feature.

## You'll need the game

This is a *list builder*, not the rulebook. To actually play you'll need the
**LaserStorm (2nd Edition)** rules - available from
[WargameVault](https://www.wargamevault.com/product/476399/laserstorm-2nd-edition?affiliate_id=564654).

## License

See [LICENSE](LICENSE).
