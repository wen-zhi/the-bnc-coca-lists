import argparse
import csv
import re

from .worditem import WordItem, RelatedForm


def main(input_file: str, output_file: str) -> None:
    mdx_items = []
    with open(input_file, "r") as f:
        reader = csv.reader(f)
        _ = next(reader)  # skip header
        for row in reader:
            list_number, headword, related_forms, total_freq = [value.strip() for value in row]
            related_forms = [
                RelatedForm(m[0], int(m[1]))
                for m in re.findall(r"(\w+)\s+\((\d+)\)", related_forms)
            ]
            related_forms = sorted(related_forms, key=lambda x: x.frequency, reverse=True)
            wi = WordItem(headword, list_number, related_forms, int(total_freq))
            mdx_items.append(f"{wi.headword}\r\n{wi}")  # mdxbuilder uses \r\n as line separator
            # redirect from related forms
            for rf in related_forms:
                if rf.form == wi.headword:
                    continue
                mdx_items.append(f"{rf.form}\r\n@@@LINK={wi.headword}")
            
    with open(output_file, "w") as f:
        f.write("\r\n</>\r\n".join(mdx_items))


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="BNC & COCA Lists mdx generator")
    argparser.add_argument("--input", help="Input file")
    argparser.add_argument("--output", help="Output file")
    args = argparser.parse_args()
    main(args.input, args.output)
