from googletrans import Translator
import argparse
from tqdm import tqdm
import os

def translate_batch(texts, translator, batch_size=32):
    translations = []
    for text in texts:
        try:
            result = translator.translate(text, src='ja', dest='en')
            translations.append(result.text)
        except Exception as e:
            print(f"Translation failed: {str(e)}")
            translations.append('')
    return translations

def process_file(input_file, output_file, translator):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    translations = []
    for i in tqdm(range(0, len(lines), 32), desc="Translating"):
        batch = lines[i:i + 32]
        batch_translations = translate_batch(batch, translator)
        translations.extend(batch_translations)

    os.makedirs(os.path.dirname(output_file), exist_ok=True) # Create file if it doesn't exist
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for translation in translations:
            f.write(translation + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_file')
    parser.add_argument('--batch_size', type=int, default=32)
    
    args = parser.parse_args()
    
    translator = Translator()
    
    print(f"Translating {args.input_file} to {args.output_file}")
    process_file(args.input_file, args.output_file, translator)
    
    print("Translation completed!")

if __name__ == "__main__":
    main()