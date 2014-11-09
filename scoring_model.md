## How are scores recorded?

Every user is given a login name that ends in either "-1" or "-2", depending on
if they were in group one or group two.

The two groups are exposed to words at different times, and use different
mnemonics (drawing or note taking) to remember words. All users in the same
group get the same exposure and mnemonics. The order of the words and the
nmemonic used will be controlled by the examiner. 

After the user is exposed to words, they take two tests. Every word that appears
in each test falls into one of four categories:

   * nt-imm (note-taking, immediate)
   * dm-imm (drawing, immediate)
   * nt-del (note-taking, delayed)
   * dm-del (drawing, delayed)

Group 1's categorization of each word on the test is different than Group 2's.

The test records each word tested, the user's answer, whether they were correct,
and which category the word belongs in (depending on if they were in group
one or two).

### Example test results

Example test result for a user in group *one*:

|word|answer|correct?|category for group *one*|
|----|------|--------|------------------------|
|foo |fuzz  |0       |nt-imm                  |
|bar |bar   |1       |dm-imm                  |
|qux |qux   |1       |nt-del                  |
|boo |foo   |0       |dm-del                  |

To score this, we'd count how many answers were correct in each category:

|category | count |
|---------|-------|
|nt-imm   | 0     |
|nt-del   | 1     |
|dm-imm   | 1     |
|dm-del   | 0     |

Example test result for a user (with the exact same answers) in group *two*:

|word|answer|correct?|category for group *two*|
|----|------|--------|------------------------|
|foo |fuzz  |0       |nt-del                  |
|bar |bar   |1       |dm-del                  |
|qux |qux   |1       |dm-imm                  |
|boo |foo   |0       |nt-imm                  |

Their scores by category would be different:

|category | count |
|---------|-------|
|nt-imm   | 0     |
|nt-del   | 0     |
|dm-imm   | 1     |
|dm-del   | 1     |

### Data location

`static/data/wordpair-categories.json` contains a dictionary of all test
answers, mapping to a 2-element list of categories, for group 1 and group 2,
respectively.
