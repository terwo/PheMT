import os

import sacrebleu

types = ['Proper_Noun', 'Abbreviated_Noun:Orig', 'Abbreviated_Noun:Norm', 'Colloquial_Expression:Orig', 'Colloquial_Expression:Norm', 'Variant:Orig', 'Variant:Norm']

def bleu(hyps_grouped, refs_grouped, align_grouped):
    scores = {}
    for hyps, refs, tp in zip(hyps_grouped, refs_grouped, types):
        bleu = sacrebleu.corpus_bleu(hyps, [refs], tokenize='intl')
        scores[tp] = round(bleu.score, 1)
    return scores

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f]

hyps_grouped = [
    read_file('outputs/gtrans_proper.txt'),       
    read_file('outputs/gtrans_abbrevorig.txt'),   
    read_file('outputs/gtrans_abbrevnorm.txt'),   
    read_file('outputs/gtrans_colloqorig.txt'),    
    read_file('outputs/gtrans_colloqnorm.txt'),     
    read_file('outputs/gtrans_variantorig.txt'),    
    read_file('outputs/gtrans_variantnorm.txt')     
]

refs_grouped = [
    read_file('proper/proper.en'),
    read_file('abbrev/abbrev.en'),
    read_file('abbrev/abbrev.en'),
    read_file('colloq/colloq.en'), 
    read_file('colloq/colloq.en'),
    read_file('variant/variant.en'),
    read_file('variant/variant.en')
]

align_grouped = [
    read_file('proper/proper.alignment'),
    read_file('abbrev/abbrev.alignment'),
    read_file('abbrev/abbrev.alignment'),
    read_file('colloq/colloq.alignment'),
    read_file('colloq/colloq.alignment'),
    read_file('variant/variant.alignment'),
    read_file('variant/variant.alignment')
]

scores = bleu(hyps_grouped, refs_grouped, align_grouped)

print("BLEU Scores:")
for type_name, score in scores.items():
    print(f"{type_name}: {score}")