# Mood-scene prompts

Prompts for the owner to run in ChatGPT, for the welcome screen and the "How Layover works" page only. **The owner makes the images. The agent does not generate or commit any image.** Each image is registered in `docs/assets/README.md` (source: ChatGPT with the prompt used, date, terms) before it is committed. `make check` fails on an image that is not registered.

Written to the image rules in the [design brief](../brief.md#images) (owner: "AI for mood scenes only", 20 Nov 2026).

## Rules for every image

- Never a named or recognisable place. No landmark, no skyline that a person could name.
- No readable signs, no brand logos, no faces. People, if any, are seen from behind or far away, with no features.
- Never on a place card or next to a result, so no picture suggests a real place.
- Warm, calm, editorial travel mood, like a magazine photo: soft daylight, space around the subject, little clutter.
- Colour: keep it in the Harbour blues, with warm neutrals. Sea and sky in soft blue, deep navy as the darkest tone, warm white and sand for light. Avoid strong orange, red, green or purple. A small warm touch (a straw hat, a cream towel) is fine.
- Ask for landscape, about 16 by 10, with quiet space on one side where text can sit. Download at 1600 px wide or more, then resize to under 1 MB.

## Prompt 1: the welcome screen (a suitcase by a window)

> A calm editorial travel photograph: a navy hard-shell suitcase standing beside a tall window in a bright, quiet room, with a folded cream linen shirt and a straw hat on a wooden bench next to it. Soft morning light comes through the window; the view outside is only soft blue sky and blurred sea, with no buildings or landmarks. Warm white walls, pale wood, deep navy and soft sky blue as the main colours. Shallow depth of field, gentle shadows, a lot of empty wall space on the right. No people, no text, no signs, no logos, no labels on the suitcase. Landscape, 16:10, natural film look.

## Prompt 2: "How Layover works" (a table of planning)

> A calm editorial travel photograph, shot from above: a pale wooden table with an open paper notebook with no readable writing, a plain navy pen, a small paper map that is blurred and shows no real place, a cup of tea and a pair of sunglasses, in soft window light. Warm white and sand tones with deep navy and soft sky-blue accents. Plenty of empty table on the left. No people, no readable text, no logos, no brand names. Landscape, 16:10, natural film look.

## Prompt 3 (spare): a quiet shore

> A calm editorial travel photograph of an empty sandy shore at the start of the day, seen from low down: smooth pale sand, a few small waves, a folded blue-and-white striped towel and a pair of sandals in the foreground. The sea and sky are soft blue and the light is warm and low. No buildings, no headlands, no boats, no people, no text, no logos. Nothing that shows where in the world it is. Large empty sky on the upper left. Landscape, 16:10, natural film look.

## After the images exist

- **Alt text** starts with "Illustrative photo:" and then says what the picture shows, in plain words. For example: "Illustrative photo: a navy suitcase beside a sunny window." The picture is decoration, so the text next to it carries all the meaning.
- **Footer line**, on every page that shows a mood scene: "Some photos on this site are AI-generated illustrations". It is not added until the first image is on a page.
- **Register** each image in `docs/assets/README.md` first: file, the prompt used, ChatGPT as the source, the date, and the terms. The brief says OpenAI's sharing and publication policy is read again by hand before Layover goes public.
- **Check** each image before use: no readable letters, no face, no logo, no place that a person could name. If ChatGPT adds any of these, run the prompt again or crop it out.
