import torch
from transformers import MarianMTModel, MarianTokenizer
import argparse
from tqdm import tqdm

def setup_baseline_transformer():
    model_name = "Helsinki-NLP/opus-mt-ja-en"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return model, tokenizer

def translate_batch(texts, model, tokenizer, device='cuda', batch_size=32):
    model = model.to(device)
    translations = []
    
    # Process in batches
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True).to(device)
        
        with torch.no_grad():
            translated = model.generate(**inputs)
            
        outputs = tokenizer.batch_decode(translated, skip_special_tokens=True)
        translations.extend(outputs)
    
    return translations

def process_file(input_file, output_file, model, tokenizer, device='cuda'):
    """
    Reads input file line by line, translates each line, and writes to output file
    """
    # Read all lines from input
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    translations = []
    for i in tqdm(range(0, len(lines), 32), desc="Translating"):
        batch = lines[i:i + 32]
        batch_translations = translate_batch(batch, model, tokenizer, device)
        translations.extend(batch_translations)
    
    # Write translations to output
    with open(output_file, 'w', encoding='utf-8') as f:
        for translation in translations:
            f.write(translation + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_file')
    parser.add_argument('--device', default='cuda')
    parser.add_argument('--batch_size', type=int, default=32)
    
    args = parser.parse_args()
    
    # Iff CUDA is available when requested
    if args.device == 'cuda' and not torch.cuda.is_available():
        print("CUDA not available, falling back to CPU")
        args.device = 'cpu'
    
    # Setup model
    print("Loading model...")
    model, tokenizer = setup_baseline_transformer()
    
    # Process file
    print(f"Translating {args.input_file} to {args.output_file}")
    process_file(args.input_file, args.output_file, model, tokenizer, args.device)
    
    print("Translation completed!")

if __name__ == "__main__":
    main()