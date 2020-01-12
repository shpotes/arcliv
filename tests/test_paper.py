import datetime
from arcliv import paper

def test_first_author():
    test1 = paper.Paper(arxiv_id=None,
                        date=None,
                        title=None,
                        summary=None,
                        author=['x xxx', 'y yyy'],
                        arxiv_link=None,
                        pdf_link=None)

    assert test1.first_author() == ('x', 'xxx')

    test2 = paper.Paper(arxiv_id=None,
                        date=None,
                        title=None,
                        summary=None,
                        author=['abc cds xxx'],
                        arxiv_link=None,
                        pdf_link=None)

    assert test2.first_author() == ('abc cds', 'xxx')

    test2 = paper.Paper(arxiv_id=None,
                        date=None,
                        title=None,
                        summary=None,
                        author=['abc cds xxx'],
                        arxiv_link=None,
                        pdf_link=None)

    assert test2.first_author() == ('abc cds', 'xxx')

def test_interpretate_template():
    test1 = paper.Paper(arxiv_id='1234.1234',
                        date=datetime.date(2000, 1, 1),
                        title='xxx xxx',
                        summary='---',
                        author=['zzz yyy'],
                        arxiv_link='',
                        pdf_link='')

    arxiv = 'ArXiv:{id}'
    pdf = '{author}-{year}.{title}'
    citation = '{init}.{Author}-{year}'
    caps = '{Title}"{Year}'

    assert test1._interpretate_template(arxiv) == 'ArXiv:1234.1234'
    assert test1._interpretate_template(pdf) == 'yyy-2000.xxx-xxx'
    assert test1._interpretate_template(citation) == 'Z.yyy-2000'
    assert test1._interpretate_template(caps) == 'xxx-xxx"00'
