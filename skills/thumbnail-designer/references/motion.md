# Motion — logo stings, animated posts, banner ads

Motion is producible here, with real files: `animate.py` renders an HTML design frame by
frame through headless Chromium and encodes with ffmpeg. MP4, WebM, GIF or a PNG frame
sequence. If ffmpeg is missing, `--frames-only` still produces the sequence — and the
script refuses to pretend otherwise.

```
python scripts/animate.py assets/templates/logo-reveal.html out.mp4 \
  --size 1920x1080 --duration 2.6 --fps 30 --gif out.gif \
  --var MARK="work/mark.svg" --var WORDMARK="work/wordmark.svg" \
  --var BASE="#0B1220" --var ACCENT="#2FB4FF" --var KNOCKOUT=1 --var TAG="..."
```

---

## 1. How the rendering works, and why it matters

The page is **not screen-recorded**. For each frame, every running animation is paused
and its `currentTime` set to that frame's exact time through the Web Animations API. A
slow machine therefore produces identical timing to a fast one, and staggered delays stay
correct because each animation keeps its own timeline.

Consequence for templates: **every animation must use `fill: both`** (`animation-fill-mode:
both`). Without it an animation reverts to its un-animated values once its time has passed,
and the tail of the clip renders wrong while the head looks fine.

---

## 2. Timing

| Piece | Length | Why |
|---|---|---|
| Logo sting | 1.5–3 s | longer and it is an obstacle between viewer and content |
| Social post loop | 3–6 s, seamless | it will play repeatedly; the loop point must not bump |
| Banner ad | ≤15 s, often a hard platform cap | and it must end on the message, held |
| Lower third | 0.6–1 s in, hold, 0.4 s out | |

- **Ease, never linear.** `cubic-bezier(.19,1,.22,1)` for entrances — fast start, long
  settle. Linear motion reads as a slideshow transition.
- **Overlap, do not queue.** The next element starts before the previous finishes.
  Sequential animations with gaps feel broken.
- **Move one thing at a time.** Everything animating at once is noise.
- **End on a hold.** The final second is the logo or the message, still. That frame is
  what gets screenshotted and remembered.
- 30 fps is right for most of this. 60 only if there is fast continuous movement.

---

## 3. Design rules that only bite in motion

**A brand-colour logo on a brand-colour background disappears.** This is the single most
common failure, and it is invisible in a static mock because you check the mock against a
white page. On a dark sting, use the knockout version (`--var KNOCKOUT=1`). Check the
*filmstrip*, not one frame.

- **Build with masks and wipes, not fades.** A fade reads as a transition between two
  slides; a wipe or a rise out of a mask reads as construction.
- **Keep highlight sweeps narrow and weak.** A wide bright sweep stops being a highlight
  on the logo and becomes a white bar crossing the frame.
- **Nothing important in the first 3 frames or the last 3.** Players and platforms clip.
- **Safe areas still apply** — see `platform-specs.md`. Vertical video loses the top 10%
  and bottom 20% to UI.

---

## 4. Formats

| Output | Use | Notes |
|---|---|---|
| **MP4** (H.264, yuv420p) | the default for everything | `faststart` is set; even dimensions enforced, or many players refuse it |
| **WebM** (VP9, yuva420p) | when transparency is genuinely needed | large; limited support |
| **GIF** | email, chat, some ad slots | no alpha worth having, big files — the 2.6 s 1080p test came out 40× the MP4 |
| **PNG frames** | handing to a video editor | `--frames-only`; no ffmpeg needed |

`animate.py` probes the finished file and prints width, height, frame count and duration.
Those are measurements, not intentions — quote them in the delivery note.

---

## 5. What is not possible here

Say these plainly rather than approximating them:

- **No After Effects / Premiere / Lottie project files.** The HTML template is the source.
- **No audio.** No music, no sound design, no voiceover.
- **No video editing** of footage the user supplies — this renders designs, it does not cut.
- **No 3D.** CSS transforms give a perspective illusion; they are not a 3D renderer.
- **No character animation or morphing.**

If the user needs any of those, deliver what this can make — the sting, the frames, the
storyboard with exact timings — and name the tool that does the rest.

---

## 6. Checks

- [ ] Built a filmstrip from the frames and **looked at it** — first frame, every beat,
      last frame. A probe that says 78 frames tells you nothing about whether it works
- [ ] Logo/type contrasts against the background at every moment, not just at the end
- [ ] Easing present; nothing linear; nothing animating alone for more than a beat
- [ ] Ends held, on the message
- [ ] Loops cleanly if it is a loop
- [ ] Duration, size and fps quoted from the probe output
- [ ] Format and limitations stated — no implied After Effects file, no implied audio

Related: `brand-identity.md` (the logo being animated), `deliverables.md`,
`platform-specs.md`, `assets/templates/logo-reveal.html`.
