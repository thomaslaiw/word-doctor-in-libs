# Word Doctor · Library — design report

**Version:** `deepseek-chat`
**Build:** single-file HTML application, no build step, no dependencies
**Models:** `deepseek-flash` (reads photographs) · `deepseek-chat` (writes questions, translates)

---

## 1. The problem this version addresses

- A school library has books and devices. In practice the devices win.
- A child who sees a tablet picks up the tablet, not the shelf.
- Reading a book needs a motive strong enough to survive the first page.
- A school break is too short to reach that motive — by the time the child is inside the story, the bell goes.
- So the books sit unused while the devices are used for something else entirely.
- **This app does not fight the device. It points the device at the book.**

The design claim in one line:

> The child plays on the device, and the thing the device is *about* is a book in the library.

---

## 2. Environment

- One child, one device, one book. Library or classroom corner.
- No accounts, no login for the child, no class list.
- The only credential involved is the teacher's AI key, stored in that one browser.
- Works without a network for everything except generating new questions.

---

## 3. Three ways in

| Mode | What it does | Needs a network |
|---|---|---|
| **Easiest words** | Ten words other readers got right most often | yes (first time) |
| **Hardest words** | Ten words that keep tripping readers up | yes (first time) |
| **Scan a book page** | Photograph a page, pick your own words, then play | no (once questions exist) |

- The first two modes draw on a **word bank**: a record of how often each word was answered right.
- The bank stores counts per word. It does not store who answered.
- If no shared server is configured, the bank lives in that one browser and the modes say so.

---

## 4. The scan flow

1. **Photograph a page.** Camera or a photo from the device.
2. **The app reads it.** The text appears, word by word.
3. **Tap a word.** It is spoken aloud, and its Chinese meaning appears.
4. **Tap again to keep it.** Kept words collect in *My words*.
5. **Start the quiz.** The app's own picks and the child's picks are merged, ten words in all.

- Tapping the same word twice removes it. Nothing is forced.
- A child can skip the picking entirely and press Start — that is a supported path, not a fallback.
- If the child picks two or three words, the app adds more from the same page at the same level.

**When a word cannot be read.** The reader marks anything it cannot make out. The app then replaces that word and the word beside it with a neutral gap, so *"I go [unclear]chool by bus"* becomes *"I ... ... by bus"*. This matters: a half word left in the text makes the question writer diagnose a spelling mistake, and every item in the run turns into a spelling question instead of a vocabulary one. A gap is honest; a guessed word is not.

**Why the child picks.** Choosing the word is the noticing. A word the child selected because it looked risky is a word they have already begun to think about, and the questions that follow land on ground they prepared.

---

## 5. The quiz

- Ten questions. Each shows one sentence with one highlighted word.
- Four options, but they are **diagnoses**, not replacement words:
  - *Nothing is wrong.*
  - *It should name a place for ships, not a place for buying things.*
  - *It is the wrong kind of word for this position.*
  - *It is too weak a word for this meaning.*
- The child locks an answer, then the comment appears.
- **Sound:** a rising two-note chime for right, a falling two-note for wrong. Generated in the browser; no audio files.
- Roughly two questions in five are *nothing is wrong*. The child cannot win by always pressing the first option.

**Why the options are diagnoses.** If the options were four words, a child could answer by ear. A diagnosis has to be read and understood, so the question stays a reading question.

---

## 6. Fill in the blanks — after every five questions

- One sentence with one to three gaps.
- The child taps a gap, then taps a word from the bank.
- The sentence is chosen to use **as many of the last five words as possible**: the app searches Simple Wikipedia for sentences containing the most of them, and only writes a sentence itself if no published one uses at least two.
- Options may include wrong words, but **never a synonym of an answer**, and never another form of an answer — otherwise the gap is ambiguous and the question is unfair.
- The gaps are not scored. When the five questions are over, the score page shows the ten questions only.
- **The finished sentence is read aloud once the answer is checked**, and a *Hear it again* button repeats it. Hearing the whole sentence with the right words in place is what turns a gap-filling exercise into a phrase the child can say.

**Why it is unscored.** The gap question is the hardest thing in the run, and it comes after five scored ones. Scoring it would punish the child twice for the same difficulty. It is there to make the words work together in one sentence, not to add marks.

---

## 7. The results page

- Score out of ten.
- A line that answers honestly: perfect, strong, good start, or keep going.
- A review list naming the words that were missed.
- Confetti above eighty percent. No confetti below it.
- Two ways out: play again, or home.

---

## 8. Pedagogy

### 8.1 The mapping asked for

| Element of the app | Learning theory | Where it comes from |
|---|---|---|
| The whole activity as a game with sound, score and celebration | **Behaviourism** | prompt → response → immediate feedback → repeat |
| Picking your own words, and filling a gap with the right word | **Constructivism** | the learner builds meaning from their own reading, not from a list given to them |
| Judging whether a word is used correctly in a sentence | **Cognitivism** (the simpler end) | noticing a pattern, then analysing an error and refining understanding |
| The score, the review list, the ten-item record | **Assessment and evaluation** | evidence of learning, and a judgement the child can act on |

- Behaviourism is claimed **only** for the game shell. Points do not teach meaning.
- The learning sits in the constructivist and cognitivist rows.
- The design deliberately keeps the two apart, because a lesson that confuses "the child enjoyed it" with "the child learned something" is the commonest failure in this kind of app.

### 8.2 The TELL six elements

| Element | This design |
|---|---|
| Learner need | A library full of books that nobody starts |
| Learning objective | Judge whether a word is used correctly, name a risky word, state a rule about trusting AI |
| Learning theory | Constructivism primary; cognitivism for the mechanism; behaviourism only for the shell |
| Activity | Scan, choose, diagnose ten sentences, fill gaps in a fifth sentence |
| Technology | OCR to bring the book in; a language model to write diagnosable items and to speak and gloss a word |
| Learning evidence | Ten answers, the words chosen, the gaps filled, the review list |

### 8.3 Why the technology, and not a worksheet

- A worksheet cannot read the book the child is holding.
- A worksheet cannot say a word out loud when a child taps it.
- A worksheet cannot write a new question about a page it has never seen.
- **The camera is the reason this works in a library at all.** It makes any book in the room the input.

### 8.4 A warning that shaped the design

From the course material: *if AI gives the answer too early, learners stop inferring, rereading and monitoring comprehension.*

- Here the machine never speaks first. The child commits, then reads the comment.
- Two in five questions have nothing wrong, so the machine's own comment is not a reliable shortcut.

---

## 9. What is stored, and what is not

| Data | Where | Why |
|---|---|---|
| The teacher's API key | That browser only | to call the model |
| The scanned photograph | Never stored; read in the browser | privacy |
| Word counts (attempts, correct) | That browser, or a shared bank if one is configured | drives Easiest / Hardest |
| Who answered what | **Not stored anywhere** | no learner record, no leaderboard of names |
| Chinese glosses already looked up | That browser, as a cache | so a second tap is instant |

- The shared word bank is **optional**. Run `stats_server.py` if several devices should share one bank.
- A purely static site such as GitHub Pages cannot run a server. That is why the shared bank is a separate small file rather than a built-in feature.
- Even with the shared bank, it holds two integers per word. There is no way to identify a reader from it.

---

## 10. Honest limits

- **The model can still be wrong.** It writes the comment; a comment that is confidently incorrect is possible. The review list and the teacher's presence are the guard, not the model.
- **A generated sentence is weaker than a published one.** Quiz sentences always come from Simple Wikipedia, never from the page the child just scanned — reusing that page turned the quiz into a comprehension check on the page instead of a vocabulary task. Only when no published sentence contains the word does the app write a short one itself, and the app does not hide that.
- **OCR fails on poor light and small print.** The text is editable, and typing is a supported route.
- **Ten questions may be too few to trust the "hardest" list early on.** The bank needs a few dozen answers before the ordering means anything, and the app says how many words it holds.
- **No adaptation within a run.** The difficulty of question six does not depend on question five. The modes are the only adaptivity.
- **The fill-in-the-blank depends on the five words being compatible.** When they are not, the question is skipped rather than forced.

---

## 11. Files

```
deepseek-chat/
  index.html         the whole app, one file
  stats_server.py    optional shared word bank (python3, no dependencies)
  report-en.md       this file
  report-zh.md       中文版
```

- To run: open `index.html`. Enter the class password and a DeepSeek key.
- To share a word bank across devices: `python3 stats_server.py --port 8099`, then set `STATS_URL` in `index.html` to that address over HTTPS.
