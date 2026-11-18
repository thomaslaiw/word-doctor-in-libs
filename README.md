# Word Doctor · Library

A library reading activity for Hong Kong primary learners (P5–P6).
Children photograph a page of the book they are holding, tap the words they
find risky, and then diagnose ten sentences built around those words. A
language model writes the items and gives its own reading of each sentence.
The child commits to an answer **before** the machine speaks.

**Live:** https://thomaslaiw.github.io/word-doctor-in-libs/

---

## The problem

A school library has books and devices, and the devices win. A child who sees a
tablet picks up the tablet. Starting a book needs a motive strong enough to
survive the first page, and a school break is too short to reach it. So the
books sit unused.

This app does not fight the device. It points it at the book: the child plays on
the device, and the thing the device is about is a book on the shelf.

---

## What it does

Three ways in:

| Mode | What it does |
|---|---|
| **Easiest words** | ten words other readers got right most often |
| **Hardest words** | ten words that keep tripping readers up |
| **Scan a book page** | photograph a page, pick your own words, then play |

The scan flow:

1. photograph a page (camera, or a photo already on the device)
2. the text appears, word by word
3. tap a word — it is spoken aloud, and its Chinese meaning appears
4. tap again to keep it
5. start the quiz

Then: ten diagnostic questions, a fill-in-the-blank sentence after every five,
and a score page. Sound for right and wrong. Confetti above 80%.

---

## Why the questions look the way they do

- The four options are **diagnoses**, not replacement words. A diagnosis has to
  be read and understood, so the question stays a reading question.
- Roughly two in five sentences have **nothing wrong with them**. A child cannot
  win by always pressing the first option.
- The **machine never speaks first**. The child commits, then reads the AI
  comment. If the comment arrived first, the child would have nothing to weigh.
- Sentences always come from **Simple Wikipedia**, never from the page just
  scanned — reusing that page turns the quiz into a comprehension check on the
  page instead of a vocabulary task.
- When the reader cannot read a word it marks it, and the app replaces that word
  and its neighbour with a gap: `"I go [unclear]chool by bus"` becomes
  `"I ... ... by bus"`. A half word left in the text makes every item a
  spelling question instead of a meaning question.

---

## What is stored

| Data | Where |
|---|---|
| Your DeepSeek API key | that browser only |
| The photographed page | never stored |
| Word counts (attempts, correct) | that browser, or a shared bank if configured |
| **Who answered what** | **not stored anywhere** |

There are no learner accounts and no leaderboard of names. The word bank holds
two integers per word and cannot identify a reader.

---

## Running it

Open `index.html`. Enter the class password and a DeepSeek API key
(get one at platform.deepseek.com). Nothing to install — see
[`requirements.txt`](requirements.txt).

Optional shared word bank, so several devices feed one ranking:

```bash
python3 stats_server.py --port 8099
```

Then set `STATS_URL` near the top of `index.html` to that server's HTTPS address.
A static site cannot run a server, which is why this is a separate file.

---

## Files

| File | What it is |
|---|---|
| `index.html` | the whole application, one file |
| `stats_server.py` | optional shared word bank (Python standard library only) |
| `report-en.md` | design report, English |
| `report-zh.md` | 設計報告,中文 |
| `requirements.txt` | why there is nothing to install |

---

## Credit

Sentence material from [Simple English Wikipedia](https://simple.wikipedia.org),
CC BY-SA. Model: DeepSeek (`deepseek-flash` for reading photographs,
`deepseek-chat` for writing items).

Built for INT4099 *Emerging Technologies for Language Education*, EdUHK.
