from typing import NamedTuple


class RelatedForm(NamedTuple):
    form: str
    frequency: int

    def __str__(self) -> str:
        return f'<li>{self.form}<span class="word-frequency"> ({self.frequency})</span></li>'


class FrequencyLevel(NamedTuple):
    level: str

    def __str__(self) -> str:
        return f'<span class="label freq-level-{self.level.lower()}">{self.level}</span>'


class WordItem:
    def __init__(self,
        headword: str,
        group: int,
        related_forms: list[RelatedForm],
        total_frequency: int,
        css_name: str = "the-bnc-coca-lists.css",
    ) -> None:
        self.headword = headword
        self.group = group
        self.related_forms = related_forms
        self.total_frequency = total_frequency
        self.css_name = css_name
        self.frequency_level = self._get_frequency_level(self.group)

    @staticmethod
    def _get_frequency_level(group: int) -> FrequencyLevel:
        assert group > 0, "List number must be greater than 0"
        if 0 < group < 4:
            return FrequencyLevel("HIGH")
        elif 4 <= group < 10:
            return FrequencyLevel("MID")
        return FrequencyLevel("LOW")

    def __str__(self) -> str:
        return (
            f'<link rel="stylesheet" href="{self.css_name}">'
             '<h1>'
                f'<span class="headword">{self.headword}</span>'
                f'<span class="label">{self.group}k</span>'
                f'{self.frequency_level}'
             '</h1>'
             '<h2>Related Forms</h2>'
              f'<ul>'
                f'{"".join(f'{related_form}' for related_form in self.related_forms)}'
              f'</ul>'
              f'<p class="word-frequency">Total Frequency: {self.total_frequency}</p>'
        )

    def __repr__(self) -> str:
        return (
            "WordItem(\n"
            f"    headword={self.headword},\n"
            f"    group={self.group},\n"
            f"    related_forms=([\n"
            f"{''.join(f'{form!r}\n' for form in self.related_forms)}"
            f"    ]),\n"
            f"    total_frequency={self.total_frequency}\n"
            ")"
        )
