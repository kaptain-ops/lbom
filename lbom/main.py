import argparse
import json
from lbom.license.LicenseResolver import LicenseResolver
from lbom.bom.BomHandler import BomHandler
from lbom.bom.BomHandlerCyclonedx import BomHandlerCyclonedx
from lbom.clearly_defined.ClearlyDefinedProviders import ClearlyDefinedProviders
import os.path
import sys


def main():
    parser = argparse.ArgumentParser(description="Lbom fills missing licenses to components on cyclonedx files. Version 0.5")
    parser.add_argument("--input_file", required=True, help="Path of input bom file")
    parser.add_argument(
        "--output_file",
        required=False,
        help="Output file path. If not provided, stdout is used",
        default=None,
    )
    parser.add_argument(
        "--notice_file",
        required=False,
        help="If provided, will generate notices file and output contents of the file to notice_file path",
        default=None,
    )
    parser.add_argument(
        "--format",
        required=False,
        help="values: cyclonedx (cyclonedx version 1.4 or 1.5)",
        default="cyclonedx",
    )
    parser.add_argument(
        "--harvest",
        required=False,
        help="If components exists in bom that do not have license information available, make request to clearlydefined to queue scan of library",
        action="store_true",
    )
    parser.add_argument(
        "--ignore_with_str",
        required=False,
        help="Do not try to fetch license information to components having given keywords separated by comma. Example value: mycompany,awesome-internal-util-package",
        default=None,
        type=str,
    )
    args = parser.parse_args()

    input_file: str = args.input_file
    output_file: str = args.output_file
    notice_file: str = args.notice_file
    harvest: bool = args.harvest
    ignore_with_str: str = args.ignore_with_str
    format: str = args.format

    provider: ClearlyDefinedProviders = ClearlyDefinedProviders()

    if not os.path.isfile(input_file):
        print("Could not find input file", file=sys.stderr)
        exit(-1)

    with open(input_file, "r") as file:
        bom_handler: BomHandler
        match format:
            case "cyclonedx":
                bom_handler = BomHandlerCyclonedx(json.load(file), provider)
            case _:
                print("Invalid input format provider", file=sys.stderr)
                exit(-1)

        resolver: LicenseResolver = LicenseResolver(bom_handler)
        lbom: dict = resolver.download_licenses(ignore_with_str, harvest)

        output_contents = json.dumps(lbom, indent=2)
        if output_file:
            with open(output_file, "w") as bom_file_fp:
                bom_file_fp.write(output_contents)
        else:
            print(output_contents)

        if notice_file:
            notice_content: str = resolver.download_notices(ignore_with_str)
            with open(notice_file, "w") as notice_file_fp:
                notice_file_fp.write(notice_content)


if __name__ == "__main__":
    main()
