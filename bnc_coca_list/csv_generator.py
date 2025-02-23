import argparse
import csv

from .import bnc_coca_data


def main(input_file: str, output_file: str, first_n_group: int) -> None:
    bnc_coca_lists = bnc_coca_data.load(input_file)
    bnc_coca_lists.sort(key=lambda x: x[0].group)
    with open(output_file, 'w+', newline='') as fout:
        writer = csv.writer(fout)
        writer.writerow(['group', 'headword', 'total_freq', 'word_forms'])
        for bnc_coca_list in bnc_coca_lists[:first_n_group]:
            bnc_coca_list.sort(key=lambda x: x.total_freq, reverse=True)
            for baseword in bnc_coca_list:
                baseword.word_forms.sort(key=lambda x: x.freq, reverse=True)
                writer.writerow([
                    f'{baseword.group}k',
                    baseword.headword,
                    baseword.total_freq,
                    ', '.join([f'{wr.word} ({wr.freq})' for wr in baseword.word_forms])
                ])


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="BNC & COCA Lists csv generator")
    argparser.add_argument("-i", "--input", help="root path to basewords data")
    argparser.add_argument("-o", "--output", help="path to output file")
    argparser.add_argument("-n", help="the first N group to include, default to 9 (max: 30)", default=9, type=int)
    args = argparser.parse_args()
    main(args.input, args.output, args.n)
