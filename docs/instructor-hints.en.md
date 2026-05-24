# Instructor Hints

This file is for instructors. It is not a student answer sheet. Use it for prompts, observation points, and adapting to different student levels. Code-level answers are separated into `docs/solutions.en.md`.

## Basic Facilitation Policy

- Before showing the answer, ask "In which context did this data become code?"
- Emphasize the flow between screen, HTTP, database, cookie, and shell rather than memorizing payloads.
- Fix one vulnerability at a time: observe, modify, retest.
- Before and after the exercises, clearly remind students not to test these techniques against external sites or third-party services.

## Exercise 0: Startup Check

Expected state:

- `http://localhost:8086` opens.
- `koide` / `password` logs in.
- BBS posting works.
- `app/data.db` is created.

Common blockers:

- The virtual environment is not active.
- Port 8086 is already in use.
- The student is using the wrong port or URL.

Prompts:

- "What URL is shown in the terminal for the running server?"
- "What do you see when you open `/cookies` after login?"

## Exercise 1: Bottle Routing

Understanding to check:

- `@get("/hello/<name>")` connects a URL to a Python function.
- `<name>` becomes the function argument `name`.
- `template()` creates the HTML response.

Follow-up questions:

- "What changes between `/hello/alice` and `/hello/bob`?"
- "Where does the app separate a function that returns HTML from a function that touches the database?"

## Exercise 2: Peewee and SQLite

Expected observations:

- The `users` and `comments` tables exist.
- `users.password` stores plain-text passwords.
- `comments.user_id` points to the author.

Prompts:

- For beginners, compare the model definition and `.schema` output line by line.
- For experienced students, move toward a password hashing design.

## Exercise 3: Session Hijacking

Expected observations:

- `/cookies` compares the browser-stored value and the app-used value after signature verification.
- `/cookies` can replace the browser-stored value.
- `/cookies` can create a signed cookie from an internal value such as `user1`.
- The raw signed cookie value is long.
- Internally, the app restores a value such as `user1`.
- Copying a cookie can reproduce login state.

Prompts:

- "Is the value stored in the browser the same as the value the app uses?"
- "What does a signed cookie prevent, and what does it not prevent?"
- "After a cookie is stolen, does password authentication still help?"

Instructor notes:

- Because `secret=COOKIE_SECRET` is used, manually entering `user1` as the browser-stored value does not work.
- The `/cookies` edit form is an exercise helper and should not exist in a real service.
- Signing detects tampering but does not prevent cookie leakage.
- `HttpOnly` blocks JavaScript reads, but it does not stop the browser from automatically sending cookies with requests.

## Exercise 4: XSS

Expected observations:

- A BBS post is interpreted as HTML.
- The helper server receives a cookie string.
- The root cause is `{{!comment.comment}}` in `app/views/bbs.tpl`.

Prompts:

- "On which screen was your input interpreted as HTML?"
- "Was the danger created when saving, or when displaying?"
- "How would cookie attributes change the impact?"

Instructor notes:

- Emphasize output escaping for the target context, not simply deleting input.
- `HttpOnly` reduces cookie theft impact, but it is not the root fix for XSS.

## Exercise 5: CSRF

Expected observations:

- A logged-in browser opens helper `/csrf`.
- Pressing the button posts to BBS.
- A fixed hidden token is not a defense.

Prompts:

- "Which site served the form?"
- "Which site received the POST?"
- "Who attached the cookie?"
- "Why does a fixed token not protect the action?"

## Exercise 6: SQL Injection

Expected observations:

- The displayed SQL `WHERE` clause is broken by the input.
- `' or 'a'='a` makes the condition always true.
- User input is interpreted as SQL structure.

Prompts:

- "Where did the input enter the SQL?"
- "What does it mean to separate SQL structure from values?"
- "What is missing if we only say 'sanitize it'?"

## Exercise 7: Command Injection

Expected observations:

- `/contact` concatenates input into a shell command.
- `"; /bin/echo injected > command_injection_result.txt; #` starts a second command.
- The root cause is `os.system(command)`.

Prompts:

- "Which character ended the intended string?"
- "Which character started the next command?"
- "Does this feature need a shell at all?"

## Exercise 8: Pico.css UI Cleanup

Expected observations:

- Shared navigation can be centralized in `base.tpl`.
- `login.tpl` becomes easier to read.
- Pico.css improves the look without memorizing many classes.

Review points:

- Are security changes and UI changes kept separate?
- Did the student add new `{{! ... }}` output without thinking?
- Can the student explain what to do if a CDN is unavailable?

## Exercise 9: Fix the Vulnerabilities

Advanced grading points:

| Point | Sufficient state |
| --- | --- |
| Root cause | Explains the risky code location and why it is risky |
| Fix | Prevents input from being interpreted as code |
| Retest | The previous successful attack input now fails |
| Side effects | Normal login, posts, and contact form still work |
| Explanation | Goes beyond "sanitize it" and explains context |

## Level-specific Prompts

For beginners:

- Ask them to describe "which screen, what input, what changed."
- First follow the screen and HTTP flow, before focusing on exact line numbers.
- Use `/cookies`, displayed SQL, and helper server logs as observation aids.

For standard-level students:

- Ask them to find the vulnerable code location.
- Ask them to explain the before/after diff.
- Require retesting for one mitigation.

For experienced students:

- Ask them to explain remaining risk when multiple mitigations are combined.
- Have them implement password hashing, CSRF tokens, and cookie attributes.
- Encourage tests and small refactors.

## Final Presentation Template

For short student presentations:

```text
Vulnerability:
Root cause:
Input tested:
Observed behavior:
Fix:
Retest result:
Remaining risk:
```

Evaluate whether they can explain root cause, context, mitigation, and retest result rather than whether they merely made an attack work.

