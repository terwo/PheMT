import subprocess
import os

def run_translation_command(input_file, output_file):
    command = [
        'python3',
        'create_translations/helsinki.py',
        input_file,
        output_file
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Successfully processed {input_file} -> {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing {input_file}: {e}")

def main():
    translations = [
        # {
        #     'input': 'abbrev/abbrev.orig.ja',
        #     'output': 'outputs/helsinki_abbrevorig.txt'
        # },
        # {
        #     'input': 'abbrev/abbrev.norm.ja',
        #     'output': 'outputs/helsinki_abbrevnorm.txt'
        # },
        # {
        #     'input': 'colloq/colloq.orig.ja',
        #     'output': 'outputs/helsinki_colloqorig.txt'
        # },
        # {
        #     'input': 'colloq/colloq.norm.ja',
        #     'output': 'outputs/helsinki_colloqnorm.txt'
        # },
        {
            'input': 'variant/variant.orig.ja',
            'output': 'outputs/helsinki_variantorig.txt'
        },
        {
            'input': 'variant/variant.norm.ja',
            'output': 'outputs/helsinki_variantnorm.txt'
        },
        {
            'input': 'proper/proper.ja',
            'output': 'outputs/helsinki_proper.txt'
        }
    ]
    # Create
    for params in translations:
        run_translation_command(params['input'], params['output'])

if __name__ == "__main__":
    main()