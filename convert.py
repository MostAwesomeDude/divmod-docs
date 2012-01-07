#!/usr/bin/env python

from pprint import pprint as pp
import re
import sys


patterns = [r"^"+ ("=" * i) + " (.*) " + ("=" * i)
            for i in range(1, 10)]
re_titles = [re.compile(p, re.MULTILINE) for p in patterns]

re_inlines = [
    (re.compile(r), repl)
    for r, repl in [
        (r"'''(.*?)'''", r"*\1*"),
        (r"''(.*?)''", r"**\1**"),
    ]]

re_link = re.compile(r'\[([\S]+) ([^\]]+)\]')
re_code_block = re.compile(r'{{{(.*?)}}}', re.DOTALL)

re_code_highlight = re.compile(r'.*#!(\w+)')

def run(path):
    with open(path) as fr, open("%s.rst" % path.replace('.txt', ''), "w") as fw:
        process_fps(fr, fw)


def process_fps(r, w):
    text = r.read()

    text = replace_weird_trac_directives(text)
    text = replace_titles(text)
    text = replace_inlines(text)
    text = replace_links(text)
    text = replace_code_block(text)

    w.write(text)
    #print text


def replace_weird_trac_directives(text):
    return re.sub(r"\[\[.*?\]\]", "", text)


def replace_inlines(text):
    for r, repl in re_inlines:
        text = r.sub(repl, text)
    return text


def replace_code_block(text):
    def repl(match):
        m = match.group(1)

        if "\n" not in m:
            return "``%s``" % m

        if m.startswith(' '):
            indent = m
        else:
            indent = "    %s" % "\n    ".join(
                l for l in m.split("\n"))

        #code = "\n::\n%s\n\n" % indent
        code = indent
        code = re_code_highlight.sub(r'\n.. code-block:: \1\n', code)

        if "::" not in code:
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
            r = re.sub(r"([%s])" % ("".join(chr(c) for c in range(65, 91))),
                       split_caps,
                       link)

            return ":doc:`%s`" % r.lstrip('-')

        links_replacement = [
            ('http://divmod.org/trac/wiki/DivmodCombinator',
             ':ref:`combinator`'),
            ('http://divmod.org/trac/wiki/DivmodNevow/Athena',
             ':ref:`athena`'),
            ('http://divmod.org/trac/wiki/DivmodNevow/AthenaTesting',
             ':ref:`athena-testing`'),
            ('http://divmod.org/trac/wiki/DivmodNevow/Deployment/ReverseProxy',
             ':ref:`nevow-deployement-reverse-proxy`'),
            ('http://divmod.org/trac/wiki/PeopleUsingDivmod',
             ':ref:`people-using-divmod`'),
            ('http://divmod.org/trac/wiki/SoftwareReleases/Nevow',
             ':ref:`software-releases-nevow`'),
            ('http://divmod.org/trac/wiki/UsingVertex',
             ':ref:`using-vertex`'),
        ]

        for l, r in links_replacement:
            if link == l:
                return r

        else:
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
