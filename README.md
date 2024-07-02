# Lbom (licenses for boms) is a tool for fetching license information for components in CycloneDX files

Lbom is a powerful tool designed to fill license information for components in CycloneDX files. It automatically adds missing licenses to components, ensuring comprehensive license tracking for your software projects.

## Usage

```
lbom [-h] --input_file INPUT_FILE [--output_file OUTPUT_FILE] [--notice_file NOTICE_FILE] [--format FORMAT] [--harvest] [--ignore_with_str IGNORE_WITH_STR]

Options

    -h, --help: Show the help message and exit.
    --input_file INPUT_FILE: Path of the input bom file.
    --output_file OUTPUT_FILE: Output file path. If not provided, stdout is used.
    --notice_file NOTICE_FILE: If provided, Lbom will generate a notices file and output its contents to the specified notice file path.
    --format FORMAT: Specify the format of the CycloneDX file (version 1.4 or 1.5).
    --harvest: If components exist in the bom without license information available, Lbom will make a request to ClearlyDefined to queue a scan of the library.
    --ignore_with_str IGNORE_WITH_STR: Do not fetch license information for components containing specific keywords, separated by commas. Example: company_name,awesome-company-pgk-name
```
## Supported Package Managers and License Information Sources
Lbom supports the following package managers and retrieves license information from the listed sources:  

    npm: npmjs
    maven: mavencentral
    git: github
    nuget: nuget
    pypi: pypi
    gem: rubygems
    pod: cocoapods
    crate: cratesio
    debsrc: debian
    deb: debian
    composer: packagist
    go: golang

## Installation

Lbom can be easily installed using pip:

```
pip install lbom

```

## Example

Here's an example of how you can use Lbom to fill license information in a CycloneDX file:

```
# Bom is generated using owasp cdxgen

cd project_dir/
cdxgen .
lbom --input_file bom.json --output_file bom_with_licenses.json --notice_file bom_notices.txt --harvest

```

### Output

If output file is not specified, bom will be printed to stdout and errors to stderr.

This command will fill missing license information in bom.json and save the result to bom_with_licenses.json. Additionally, it will queue scans for components with missing license information. Harvesting missing components can take some time.

## Contribution
If you'd like to contribute to Lbom, feel free to submit pull requests or open issues on GitHub.

## License

Lbom is licensed under the MIT License. See the LICENSE file for more information.
