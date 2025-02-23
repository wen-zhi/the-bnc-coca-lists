from typing import NamedTuple
import os


class WordForm(NamedTuple):
    word: str
    freq: int


class Baseword(NamedTuple):
    group: int
    headword: str
    total_freq: int
    word_forms: list[WordForm]


def load(root: str) -> list[list[Baseword]]:
    bnc_coca_lists: list[list[Baseword]] = []
    fprefix = "basewrd"
    for fname in os.listdir(root):
        if not fname.startswith(fprefix):
            continue
        group = int(fname.lstrip(fprefix).rstrip('.txt'))
        if group > 30:  # drop the 5 additional lists (31-35)
            continue
        bnc_coca_list: list[Baseword] = []
        fpath = os.path.join(root, fname)
        with open(fpath, "r") as f:
            for i, line in enumerate(f, start=1):
                line = line.rstrip()
                if not line:
                    continue
                try:
                    word, freq = line.lstrip().split()
                    word, freq = word.lower(), int(freq)
                except ValueError:
                    raise Exception(f"line {i} of file `{fpath}` is invalid, please fix it first.")
                if not line.startswith('\t'):
                    bnc_coca_list.append(
                        Baseword(
                            group=group,
                            headword=word,
                            total_freq=freq,
                            word_forms=[]
                        )
                    )
                else:
                    bnc_coca_list[-1].word_forms.append(WordForm(word, freq))
        # add headword to each word_forms
        for _, headword, total_freq, word_forms in bnc_coca_list:
            word_forms.append(WordForm(headword, total_freq - sum(wf.freq for wf in word_forms)))
        bnc_coca_lists.append(bnc_coca_list)
    return bnc_coca_lists
