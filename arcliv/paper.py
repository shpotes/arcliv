"""
Helper class
"""

import datetime
import re
from typing import List, Tuple

class Paper(object):
    def __init__(self,
                 arxiv_id: str,
                 date: datetime.date,
                 title: str,
                 summary: str,
                 author: List[str],
                 arxiv_link: str,
                 pdf_link: str,
                 doi_link: str = None,
                 eprint: str = 'ArXiv',
                 citation_template: str = '{Author}{year}',
                 pdf_template: str = '{author}-{year}.{title}'):
        self.arxiv_id = arxiv_id
        self.date = date
        self.title = title
        self.summary = summary
        self.author = author
        self.arxiv_link = arxiv_link
        self.pdf_link = pdf_link
        self.doi_link = doi_link
        self._citation_template = citation_template
        self._pdf_template = pdf_template


    def __str__(self) -> str:
        return self.get_citation_id()

    def get_citation_id(self):
        return _interpretate_template(self, self._citation_template)

    def get_pdf_name(self):
        return _interpretate_template(self, self._pdf_template)

    def _interpretate_template(self, template: str) -> str:
        """
        TODO: Raise error
        format:
          {(a|A)utor}
          {id}
          {(y|Y)ear}
          {eprint}
          {(t|T)itle}
          {init}
        """
        
        valid = r'[\w\-\.]*({[init|[a|A]uthor|id|[y|Y]ear|eprint|[t|T]itle]})*[\w\-\.]*'

        assert template
        assert re.match(valid, template)

        template = template.replace('Tittle', 'cap_title')
        template = template.replace('Author', 'cap_author')
        template = template.replace('Year', 'decade')
        
        author_name, author_last_name = self.first_author()
        year = self.date.year

        print(author_name)
        return template.format(
            init=author_name[0].upper(),
            author=author_last_name,
            Author=capitalize(author),
            id=self.arxiv_id,
            year=year,
            decade=str(year)[-2:]
        )

    def first_author(self) -> Tuple[str, str]:
        """
        Compute first author name
        """
        first_author = self.author[0]
        *name, last_name = first_author.split()
        name = ' '.join(name)
        return name, last_name


    def get_citation(self) -> str:
        """
        TODO: check for doi
        """
        citation = '''@misc{{{bib_id},
          title = {{{title}}},
          author = {{{author}}},
          year = {{{year}}},
          eprint = {{{eprint}}},
        }},'''.format(
            bib_id=self.compute_citation_id(),
            title=self.title,
            author=self.first_author(),
            year=self.date.year,
            eprint=self.eprint
        )

        return citation
