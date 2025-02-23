import argparse

from .import bnc_coca_data
from ._mdx_item import WordItem, RelatedForm


def main(input_file: str, output_file: str, first_n_group: int) -> None:
    mdx_items = []
    bnc_coca_lists = bnc_coca_data.load(input_file)
    for bnc_coca_list in bnc_coca_lists:
        if bnc_coca_list[0].group > first_n_group:
            continue
        for baseword in bnc_coca_list:
            related_forms = [
                RelatedForm(wf.word, wf.freq)
                for wf in baseword.word_forms
            ]
            related_forms = sorted(related_forms, key=lambda x: x.frequency, reverse=True)
            wi = WordItem(baseword.headword, baseword.group, related_forms, baseword.total_freq)
            mdx_items.append(f"{wi.headword}\r\n{wi}")  # mdxbuilder uses \r\n as line separator
            # redirect from related forms
            for rf in related_forms:
                if rf.form == wi.headword:
                    continue
                mdx_items.append(f"{rf.form}\r\n@@@LINK={wi.headword}")
    mdx_items.sort()
    with open(output_file, "w") as f:
        f.write("\r\n</>\r\n".join(mdx_items))


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="BNC & COCA Lists mdx generator")
    argparser.add_argument("-i", "--input", help="root path to basewords data")
    argparser.add_argument("-o", "--output", help="path to output file")
    argparser.add_argument("-n", help="the first N group to include, default to 28 (max: 30)", default=28, type=int)
    args = argparser.parse_args()
    main(args.input, args.output, args.n)
