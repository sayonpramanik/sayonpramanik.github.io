# News, weekly packs and verified coverage

The site remains static HTML on GitHub Pages. Existing URLs, Field Notes, Essays,
metadata and original content are retained. No site-wide framework is required.

## Publish a weekly pack item

1. Read the completed pack in the task “Weekly content pack for Sayon Pramanik”
   (conversation `6a6af761-4458-83ed-b79d-8e7975f11945`). Record its delivery date.
2. Select substantive research reflections or verified academic updates. Do not
   copy hashtags, platform instructions, backlink tasks or uncompleted plans as news.
   Do not turn an outline into a claim that research has been completed.
3. Check `content/news.json` for duplicate topics and `source_pack` values. Add an
   entry with a stable lowercase hyphenated `slug`, actual website publication
   `date`, `title`, `category`, `summary`, `source_pack`, and `body` (arrays of
   `p` or `h2` plus plain text). Use `sources` and `related` arrays of URL/label
   pairs. On revision, retain the original date and set `modified`.
4. For external claims, verify the original source. Dates of events, source
   publication and website publication must remain distinct. Label reflections
   and work in progress accurately. Do not expose private research or editorial work.
5. Run `python3 scripts/build_updates.py` then `python3 scripts/check_site.py`.
   The builder refreshes news pages, their RSS feed, the homepage preview and both
   sitemaps. It preserves the existing Writing feed at `/feed.xml`.
6. Review the diff and rendered pages on mobile and desktop. Commit all source
   and generated changes together; publish to `main` without force-pushing.
   Check deployment and live URLs before reporting success.

## Coverage

Edit `content/media.json`. Each entry records its category, original publisher,
source date label, precise supported summary, source URL and verification date.
Use original newspaper reports or institutional sources. Keep newspaper coverage,
sporting achievements, academic use and institutional profiles distinct. An
article written by Sayon belongs in Publications, not third-party press coverage.
Do not infer endorsements from a syllabus citation. Do not invent publication
 dates from URL paths or search crawl dates. Exclude unverified namesakes.

## Templates

`templates/page.html` preserves the site's typography, colours, navigation and
footer for generated pages. Existing pages remain hand-maintained. If global
navigation changes, update those pages and the template together.
The footer discloses: “Maintained with assistance from AI agents.”

## Initial source verification — 24 September 2026

- The Tribune, 20 December 2022: directly names Sayon Pramanik of NIT Raipur as
  men's singles runner-up. Sporting coverage, not research coverage.
- Geography syllabus on the Shaheed Bhagat Singh College / University of Delhi
  domain: PDF page 18 lists the Sangani and Pramanik (2024) article in the Unit 4
  tutorial exercise for Geography of Behaviour and Emotions (DSE 15). No release
  date is inferred from the upload path.
- NIT Raipur newsletter search results were found, but full source retrieval
  failed; they were not added. No broad claim of exhaustive press coverage is made.
