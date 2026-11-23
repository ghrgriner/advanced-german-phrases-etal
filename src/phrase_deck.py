'''Create file for loading into Anki flashcard program

Anki software does have the ability to indicate column names in the input
file, but it does not support simply using the first row as column names.
We use the simple input format of having no names in the input file
whatsoever, although we do save them to a separate file for housekeeping.
'''

import csv
import urllib
import pandas as pd
import numpy as np

#------------------------------------------------------------------------------
# Parameters
#------------------------------------------------------------------------------

# Input
NOTES_FILE = '../output/german_phrases_etal.tsv'
EX_FILE = '../output/german_phrases_examples.tsv'
PG_FILE = '../output/project_gutenberg_refs.tsv'
# Output
OUTPUT_FILE = '../output/german_phrases_deck.tsv'
FIELDS_FILE = '../output/german_phrases_deck_fields.tsv'

OUTVARS = ['note_id','sheet_is_M','en1','de1','de1_hint','part_of_speech',
    'de_answer','de_ans_cit','de_ans_cit_more','related_entries',
    'gc_front_is_DE1O','gc_front_is_DE1_or_DE1O','gc_front_is_EN',
    'gc_front_is_ST','n_de1','dib_chapter_list',
    'de3_1','de3p_1','de3_2','de3p_2','de3_3','de3p_3',
    'de3_4','de3p_4','de3_5','de3p_5',
'ex_ob_1','ex_hint_1','exc_template_1','exc_answer_1','exc_filled_1','ex_cit_1',
'ex_ob_2','ex_hint_2','exc_template_2','exc_answer_2','exc_filled_2','ex_cit_2',
'ex_ob_3','ex_hint_3','exc_template_3','exc_answer_3','exc_filled_3','ex_cit_3',
'ex_ob_4','ex_hint_4','exc_template_4','exc_answer_4','exc_filled_4','ex_cit_4',
    'wk_cit_1','wk_cit_2']

#------------------------------------------------------------------------------
# Functions
#------------------------------------------------------------------------------
def date_to_year(dt):
    return pd.to_datetime(dt).year

def url_to_page_title(ref):
    if 'coerll.utexas.edu' not in ref and '&oldid=' not in ref:
        raise ValueError(f"'&oldid=' not found in {ref=}")
    start = ref.split('&oldid=', maxsplit=1)[0]
    rest = 'w/index.php?title='
    enwks = 'https://en.wiktionary.org/'
    dewks = 'https://de.wiktionary.org/'
    dewps = 'https://de.wikipedia.org/'
    if start.startswith(enwks + rest):
        almost = start[len(enwks + rest):]
    elif start.startswith(dewks + rest):
        almost = start[len(dewks + rest):]
    elif start.startswith(dewps + rest):
        almost = start[len(dewps + rest):]
    elif ref.startswith('https://coerll.utexas.edu/dib/'):
        return 'Deutsch im Blick'
    else:
        raise ValueError(f'bad ref: {ref=}, {start=}')
    return urllib.parse.unquote(almost).replace('_', ' ')

def make_citation_ex(row):
    return make_citation(row['ref_url'], row['ref_dt'], row['pg_cit'])

def make_citation_de_ref(row):
    return make_citation(row['de_ans_ref_url'], row['de_ans_ref_dt'], None)

def simple_cit_1(row):
    return simple_cit(row['wk_url_1'], row['wk_title_1'])

def simple_cit_2(row):
    return simple_cit(row['wk_url_2'], row['wk_title_2'])

def simple_cit(ref, title):
    if '.wiktionary.org/' in ref:
        res = '<a href="' + ref + '">' + title + '</a>. In Wiktionary.'
        return res
    elif ref == '':
        return ''
    else:
        raise ValueError(f'ref not expected {ref=}')

def make_citation(ref, ref_dt, pg_cit):
    # Title (Year). In Wikipedia. [URL]
    # Title (Year). In Wiktionary. [URL]
    # TODO: project gutenberg ends in '.'

    if 'wiktionary' in ref or 'wikipedia' in ref:
        title = url_to_page_title(ref)
        year = date_to_year(ref_dt)

        if 'wiktionary' in ref:
            source = 'Wiktionary'
        else:
            source = 'Wikipedia'
        #res = title + '. (' + str(year) + '). In ' + source + '. [<a>' + row['ref'] + '</a>]'
        if '"' in title:
            raise ValueError(f'quote in {title=}')
        res = '<a href="' + ref + '">' + title + '</a>. (' + str(year) + '). In ' + source + '.'
    elif 'gutenberg' in ref:
        res = pg_cit
    elif 'coerll' in ref:
        title = url_to_page_title(ref)
        year = date_to_year(ref_dt)
        res = 'Abrams, Z. <a href="' + ref + '">' + title + '</a>. Retrieved ' + str(year) + '.'
    else:
        res = ''
    return res

def transpose_examples(df):
    df_long = pd.melt(df, id_vars=['note_id','ex_index'],
       value_vars=['exc_filled','exc_template','ex_hint','exc_answer','ex_cit',
                   'ex_ob'],
       var_name='ex_var',
       value_name='ex_val')
    df_long['new_name'] = df_long.ex_var + '_' + df_long.ex_index.astype(str)
    #print(df_long)

    return df_long.pivot(index='note_id', columns='new_name', values='ex_val')

def add_vars_merge_and_write(notes, ex):
    notes['sheet_is_M'] = notes.sheet.map(lambda x: 'Y' if x == 'M' else '')
    notes['n_de1'] = notes.de1.map(lambda x: len(x.split(';')) if not pd.isna(x) else 0)
    notes['de3_list'] = notes.de3.map(lambda x: x.split(';') if not pd.isna(x) else [])
    notes['de3p_list'] = notes.de3p.map(lambda x: x.split(';') if not pd.isna(x) else [])
    for idx in [1, 2, 3, 4, 5]:
        notes['de3_' + str(idx)] = notes.de3_list.map(
            lambda x: x[idx-1].strip() if len(x) >= idx else '')
        notes['de3p_' + str(idx)] = notes.de3p_list.map(
            lambda x: x[idx-1].strip() if len(x) >= idx else '')
    notes['gc_front_is_DE1O'] = notes.gc_front.map(lambda x: 'Y' if x == 'DE1O' else '')
    notes['gc_front_is_DE1_or_DE1O'] = notes.gc_front.map(lambda x: 'Y' if x == 'DE1' or x == 'DE1O' else '')
    notes['gc_front_is_EN'] = notes.gc_front.map(lambda x: 'Y' if x == 'EN' else '')
    notes['gc_front_is_ST'] = notes.gc_front.map(lambda x: 'Y' if x == 'ST' else '')

    notes = notes.merge(ex, on='note_id', how='left')
    dfout = notes[OUTVARS]
    dfout.to_csv(OUTPUT_FILE, sep='\t', quoting=csv.QUOTE_NONE, header=False, index=False)
    dfout[0:0].to_csv(FIELDS_FILE, sep='\t',
             index=False, quoting=csv.QUOTE_NONE)

def main():
    notes = pd.read_csv(NOTES_FILE, sep='\t', quoting=csv.QUOTE_NONE)
    notes = notes[notes.use_note == 'Y']
    ex = pd.read_csv(EX_FILE, sep='\t', quoting=csv.QUOTE_NONE)
    pg = pd.read_csv(PG_FILE, sep='\t', quoting=csv.QUOTE_NONE, keep_default_na=False)
    ex = ex.merge(pg[['url','citation']].rename(columns = {'citation': 'pg_cit'}),
                  left_on='ref_url', right_on='url', how='left')
    ex['pg_cit'] = ex.pg_cit.fillna('')
    ex['ref_url'] = ex.ref_url.fillna('')
    ex['ex_cit'] = ex[['ref_url','ref_dt','pg_cit']].apply(make_citation_ex, axis=1)
    ex['ex_ob'] = np.where(ex.ref_sect == 'BACK', 'Y', '')
    notes['de_ans_ref_url'] = notes.de_ans_ref_url.fillna('')
    notes['de_ans_cit'] = notes[['de_ans_ref_url','de_ans_ref_dt']].apply(make_citation_de_ref, axis=1)
    notes['de_ans_cit_more'] = notes.de_ans_ref_more
    vars_ = ['wk_url_1','wk_title_1','wk_url_2','wk_title_2']
    for var in vars_:
        notes[var] = notes[var].fillna('')
    notes['wk_cit_1'] = notes[['wk_url_1','wk_title_1']].apply(simple_cit_1, axis=1)
    notes['wk_cit_2'] = notes[['wk_url_2','wk_title_2']].apply(simple_cit_2, axis=1)
    #print(ex[['ref','ref_dt','ex_cit']])

    #print(notes)
    #print(ex)
    #print(pg)
    ex_trp = transpose_examples(ex)
    add_vars_merge_and_write(notes, ex_trp)

if __name__ == '__main__':
    main()
