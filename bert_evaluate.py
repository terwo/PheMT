import torch
from bert_score import BERTScorer
import pandas as pd
from tqdm import tqdm
import numpy as np
import os

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() if line.strip() else "" for line in f]

def evaluate_translations(output_dir='outputs/', ref_dir='./'):

    scorer = BERTScorer(
        lang="en",
        rescale_with_baseline=True
    )
    
    # Define phenomena
    phenomena = {
        'proper': {'versions': ['']},  # proper has no norm/orig distinction
        'abbrev': {'versions': ['orig', 'norm']},
        'colloq': {'versions': ['orig', 'norm']},
        'variant': {'versions': ['orig', 'norm']}
    }
    
    phenomenon_scores = {}
    all_results = []
    interesting_examples_by_phenomenon = {}
    
    for phenomenon, config in phenomena.items():
        for version in config['versions']:
            # Skip version suffix for proper
            phenomenon_key = phenomenon if phenomenon == 'proper' else f"{phenomenon}_{version}"
            print(f"\nProcessing {phenomenon_key}...")
            
            try:
                ref_suffix = f"{phenomenon}/{phenomenon}.ja" if phenomenon == 'proper' else f"{phenomenon}/{phenomenon}.{version}.ja"
                ref_path = os.path.join(ref_dir, ref_suffix)
                
                helsinki_suffix = f"helsinki_{phenomenon}{'' if phenomenon == 'proper' else version}.txt"
                google_suffix = f"gtrans_{phenomenon}{'' if phenomenon == 'proper' else version}.txt"
                
                helsinki_path = os.path.join(output_dir, helsinki_suffix)
                google_path = os.path.join(output_dir, google_suffix)
                
                # Read files
                references = read_file(ref_path)
                helsinki_translations = read_file(helsinki_path)
                google_translations = read_file(google_path)
                
                # Check all files have same number of lines
                assert len(references) == len(helsinki_translations) == len(google_translations), \
                    f"Mismatch in number of lines for {phenomenon_key}, with reference: {len(references)}, Helsinki: {len(helsinki_translations)}, Google: {len(google_translations)}"
                
                helsinki_P, helsinki_R, helsinki_F1 = scorer.score(helsinki_translations, references)
                google_P, google_R, google_F1 = scorer.score(google_translations, references)
                
                helsinki_F1 = helsinki_F1.numpy()
                google_F1 = google_F1.numpy()
                
                # DataFrame for this phenomenon and version
                phenomenon_df = pd.DataFrame({
                    'Phenomenon': phenomenon_key,
                    'Reference': references,
                    'Helsinki': helsinki_translations,
                    'Google': google_translations,
                    'Helsinki_F1': helsinki_F1,
                    'Google_F1': google_F1
                })
                
                # Calculate average score
                phenomenon_scores[phenomenon_key] = {
                    'Helsinki': np.mean(helsinki_F1),
                    'Google': np.mean(google_F1)
                }
                
                # Find interesting examples
                interesting_examples = get_interesting_examples(phenomenon_df)
                interesting_examples_by_phenomenon[phenomenon_key] = interesting_examples
                
                # Add to overall results
                all_results.append(phenomenon_df)
                
            except FileNotFoundError as e:
                print(f"Warning: Could not find files for {phenomenon_key}: {str(e)}")
                continue
            except Exception as e:
                print(f"Error processing {phenomenon_key}: {str(e)}")
                continue
    
    # Combine all results
    if all_results:
        results_df = pd.concat(all_results, ignore_index=True)
    else:
        results_df = pd.DataFrame()
    
    return phenomenon_scores, interesting_examples_by_phenomenon, results_df

def get_interesting_examples(df, n=10):
    # Where models differ the most
    df['score_diff'] = abs(df['Helsinki_F1'] - df['Google_F1'])
    high_diff = df.nlargest(n, 'score_diff')
    
    # Best and worst performing for each model
    helsinki_best = df.nlargest(n, 'Helsinki_F1')
    helsinki_worst = df.nsmallest(n, 'Helsinki_F1')
    google_best = df.nlargest(n, 'Google_F1')
    google_worst = df.nsmallest(n, 'Google_F1')
    
    return {
        'largest_differences': high_diff,
        'helsinki_best': helsinki_best,
        'helsinki_worst': helsinki_worst,
        'google_best': google_best,
        'google_worst': google_worst
    }

if __name__ == "__main__":
    phenomenon_scores, interesting_examples, results_df = evaluate_translations()
    
    # Print scores for each phenomenon
    print("\nPhenomenon-wise BERTScore F1 Scores:")
    for phenomenon, scores in phenomenon_scores.items():
        print(f"\n{phenomenon}:")
        print(f"Helsinki: {scores['Helsinki']:.3f}")
        print(f"Google: {scores['Google']:.3f}")
    
    
    results_df.to_csv('detailed_results_full_2.csv', index=False)
    print("\nDetailed results saved to 'detailed_results.csv'")
    
    # # Save interesting examples for each phenomenon
    # for phenomenon, examples in interesting_examples.items():
    #     filename = f'interesting_examples_{phenomenon}_full.csv'
    #     pd.DataFrame(examples['largest_differences']).to_csv(filename, index=False)
    #     print(f"Interesting examples for {phenomenon} saved to {filename}")

    for phenomenon, examples in interesting_examples.items():
        for category, df in examples.items():
            filename = f'interesting_examples_{phenomenon}_{category}_fuller_2.csv'
            df.to_csv(filename, index=False)
            print(f"Saved {category} examples for {phenomenon} to {filename}")