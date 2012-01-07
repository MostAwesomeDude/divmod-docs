#!/usr/bin/env python
"""Roughly convert from Trac Wiki syntax to RestructuredText"""

from pprint import pprint as pp
import re
import sys


title_patterns = [r"^"+ ("=" * i) + " (.*) " + ("=" * i)
                  for i in range(1, 10)]
re_titles = [re.compile(p, re.MULTILINE) for p in title_patterns]

re_inlines = [
    (re.compile(reg), replace_by)
    for reg, replace_by in [
        (r"'''(.*?)'''", r"*\1*"),
        (r"''(.*?)''", r"**\1**"),
    ]]

re_link = re.compile(r'\[([\S]+) ([^\]]+)\]')
re_code_block = re.compile(r'{{{(.*?)}}}', re.DOTALL)
re_code_highlight = re.compile(r'.*#!(\w+)')


def run(path):
    with open(path) as fr, open("%s.rst" % path.replace('.txt', ''), "w") as fw:
        process_file(fr, fw)

def process_file(r, w):
    text = r.read()

    text = replace_titles(text)
    text = replace_inlines(text)
    text = replace_links(text)
    text = replace_code_block(text)

    w.write(text)


def replace_inlines(text):
    """Replace inline syntax"""
    for r, repl in re_inlines:
        text = r.sub(repl, text)
    return text


def replace_code_block(text):
    def repl(match):
        m = match.group(1)

        if "\n" not in m:
            return "``%s``" % m

        if m.startswith(' '):
            # Don't indent if it already looks indented
            code = m
        else:
            code = "    %s" % "\n    ".join(
                l for l in m.split("\n"))

        code = re_code_highlight.sub(r'\n.. code-block:: \1\n', code)

        if "::" not in code:
            # Previous regex didn't apply, manually set code block
            code = "\n::\n%s\n\n" % code

        return code

    return re_code_block.sub(repl, text)


def replace_links(text):
    def repl(match):
        link, text = match.groups()

        if link.startswith('wiki:'):
            link = link[len('wiki:'):]

            if link.startswith('Divmod'):
                link = link[len('Divmod'):]

            def split_caps(m):
                s = m.group(1)
                return "-" + s.lower()

            link = link.replace('/', '')
            # Split the Wiki name on capitalized characters
            r = re.sub(r"([%s])" % ("".join(chr(c) for c in range(65, 91))),
                       split_caps,
                       link)

            return ":doc:`%s`" % r.lstrip('-')

        # Those are Wiki links but inserted with the full URL in the source
        # Try to be smart (but it's difficult -_- )
        urls_replacement = [
            ('http://divmod.org/trac/wiki/DivmodCombinator',
             ':doc:`products/combinator`'),
            ('http://divmod.org/trac/wiki/DivmodNevow/Athena',
             ':doc:`products/nevow/athena`'),
            ('http://divmod.org/trac/wiki/DivmodNevow/AthenaTesting',
             ':doc:`products/nevow/athena-testing`'),
            ('http://divmod.org/trac/wiki/DivmodNevow/Deployment/ReverseProxy',
             ':doc:`products/nevow/reverse-proxy`'),
            ('http://divmod.org/trac/wiki/PeopleUsingDivmod',
             ':doc:`people-using-divmod`'),
            ('http://divmod.org/trac/wiki/SoftwareReleases/Nevow',
             ':doc:`software-releases-nevow`'),
            ('http://divmod.org/trac/wiki/UsingVertex',
             ':doc:`using-vertex`'),
        ]

        for url, url_replace in urls_replacement:
            if link == url:
                return url_replace

        else:
            # It looks like a normal, extern link, just process it as it.
            return "`%s <%s>`_" % (text, link)

    return re_link.sub(repl, text)


def replace_titles(text):
    for i, (r, motif) in enumerate(
        zip(re_titles, ["=", "=", "'", '"', "~", "_", "-"])):
        def repl(match):
            matched = match.group(1)
            if i == 0:
                repl = "%s\n" % ("=" * len(matched))
            else:
                repl = "\n\n"

            repl += "%s\n%s\n" % (
                matched,
                "=" * len(matched)
            )

            return repl
        text = r.sub(repl, text)

    return text


if __name__ == '__main__':
    for f in sys.argv[1:]:
        run(f)
