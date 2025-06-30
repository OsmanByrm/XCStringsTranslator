import json
import sys
import os
import argparse
from deep_translator import GoogleTranslator

def translate_xcstrings(input_file, target_language, output_file=None):
    """
    Translate missing translations in a Localizable.xcstrings file to the target language.
    
    Args:
        input_file (str): Path to the input Localizable.xcstrings file
        target_language (str): Target language code (e.g., 'es' for Spanish)
        output_file (str, optional): Path to the output file. If not provided, will overwrite the input file.
    """
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    source_language = data.get('sourceLanguage', 'en')
    strings = data.get('strings', {})
    
    # Initialize translator
    translator = GoogleTranslator(source=source_language, target=target_language)
    
    # Count of missing translations
    missing_count = 0
    translation_count = 0
    total_strings = len(strings)
    existing_translations = 0
    empty_keys = 0
    no_localizations = 0
    skipped_strings = 0
    
    print(f"Total strings in file: {total_strings}")
    
    # Iterate through all strings
    for key, value in strings.items():
        # Skip empty keys
        if key.strip() == "":
            empty_keys += 1
            continue
            
        # Check if the value has localizations
        if 'localizations' not in value or not value['localizations']:
            # If this is a valid string that should be translated
            if key and isinstance(key, str) and len(key) > 1 and not key.isspace():
                missing_count += 1
                try:
                    # Try to translate this key
                    if key.strip():
                        translated_text = translator.translate(key)
                        
                        # Create localizations if not exist
                        if 'localizations' not in value:
                            value['localizations'] = {}
                            
                        # Add the translation
                        value['localizations'][target_language] = {
                            "stringUnit": {
                                "state": "translated",
                                "value": translated_text
                            }
                        }
                        
                        translation_count += 1
                        print(f"Translated key: {key} -> {translated_text}")
                except Exception as e:
                    print(f"Error translating key {key}: {str(e)}")
            else:
                no_localizations += 1
            continue
            
        localizations = value.get('localizations', {})
        
        # Check if target language exists but is not translated
        if target_language in localizations:
            existing_translations += 1
            # Check if it's marked as 'needs_review' or similar
            target_unit = localizations[target_language].get('stringUnit', {})
            state = target_unit.get('state', '')
            if state in ['needs_review', 'new']:
                missing_count += 1
                
                # Get the source string from source language
                source_text = key
                if source_language in localizations and 'stringUnit' in localizations[source_language]:
                    if 'value' in localizations[source_language]['stringUnit']:
                        source_text = localizations[source_language]['stringUnit']['value']
                
                try:
                    # Translate the text
                    if source_text.strip():  # Skip empty strings
                        translated_text = translator.translate(source_text)
                        
                        # Update the translation
                        target_unit["state"] = "translated"
                        target_unit["value"] = translated_text
                        
                        translation_count += 1
                        print(f"Updated string needing review: {source_text} -> {translated_text}")
                except Exception as e:
                    print(f"Error updating review string {source_text}: {str(e)}")
            continue
        
        # Check if the target language is missing
        if target_language not in localizations:
            missing_count += 1
            
            # Get the source string from source language
            source_text = key
            if source_language in localizations and 'stringUnit' in localizations[source_language]:
                if 'value' in localizations[source_language]['stringUnit']:
                    source_text = localizations[source_language]['stringUnit']['value']
            
            try:
                # Translate the text
                if source_text.strip():  # Skip empty strings
                    translated_text = translator.translate(source_text)
                    
                    # Add the translation
                    localizations[target_language] = {
                        "stringUnit": {
                            "state": "translated",
                            "value": translated_text
                        }
                    }
                    
                    translation_count += 1
                    print(f"Translated: {source_text} -> {translated_text}")
                else:
                    skipped_strings += 1
            except Exception as e:
                print(f"Error translating {source_text}: {str(e)}")
    
    # Save the updated data
    if output_file is None:
        output_file = input_file
        
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\nTranslation completed!")
    print(f"Total strings: {total_strings}")
    print(f"Empty keys: {empty_keys}")
    print(f"Strings without localizations field: {no_localizations}")
    print(f"Strings skipped: {skipped_strings}")
    print(f"Existing translations for {target_language}: {existing_translations}")
    print(f"Missing translations found: {missing_count}")
    print(f"Translations added: {translation_count}")
    print(f"Output saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Translate missing translations in a Localizable.xcstrings file')
    parser.add_argument('input_file', help='Path to the input Localizable.xcstrings file')
    parser.add_argument('target_language', help='Target language code (e.g., "es" for Spanish)')
    parser.add_argument('--output', '-o', help='Path to the output file. If not provided, will overwrite the input file')
    
    args = parser.parse_args()
    
    translate_xcstrings(args.input_file, args.target_language, args.output)

if __name__ == "__main__":
    main() 