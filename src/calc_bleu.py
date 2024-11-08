# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import sys
import nltk
from nltk.translate.bleu_score import corpus_bleu
from nltk.tokenize import word_tokenize


# +
def calculate_bleu(output_file, proper):
    # Read files
    with open(output_file, 'r', encoding='utf-8') as f_hyp, \
         open(proper, 'r', encoding='utf-8') as f_ref:
        # By lines
        output_lines = [line.strip() for line in f_hyp]
        proper_lines = [line.strip() for line in f_ref]

    # Tokenize all sentences
    hypotheses = [word_tokenize(line.lower()) for line in output_lines]
    
    # List of list of references
    references = [[word_tokenize(line.lower())] for line in proper_lines]

    # BLEU score
    bleu_score = corpus_bleu(references, hypotheses)
    return bleu_score

def main(args):
    if len(args) < 2:
        print('[USAGE] python src/calc_bleu.py output_file alignment_file')
        sys.exit(1)

    output_file = args[0]  # outputs/helsinki_proper.txt
    proper = args[1]   # proper/proper.en

    bleu_score = calculate_bleu(output_file, proper)
    print(f'BLEU: {round(bleu_score, 3)}')

if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
