# Overview

This is a small repository with a text file (deck) of advanced German phrases
(n = ~4000)
for learners of German. Currently, we haven't added translations
or to this public deck, but we might do so in the future. There are over 1000
example sentences. We may continue to add such sentences, but until then, an
AI will have to suffice for interested users.

Two subsets of notes are worth highlighting:

1. The deck contains all high-frequency idioms (that meet this
   project's 'phrase criterion') from the English-language or
   German-language Wiktionary (as of 18Jun2025).

2. We used [Deutsch im Blick](https://coerll.utexas.edu/dib/index.php) and
   [Grimm Grammar](https://coerll.utexas.edu/gg)  as our
   first-year textbook and companion grammar and therefore
   this deck contains vocabulary from those sources
   meeting the phrase criteria.

For both of the above, we have separate repositories where we
describe in detail the extraction process and we have indicators in
this deck for notes meeting either of these criteria. See (1) https://github.com/ghrgriner/german-idiom-freq
and (2) https://github.com/ghrgriner/deutsch-im-blick.

We use Anki flashcard software for study, so these notes occasionally
refer to this software, but the deck should be suitable for use
with other software. (Well, once card prompts are added.)

See [LICENSE.txt](LICENSE.txt) and [DiBGG\_LICENSE.txt](DiBGG_LICENSE.txt) for
complete license and attribution
details for Wiktionary, Deutsch im Blick, Grimm Grammar, and for this repository.

# Repository contents

Currently the repository contains only the deck file `german_phrases_etal.tsv`
in the output/ directory and documentation. In the future we will likely
add code. For example, we will probably provide the code that
goes from answer template (with blanks) and answer field to a complete
(and formatted) sentence on the card's back. (We don't use Anki's
'cloze card' template, but interested users should be able to process the
card to use this template if desired.)

# Deck contents

## Overview

We have restricted the deck to notes in our vocabulary list
where the headword contains a space. Generally, we construct the
headword by removing any leading definite article or 'sich' and
proceed until the first '(' or '['. However, there are some notes
where this rule will not work and we assign the headword manually
(see `de_headword`). There may be a few notes where this manual
assignment slipped through the cracks. For example, generally for
notes of the form 'sich + prepositional phrase + infinitive', we
manually assign the headword to the infinitive.

## Card types

We will start by describing how we store our vocabulary internally.

We use two worksheets to store our vocabulary for German. One sheet
contains words or phrases we think one is likely to encounter in
most languages. We call this the 'Main' sheet. The other sheet is for
German-specific lexical entries and synonyms. For example, 'ein Stachel
in Fleisch sein' is on the 'Main' sheet and 'ein Dorn im Auge sein'
is on the German sheet. This is to make the 'Main' sheet cards easier,
because it's unrealistic to ask oneself to produce many German answers
for a given note. If we think the two synonyms have similar frequency,
we might provide hints on each card (e.g., 'not: Dorn').

On the German sheet, we might make the answer
be German (or both German + English, but in practice, if a German answer
is required, we typically just produce the German for studying and use the
English for reference if we fail the card).

We format each card as a table with (usually, see `gc_front`) the
German headword or its English translation in the first row of the
table. The plural of nouns, adjective comparative, or verb forms
are in the second row on the back of the card. The second row is
empty on the front. Any additional answers that we want to make ourselves
produce are in additional rows of the table. For 'Main' sheet notes,
we generally use English prompts for each row. For 'German' sheet notes,
the prompts can be more complex (see `gc_front` below).

After the table with the card prompts and answers we might include
supporting information on the card in other fields, such as general
notes about usage that are too long for the table, words and their
translations that we often confuse with the target word, etc.

## Text file contents

The fields for `output/german_phrases_etal.tsv` and `output/german_phrases_examples.tsv`
are documented in the wiki (here)[https://github.com/ghrgriner/advanced-german-phrases-etal/wiki/Text-file-fields].

# Wiki

The repository [wiki](https://github.com/ghrgriner/advanced-german-phrases-etal/wiki) has
some further discussion.
The wiki home page linked has the recommended reading order.

# Trademark Notice

Wiktionary and Wikipedia are trademarks of the Wikimedia Foundation and
are used with the permission of the Wikimedia Foundation. We are not
endorsed by or affiliated with the Wikimedia Foundation.

Anki is a registered trademark of Ankitects Pty Ltd.
We are not endorsed by or affiliated with Ankitects Pty Ltd.
