# XCStrings Translator

A simple Python script to automatically translate `Localizable.xcstrings` files for Xcode projects using Google Translate. This tool helps you quickly add new localizations to your iOS or macOS applications by filling in missing translations.

## Xcode Setup

Before using the translator script, you need to set up a `Localizable.xcstrings` file in your Xcode project.

1.  **Create a String Catalog:**
    *   In Xcode, right-click on your project folder in the Project Navigator.
    *   Select **New File From Template**.
    *   In the filter bar, type `String` and select the **String Catalog** template.
    *   Name the file `Localizable.xcstrings` and create it.

2.  **Populate Initial Strings:**
    *   Build and run your project once. Xcode will scan your code for localizable strings (e.g., `String("Hello, World!")` in SwiftUI or `NSLocalizedString`) and add them to your `Localizable.xcstrings` file.

3.  **Translate:**
    *   Once your strings appear in the String Catalog, you can run the Python script to translate them into your desired language.

## Features

-   Translates string values that are missing for a target language.
-   Handles strings that have no localizations yet.
-   Updates strings that are marked for review (e.g., `needs_review` state).
-   Can either overwrite the input file or save the translated content to a new file.
-   Powered by `deep-translator` for translation.

## Requirements

-   Python 3
-   `deep-translator` library

## Installation

To run this script, you first need to install the required Python library:

```bash
pip3 install -r requirements.txt
```

## Usage

Run the script from your terminal and provide the path to your `.xcstrings` file and the target language code.

```bash
python3 translate_strings.py <path_to_input_file> <target_language_code>
```

### Examples

**1. Translate and overwrite the file:**

To translate your `Localizable.xcstrings` file to Spanish (`es`) and update it in place:

```bash
python3 translate_strings.py /path/to/your/project/Localizable.xcstrings es
```

**2. Save translations to a new file:**

To translate the file and save the output to a different file, use the `-o` or `--output` flag:

```bash
python3 translate_strings.py Localizable.xcstrings es -o Localizable_es.xcstrings
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
