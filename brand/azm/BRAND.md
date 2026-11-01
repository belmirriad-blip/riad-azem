# Azm (عزم) brand

**عزم: resolve you act on.** Azm teaches Algerian Bac students (mainly 3AS Sciences expérimentales) how to study: a plan, past exam exercises, a daily log, and follow-up. It is not tutoring.

- **Core idea:** students fail the Bac not because it's hard, but because nobody taught them how to study.
- **Founder:** Riad, a medical student who went from 10 to 16 on the Bac in about three months by studying this way.
- **Audience:** students aged 16 to 19 (many under 10/20), and the parents who pay and worry.

## Voice
Calm, serious, honest, practical. A steady older brother who did it, not a motivational coach.
- Concrete actions with numbers. Never promise grades. No hype, no emoji spam, no fake urgency.
- Simple Modern Standard Arabic in the app, Darija on social, French for terms students already use.
- Address each student in the form that matches their gender.

| Write like this | Not like this |
|---|---|
| حصتان اليوم. ابدأ بالعلوم. | انطلق نحو النجاح!! |
| ضيّعت يوماً؟ زِد نصف ساعة غداً وواصل. | لا تستسلم أبداً، أنت بطل! |
| الطريقة قبل الساعات. | احصل على 18 مضمونة! |

## Colour
| Name | Hex | Role | Share |
|---|---|---|---|
| Blue | `#2457D6` | Primary: buttons, links, the mark, key numbers | 30% |
| Paper | `#F4F6FB` | Light backgrounds, cards | 55% |
| Ink | `#121A2E` | Text, dark theme background | 10% |
| Slate | `#A7B1C6` | Borders, secondary data, muted marks | 4% |
| Amber | `#F0A23B` | The one warm accent: at most one per screen | 1% |

Contrast (WCAG AA needs 4.5:1 for text):
- Pass: white on Blue 6.16, Blue on Paper 5.70, Ink on Paper 16.01, Paper on Ink 16.01, Amber on Ink 8.19, Slate on Ink 8.04.
- Fail: Amber on Paper 1.95 and Slate on Paper 1.99 (fills and borders only, never text on light); Blue on Ink 2.81 (on dark, the mark and links go white).

No purple. No gradients.

## Type
- **Headings and wordmark:** Readex Pro 600 / 700.
- **Body and UI:** IBM Plex Sans Arabic 400 / 500 / 600. Line height 1.7 for body, 1.3 for headings.
- **Numbers:** Western digits 0–9, tabular figures for scores, timers and stats.
- **Scale (rem):** 0.75 caption · 0.875 small · 1 body · 1.125 lead · 1.375 h3 · 1.75 h2 · 2.25 h1 · 3.5 display (countdown only).

## Logo
- **Mark:** the letter ع written with a flat calligraphy pen: thick and thin strokes, sharp cut ends. The lower curve drops, turns and climbs to the right past where it started: steady progress. Two geometric alternatives (cut rings, and rings with pen contrast) are kept in `svg/` as variations 2 and 3.
- **Lockups:** mark + عزم (RTL, mark on the right); mark + “Azm” for French or English; mark alone.
- **Colour versions:** blue on white, white on blue, white on ink, single-colour ink.
- **Clear space:** the height of the ع's lower curve on every side. **Minimum:** 20 px for the mark, 80 px wide for a lockup.
- **Don't:** stretch it, add shadows or gradients, recolour it outside the palette, or place it on busy images.

## Social templates
Lots of empty space, at most two colours plus white, no photos, no emoji, one idea per post. Templates in `social/` (editable HTML + PNG): post 1080×1350 (ink and white), story 1080×1920 (number-led), reel cover 1080×1920 (title inside the centre crop), YouTube thumbnail 1280×720 (four words at most, one big number), testimonial 1080×1350 (blank: fill with a real student's grades and words, first name or initials only).

## Files
`svg/` logos · `png/` logos at 512 and 1024 · `icons/` favicon.svg/.ico, apple-touch-icon 180, PWA 192/512, maskable 192/512 · `social/` templates · `BRAND.md`.

Not yet done (needs the Azm app repo): owl mascot redraw, design tokens in the app, replacing the purple theme, the `/brand` route, web manifest update (`theme_color` and `background_color` `#121A2E`).
