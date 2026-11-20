# Asset register

Every image, font, icon and illustration committed to this repository is listed here, with its source and terms. A file is recorded here before it is committed (AGENTS.md, "Media is registered first"). `make check` fails when a media file under `docs/` is missing from this table (`tools/check_boards.py`).

Each row names the file by its path from the repository root. "Date checked" is the day the source and its terms were read.

## Fonts

Source Serif 4 (version 4.005) and Source Sans 3 (version 3.052) are served from this repository, not from Google's servers (design brief, "How the fonts are served"). The files are the variable WOFF2 builds from the official Adobe releases, one upright and one italic file for each family. Both families use the SIL Open Font License 1.1: free to use, including for commercial work, and free to embed and share when the licence text goes with them. The font names may not be sold on their own.

| File | What it is | Source | Author or owner | Licence and terms | Date checked |
|---|---|---|---|---|---|
| `docs/design/boards/fonts/SourceSerif4Variable-Roman.woff2` | Source Serif 4, upright, variable weight | [source-serif 4.005R](https://github.com/adobe-fonts/source-serif/releases/tag/4.005R) | Adobe | [SIL OFL 1.1](https://openfontlicense.org/open-font-license-official-text/) | 20 Nov 2026 |
| `docs/design/boards/fonts/SourceSerif4Variable-Italic.woff2` | Source Serif 4, italic, variable weight | [source-serif 4.005R](https://github.com/adobe-fonts/source-serif/releases/tag/4.005R) | Adobe | [SIL OFL 1.1](https://openfontlicense.org/open-font-license-official-text/) | 20 Nov 2026 |
| `docs/design/boards/fonts/SourceSans3VF-Upright.woff2` | Source Sans 3, upright, variable weight | [source-sans 3.052R](https://github.com/adobe-fonts/source-sans/releases/tag/3.052R) | Adobe | [SIL OFL 1.1](https://openfontlicense.org/open-font-license-official-text/) | 20 Nov 2026 |
| `docs/design/boards/fonts/SourceSans3VF-Italic.woff2` | Source Sans 3, italic, variable weight | [source-sans 3.052R](https://github.com/adobe-fonts/source-sans/releases/tag/3.052R) | Adobe | [SIL OFL 1.1](https://openfontlicense.org/open-font-license-official-text/) | 20 Nov 2026 |
| `docs/design/boards/fonts/OFL-SourceSerif4.txt` | Licence text for Source Serif 4 | [source-serif 4.005R](https://github.com/adobe-fonts/source-serif/releases/tag/4.005R) | Adobe | [SIL OFL 1.1](https://openfontlicense.org/open-font-license-official-text/) | 20 Nov 2026 |
| `docs/design/boards/fonts/OFL-SourceSans3.txt` | Licence text for Source Sans 3 | [source-sans 3.052R](https://github.com/adobe-fonts/source-sans/releases/tag/3.052R) | Adobe | [SIL OFL 1.1](https://openfontlicense.org/open-font-license-official-text/) | 20 Nov 2026 |

## Icons

The icons are from Lucide, release [1.77.0](https://github.com/lucide-icons/lucide/releases/tag/1.77.0), copied from its `icons/` folder. Lucide is under the ISC licence. The icons that come from the Feather project are under the MIT licence. Both allow commercial use when the notice is kept, and `docs/design/boards/icons/LICENSE-lucide.txt` keeps both notices ([licence](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE)). The files use `currentColor`, so they take the colour of the text around them.

Three names changed in this release, so the closest current icon is used: `shield-alert` is now `shield-exclamation-point`, `waves` is now `waves-horizontal`, and `circle-help` is now `circle-question-mark`.

| File | What it is | Source | Author or owner | Licence and terms | Date checked |
|---|---|---|---|---|---|
| `docs/design/boards/icons/bed.svg` | Icon: bed | [Lucide 1.77.0](https://lucide.dev/icons/bed) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/book-open.svg` | Icon: book-open | [Lucide 1.77.0](https://lucide.dev/icons/book-open) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/calendar-days.svg` | Icon: calendar-days | [Lucide 1.77.0](https://lucide.dev/icons/calendar-days) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/check.svg` | Icon: check | [Lucide 1.77.0](https://lucide.dev/icons/check) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/chevron-down.svg` | Icon: chevron-down | [Lucide 1.77.0](https://lucide.dev/icons/chevron-down) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/chevron-right.svg` | Icon: chevron-right | [Lucide 1.77.0](https://lucide.dev/icons/chevron-right) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/circle-question-mark.svg` | Icon: circle-question-mark | [Lucide 1.77.0](https://lucide.dev/icons/circle-question-mark) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/clock.svg` | Icon: clock | [Lucide 1.77.0](https://lucide.dev/icons/clock) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/cloud-sun.svg` | Icon: cloud-sun | [Lucide 1.77.0](https://lucide.dev/icons/cloud-sun) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/coins.svg` | Icon: coins | [Lucide 1.77.0](https://lucide.dev/icons/coins) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/external-link.svg` | Icon: external-link | [Lucide 1.77.0](https://lucide.dev/icons/external-link) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/globe.svg` | Icon: globe | [Lucide 1.77.0](https://lucide.dev/icons/globe) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/hotel.svg` | Icon: hotel | [Lucide 1.77.0](https://lucide.dev/icons/hotel) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/info.svg` | Icon: info | [Lucide 1.77.0](https://lucide.dev/icons/info) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/link.svg` | Icon: link | [Lucide 1.77.0](https://lucide.dev/icons/link) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/map-pin.svg` | Icon: map-pin | [Lucide 1.77.0](https://lucide.dev/icons/map-pin) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/map.svg` | Icon: map | [Lucide 1.77.0](https://lucide.dev/icons/map) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/message-circle.svg` | Icon: message-circle | [Lucide 1.77.0](https://lucide.dev/icons/message-circle) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/moon.svg` | Icon: moon | [Lucide 1.77.0](https://lucide.dev/icons/moon) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/party-popper.svg` | Icon: party-popper | [Lucide 1.77.0](https://lucide.dev/icons/party-popper) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/pencil.svg` | Icon: pencil | [Lucide 1.77.0](https://lucide.dev/icons/pencil) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/plane.svg` | Icon: plane | [Lucide 1.77.0](https://lucide.dev/icons/plane) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/plus.svg` | Icon: plus | [Lucide 1.77.0](https://lucide.dev/icons/plus) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/refresh-cw.svg` | Icon: refresh-cw | [Lucide 1.77.0](https://lucide.dev/icons/refresh-cw) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/search.svg` | Icon: search | [Lucide 1.77.0](https://lucide.dev/icons/search) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/send.svg` | Icon: send | [Lucide 1.77.0](https://lucide.dev/icons/send) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/share-2.svg` | Icon: share-2 | [Lucide 1.77.0](https://lucide.dev/icons/share-2) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/shield-exclamation-point.svg` | Icon: shield-exclamation-point | [Lucide 1.77.0](https://lucide.dev/icons/shield-exclamation-point) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/sparkles.svg` | Icon: sparkles | [Lucide 1.77.0](https://lucide.dev/icons/sparkles) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/square.svg` | Icon: square | [Lucide 1.77.0](https://lucide.dev/icons/square) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/sun.svg` | Icon: sun | [Lucide 1.77.0](https://lucide.dev/icons/sun) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/sunrise.svg` | Icon: sunrise | [Lucide 1.77.0](https://lucide.dev/icons/sunrise) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/sunset.svg` | Icon: sunset | [Lucide 1.77.0](https://lucide.dev/icons/sunset) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/thermometer.svg` | Icon: thermometer | [Lucide 1.77.0](https://lucide.dev/icons/thermometer) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/ticket.svg` | Icon: ticket | [Lucide 1.77.0](https://lucide.dev/icons/ticket) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/train-front.svg` | Icon: train-front | [Lucide 1.77.0](https://lucide.dev/icons/train-front) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/wallet.svg` | Icon: wallet | [Lucide 1.77.0](https://lucide.dev/icons/wallet) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/waves-horizontal.svg` | Icon: waves-horizontal | [Lucide 1.77.0](https://lucide.dev/icons/waves-horizontal) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/wifi-off.svg` | Icon: wifi-off | [Lucide 1.77.0](https://lucide.dev/icons/wifi-off) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/x.svg` | Icon: x | [Lucide 1.77.0](https://lucide.dev/icons/x) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |
| `docs/design/boards/icons/LICENSE-lucide.txt` | Lucide licence text (ISC and MIT notices) | [LICENSE](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | Lucide Icons and Contributors | [ISC, MIT](https://github.com/lucide-icons/lucide/blob/1.77.0/LICENSE) | 20 Nov 2026 |

## Photos

Place photos are from Unsplash. The [Unsplash Licence](https://unsplash.com/license) was read on 20 Nov 2026. It says that "all images can be downloaded and used for free", for "commercial and non-commercial purposes", with "no permission needed". It does not allow images to be "sold without significant modification", or compiled "to replicate a similar or competing service". Credit is not required, but photographers appreciate it. The licence page shows no "last updated" date. Layover credits the photographer on the photo (design brief, "Aesthetic direction"). Each photo was downloaded from its Unsplash page, then resized to 1600 px on the long edge as JPEG, and is under 1 MB. Each photo shows the place it names.

| File | What it is | Source | Author or owner | Licence and terms | Date checked |
|---|---|---|---|---|---|
| `docs/design/boards/photos/lisbon.jpg` | Lisbon: red roofs of Alfama and the river Tagus, daylight, landscape | [Photo page](https://unsplash.com/photos/brown-and-white-concrete-houses-near-sea-during-daytime-qmaJ1JUL8G8) | [João Reguengos](https://unsplash.com/@yey_eye) | [Unsplash Licence](https://unsplash.com/license) | 20 Nov 2026 |
| `docs/design/boards/photos/valencia.jpg` | Valencia: the Palau de les Arts in the City of Arts and Sciences, daylight, portrait | [Photo page](https://unsplash.com/photos/city-of-arts-and-sciences-in-valencia-spain-under-blue-and-white-sky-jKywkUgB4X4) | [Diego Olguin](https://unsplash.com/@dieshock) | [Unsplash Licence](https://unsplash.com/license) | 20 Nov 2026 |
| `docs/design/boards/photos/valletta.jpg` | Valletta: the city wall, the Carmelite church dome and the harbour water, daylight, portrait | [Photo page](https://unsplash.com/photos/city-skyline-with-domed-building-across-blue-water-ai80NecqayM) | [Daniel Höhe](https://unsplash.com/@beyondxphotography) | [Unsplash Licence](https://unsplash.com/license) | 20 Nov 2026 |
