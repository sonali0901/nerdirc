import re
import os

WORKDIR = '/tmp'

class Tex(object):
    def __init__(self, timeout=1, workdir=WORKDIR, target='math'):
        self.PREAMBLE = r'''

\documentclass{article}  
\usepackage{amsmath}
\usepackage{amsthm}
\usepackage{amssymb}
\usepackage{bm}
\newcommand{\mx}[1]{\mathbf{\bm{#1}}} % Matrix command
\newcommand{\vc}[1]{\mathbf{\bm{#1}}} % Vector command 
\newcommand{\T}{\text{T}}                % Transpose
\pagestyle{empty} 
\begin{document} 
                        '''

        self.PAGE = '$%s$ \n\\newpage \n' 
        self.ENDDOC = '\end{document}'

        self.timeout = timeout
        self.workdir = workdir
        self.target = target

    def extract(self, data):
        pointer = re.findall('(?:<x>)(?P<tex>.*?)(?:</x>)', data)

        if not pointer:
            return

        olddir = os.getcwd()
        os.chdir(self.workdir)

        self.make(pointer)
        self.build(self.target)

        os.chdir(olddir)

        size = len(pointer)

        for ind in range(size):
            yield('%s/%s-%s.gif' % (self.workdir, self.target, ind + 1))

    def make(self, latex):

        f = open('%s.tex' % self.target, 'w')
        f.write(self.PREAMBLE)

        for ind in latex:
            f.write(self.PAGE % ind)

        f.write(self.ENDDOC)
        f.close()

    def build(self, target):
        CMDX = 'timeout 2 latex -halt-on-error %s.tex' % target
        CMDY = "dvigif -T tight -x 1200 -z 9 -bg transparent \
                -o %s-%%d.gif %s.dvi" % (target, target)

        os.system(CMDX)
        os.system(CMDY) 




