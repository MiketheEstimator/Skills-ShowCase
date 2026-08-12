---
name: SKILL_DOC_LATEX_PRECISION
description: "High-fidelity mathematical and academic typesetting requiring strict syntax validation. Use when producing .tex files for academic papers, technical reports, theses, equations, or any document requiring precise mathematical notation. Triggers: 'LaTeX', '.tex file', 'academic paper', 'typeset equations', 'thesis', 'arXiv submission', 'IEEE format', 'APA format', 'BibTeX'."
---

# SKILL_DOC_LATEX_PRECISION — LaTeX Typesetting Skill

## Quick Reference

| Task | Section |
|------|---------|
| Document class templates | [Document Templates](#document-templates) |
| Mathematics typesetting | [Mathematics](#mathematics) |
| Tables & figures | [Tables & Figures](#tables--figures) |
| Bibliography (BibTeX/BibLaTeX) | [Bibliography](#bibliography) |
| Compilation pipeline | [Compilation Pipeline](#compilation-pipeline) |
| Validation & QA | [Validation & QA](#validation--qa) |

---

## Document Templates

### Minimal Article

```latex
\documentclass[12pt, a4paper]{article}

% Encoding & language
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[english]{babel}

% Core packages
\usepackage{amsmath, amssymb, amsthm}   % mathematics
\usepackage{graphicx}                    % figures
\usepackage{booktabs}                    % professional tables
\usepackage{hyperref}                    % clickable links
\usepackage{geometry}                    % page layout
\usepackage{microtype}                   % typography refinement

\geometry{margin=2.5cm}

% Metadata
\title{Document Title}
\author{Author Name \\ \small Institution \\ \small \texttt{email@domain.com}}
\date{\today}

\begin{document}

\maketitle
\tableofcontents
\newpage

\begin{abstract}
Abstract text here.
\end{abstract}

\section{Introduction}
\label{sec:intro}

Body text. Reference a section: see Section~\ref{sec:method}.

\section{Method}
\label{sec:method}

Content here.

\section{Conclusion}

Conclusion here.

\bibliographystyle{plain}
\bibliography{references}

\end{document}
```

### IEEE Conference Paper

```latex
\documentclass[conference]{IEEEtran}
\usepackage{cite}
\usepackage{amsmath, amssymb}
\usepackage{graphicx}
\usepackage{url}

\begin{document}

\title{Paper Title}

\author{
  \IEEEauthorblockN{First Author}
  \IEEEauthorblockA{Department\\Institution\\Email}
  \and
  \IEEEauthorblockN{Second Author}
  \IEEEauthorblockA{Department\\Institution\\Email}
}

\maketitle

\begin{abstract}
Abstract text (150 words max for IEEE).
\end{abstract}

\begin{IEEEkeywords}
keyword1, keyword2, keyword3
\end{IEEEkeywords}

\section{Introduction}
Text with citation~\cite{author2024}.

\bibliographystyle{IEEEtran}
\bibliography{references}

\end{document}
```

### Thesis / Dissertation

```latex
\documentclass[12pt, a4paper, twoside]{book}

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath, amssymb, amsthm}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage[hidelinks]{hyperref}
\usepackage{geometry}
\usepackage{fancyhdr}
\usepackage{setspace}
\usepackage[backend=biber, style=authoryear]{biblatex}

\geometry{left=4cm, right=2.5cm, top=3cm, bottom=3cm}
\doublespacing
\addbibresource{references.bib}

\begin{document}

\frontmatter
\include{chapters/titlepage}
\include{chapters/abstract}
\tableofcontents
\listoffigures
\listoftables

\mainmatter
\include{chapters/01-introduction}
\include{chapters/02-literature}
\include{chapters/03-methodology}
\include{chapters/04-results}
\include{chapters/05-conclusion}

\backmatter
\printbibliography

\end{document}
```

---

## Mathematics

### Inline vs Display

```latex
% Inline math — within text
The equation $E = mc^2$ defines mass-energy equivalence.

% Display math — centred, numbered
\begin{equation}
  \label{eq:euler}
  e^{i\pi} + 1 = 0
\end{equation}

% Display math — unnumbered
\[
  \sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}
\]
```

### Common Mathematical Constructs

```latex
% Fractions
\frac{numerator}{denominator}
\dfrac{a}{b}   % display-size fraction inline

% Superscript / subscript
x^{2}          % superscript
x_{i}          % subscript
x^{2}_{i}      % both

% Greek letters
\alpha \beta \gamma \delta \epsilon \pi \sigma \omega
\Alpha \Beta \Gamma \Delta \Sigma \Omega

% Operators
\sum_{i=1}^{n}
\prod_{i=1}^{n}
\int_{0}^{\infty}
\iint \iiint \oint
\lim_{x \to \infty}
\nabla \partial

% Roots
\sqrt{x}
\sqrt[n]{x}

% Matrices
\begin{pmatrix} a & b \\ c & d \end{pmatrix}   % round brackets
\begin{bmatrix} a & b \\ c & d \end{bmatrix}   % square brackets
\begin{vmatrix} a & b \\ c & d \end{vmatrix}   % determinant

% Aligned equations (amsmath)
\begin{align}
  f(x) &= x^2 + 2x + 1 \\
       &= (x + 1)^2
\end{align}

% Cases
f(x) = \begin{cases}
  x^2  & \text{if } x \geq 0 \\
  -x^2 & \text{if } x < 0
\end{cases}

% Text within math
\text{for all } x \in \mathbb{R}

% Number sets
\mathbb{R} \mathbb{Z} \mathbb{N} \mathbb{Q} \mathbb{C}

% Norms / brackets
\left\| x \right\|          % auto-size double bar
\left( \frac{a}{b} \right)  % auto-size parentheses
\left[ x \right]            % auto-size brackets
```

### Theorem Environments

```latex
% In preamble (requires amsthm)
\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{definition}{Definition}[section]
\newtheorem{remark}{Remark}

% In document
\begin{theorem}[Optional name]
\label{thm:main}
Statement of theorem.
\end{theorem}

\begin{proof}
Proof goes here. \qed
\end{proof}

\begin{definition}
A \emph{widget} is defined as...
\end{definition}
```

---

## Tables & Figures

### Professional Table (booktabs)

```latex
\usepackage{booktabs}   % in preamble

\begin{table}[htbp]
  \centering
  \caption{Table caption above.}
  \label{tab:results}
  \begin{tabular}{lrr}
    \toprule
    Method    & Accuracy (\%) & Runtime (s) \\
    \midrule
    Baseline  & 82.3          & 1.2         \\
    Proposed  & \textbf{91.7} & 2.8         \\
    \bottomrule
  \end{tabular}
\end{table}
```

Column specifiers:
```
l  — left aligned
r  — right aligned
c  — centred
p{3cm} — fixed width, text wraps
```

### Figure

```latex
\usepackage{graphicx}   % in preamble

\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\linewidth]{figures/diagram.pdf}
  \caption{Figure caption below.}
  \label{fig:diagram}
\end{figure}

% Two figures side by side
\begin{figure}[htbp]
  \centering
  \begin{minipage}{0.48\linewidth}
    \includegraphics[width=\linewidth]{fig1.pdf}
    \caption{First figure.}
    \label{fig:one}
  \end{minipage}
  \hfill
  \begin{minipage}{0.48\linewidth}
    \includegraphics[width=\linewidth]{fig2.pdf}
    \caption{Second figure.}
    \label{fig:two}
  \end{minipage}
\end{figure}
```

Figure placement specifiers:
```
h — here (approximately)
t — top of page
b — bottom of page
p — separate page for floats
! — override LaTeX judgement
H — exactly here (requires float package)
```

### Cross-References

```latex
% Label everything
\label{sec:intro}     % section
\label{eq:main}       % equation
\label{fig:result}    % figure
\label{tab:data}      % table

% Reference
see Section~\ref{sec:intro}
Equation~\eqref{eq:main}    % eqref adds parentheses: (1)
Figure~\ref{fig:result}
Table~\ref{tab:data}

% Use ~ (non-breaking space) before \ref always
```

---

## Bibliography

### BibTeX (.bib file format)

```bibtex
@article{smith2024deep,
  author  = {Smith, John and Jones, Alice},
  title   = {Deep Learning for Construction},
  journal = {Journal of Computing in Civil Engineering},
  year    = {2024},
  volume  = {38},
  number  = {2},
  pages   = {04024001},
  doi     = {10.1061/JCCEE5.CPENG-5678}
}

@inproceedings{lee2023bim,
  author    = {Lee, David},
  title     = {BIM Integration Challenges},
  booktitle = {Proceedings of the International Conference on Construction},
  year      = {2023},
  pages     = {123--135},
  publisher = {ASCE}
}

@book{knuth1984texbook,
  author    = {Knuth, Donald E.},
  title     = {The \TeX book},
  publisher = {Addison-Wesley},
  year      = {1984}
}

@misc{github2024repo,
  author  = {Author, Name},
  title   = {Repository Title},
  year    = {2024},
  url     = {https://github.com/org/repo},
  note    = {Accessed: 2024-03-15}
}
```

### BibLaTeX (modern, preferred)

```latex
% Preamble
\usepackage[backend=biber, style=authoryear, sorting=nyt]{biblatex}
\addbibresource{references.bib}

% In document body
\cite{smith2024deep}           % (Smith, 2024)
\textcite{smith2024deep}       % Smith (2024)
\parencite{smith2024deep}      % (Smith, 2024) — same as \cite for authoryear
\footcite{smith2024deep}       % footnote citation

% At end of document
\printbibliography

% Compile with biber (not bibtex)
```

Common styles:
```
authoryear   — APA-style (author, year)
numeric      — [1], [2], [3]
ieee         — IEEE numeric
apa          — strict APA 7th
chicago-notes — Chicago footnote
```

---

## Compilation Pipeline

### Standard (pdflatex + bibtex)

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex    # run twice to resolve references
```

### Modern (lualatex/xelatex + biber)

```bash
lualatex main.tex    # or xelatex main.tex
biber main
lualatex main.tex
lualatex main.tex
```

### Automated with latexmk (recommended)

```bash
# Install
pip install latexmk   # or: sudo apt install latexmk

# Compile (auto-detects bibliography tool)
latexmk -pdf main.tex

# Compile with lualatex
latexmk -lualatex main.tex

# Continuous rebuild on save
latexmk -pdf -pvc main.tex

# Clean auxiliary files
latexmk -c        # clean intermediate files
latexmk -C        # clean everything including PDF
```

### Auxiliary Files to .gitignore

```gitignore
# LaTeX auxiliary files
*.aux
*.bbl
*.bcf
*.blg
*.fdb_latexmk
*.fls
*.lof
*.log
*.lot
*.out
*.run.xml
*.synctex.gz
*.toc
*.xdv
# Keep: *.tex, *.bib, *.pdf (if distributing), figures/
```

### Docker-based Compilation (reproducible)

```dockerfile
FROM texlive/texlive:latest

WORKDIR /doc
COPY . .
RUN latexmk -pdf main.tex
```

```bash
docker build -t latex-doc .
docker run --rm -v $(pwd)/output:/doc/output latex-doc \
  cp main.pdf output/
```

---

## Validation & QA

### Error Log Parsing

```bash
# After compilation, check log for errors and warnings
grep -E "^!" main.log           # fatal errors
grep -E "Warning:" main.log     # warnings
grep -E "Overfull|Underfull" main.log  # layout issues
```

### Common Error Messages & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `! Undefined control sequence` | Typo in command or missing package | Check spelling; add required `\usepackage` |
| `! Missing $ inserted` | Math outside math mode | Wrap in `$...$` or `\(...\)` |
| `! File 'package.sty' not found` | Package not installed | Run `tlmgr install package` |
| `Overfull \hbox` | Text/equation too wide | Use `\allowbreak`, adjust wording, or `\sloppy` |
| `Citation 'key' undefined` | Missing .bib entry or compile order | Check .bib file; re-run full compile sequence |
| `Label 'X' multiply defined` | Duplicate `\label` | Make all labels unique |
| `There were undefined references` | Need another compile pass | Run `pdflatex` again |

### Python Log Analyser

```python
import re

def parse_latex_log(log_path: str):
    with open(log_path, 'r', errors='ignore') as f:
        content = f.read()

    errors   = re.findall(r'^!.*', content, re.MULTILINE)
    warnings = re.findall(r'.*Warning:.*', content)
    overfull = re.findall(r'Overfull \\hbox.*', content)
    undef    = re.findall(r'.*undefined.*', content, re.IGNORECASE)

    print(f"ERRORS ({len(errors)}):")
    for e in errors: print(f"  {e}")

    print(f"\nWARNINGS ({len(warnings)}):")
    for w in warnings[:10]: print(f"  {w}")

    print(f"\nOVERFULL HBOX ({len(overfull)}): {len(overfull)} instances")
    print(f"UNDEFINED REFS ({len(undef)}): {len(undef)} instances")

parse_latex_log('main.log')
```

### QA Checklist

- [ ] Document compiles without fatal errors (`!` lines in log)
- [ ] Zero undefined references (`\ref`, `\cite` all resolve)
- [ ] Zero undefined citations
- [ ] No multiply-defined labels
- [ ] Overfull/underfull hbox count is acceptable
- [ ] Table of contents is correct
- [ ] Figures and tables appear near their reference points
- [ ] Page numbers are correct (especially with `\frontmatter`/`\mainmatter`)
- [ ] PDF bookmarks/hyperlinks work (hyperref)
- [ ] Bibliography sorted and formatted correctly

### QA Loop

1. Compile full sequence (latexmk or 3-pass manual)
2. Parse log — fix all `!` errors
3. Fix undefined references
4. Check overfull hboxes — fix where severe (>10pt)
5. Visual review of PDF — spot-check equations, tables, figures
6. **Do not submit until zero fatal errors and zero undefined references**

---

## Dependencies

```bash
# Full TeX distribution
# Linux
sudo apt install texlive-full      # complete (4GB)
sudo apt install texlive-latex-extra texlive-science  # targeted

# macOS
brew install --cask mactex         # full MacTeX

# Windows
# Download MiKTeX from https://miktex.org or
# TeX Live from https://tug.org/texlive/

# Build tool
sudo apt install latexmk

# Package manager (TeX Live)
tlmgr install package-name

# Python log parsing — stdlib only (no install needed)
import re
```
> [!NOTE]   
>**you cannot get rendered display math inside a fenced code block**. A fenced code block is for showing literal source text, while display math is a separate Markdown/MathJax render pass. GitHub’s docs treat code blocks and mathematical expressions as different formatting features, and GitHub math rendering uses MathJax rather than code-block syntax. ([GitHub Docs][1])
>
So the unambiguous rule to tell any LLM is:

**Use a fenced code block only to show the raw Markdown/LaTeX source.
Use a standalone LaTeX math block outside the code fence to render the formal display equation.** ([GitHub Docs][1])

Use this wording:

```text
Render all formal equations as LaTeX display math blocks, not inline math.
When showing the source, place the raw Markdown/LaTeX in a separate fenced code block labeled markdown.
Never put rendered math inside a code fence.
For explanatory structure, use this order:
1. Title
2. Rendered display equation
3. Fenced markdown source
4. Symbol key
5. Structural reading
```

Here is the **universal, low-ambiguity prompt formula**:

```text
For all mathematical expressions, use DISPLAY MATH, not inline math.

REQUIRED FORMAT:
- First, render the equation as a standalone LaTeX display block.
- Second, provide the exact raw Markdown source in a separate fenced `markdown` code block.
- Third, add an annotated symbol key below it.
- Fourth, add a short structural reading of the equation.

DO NOT:
- Do not leave important equations inline unless I explicitly ask.
- Do not put rendered math inside a code fence.
- Do not substitute plain-text math when LaTeX display math can be used.
```

Example of the pattern you want:

Rendered:

$$ 
i\hbar \frac{\partial \Psi}{\partial t} = -\frac{\hbar^2}{2m}\frac{\partial^2 \Psi}{\partial x^2} + V(x)\Psi 
$$

Source:
```markdown
\[ i\hbar \frac{\partial \Psi}{\partial t} = -\frac{\hbar^2}{2m}\frac{\partial^2 \Psi}{\partial x^2} + V(x)\Psi \]


Source:

```markdown
\[
i\hbar \frac{\partial \Psi}{\partial t}
=
-\frac{\hbar^2}{2m}\frac{\partial^2 \Psi}{\partial x^2}
+
V(x)\Psi
\]
```

Symbol key:

* ( i ) = imaginary unit
* ( \hbar ) = reduced Planck constant
* ( \Psi ) = wavefunction
* ( V(x) ) = potential energy

Structural reading:

* Left side = time evolution
* Right side, first term = kinetic/spatial curvature term
* Right side, second term = potential term

For maximum cross-platform reliability, prefer `\[ ... \]` for display math rather than `$$ ... $$`; Overleaf specifically recommends `\[ ... \]` instead of `$$ ... $$` in LaTeX contexts. ([Overleaf][2])
> [!NOTE]  
> **Troubleshooting: GitHub Preview vs. Native LaTeX**
> If your equations are failing to render in the GitHub preview, check your delimiters. GitHub Flavored Markdown (GFM) requires `$$...$$` to trigger a multi-line display math block. If you use standard LaTeX `\[ ... \]` outside of a code block, GitHub's markdown parser will strip the backslashes and break the render.
> 
> **The Workaround:** When building skill sheets in `.md`, use `$$` for the visual preview section so it renders correctly on GitHub, but strictly instruct the LLM to output the gold-standard `\[ ... \]` inside its fenced code blocks for the final `.tex` artifact.


GitHub Flavored Markdown (GFM) includes a specific set of five "Alert" callouts (also known as admonitions) that natively render with distinct colors and icons in the repository preview. 

([https://github.blog/changelog/2023-12-14-new-markdown-extension-alerts-provide-distinctive-styling-for-significant-content/])

> [!NOTE]  
> Useful information that users should know, even when skimming.

> [!TIP]
> Helpful advice for doing things better or more easily.

> [!IMPORTANT]  
> Key information users need to know to achieve their goal.

> [!WARNING]  
> Urgent info that needs immediate user attention to avoid problems.

> [!CAUTION]
> Advises about risks or negative outcomes of certain actions.

## So the shortest **definitive instruction** to reuse is:

```text
Use LaTeX display math for formal equations.
Render the equation as a standalone math block using \[ ... \].
Then show the raw source separately in a fenced markdown block.
```

And if you want the elegant format every time, use this stronger house style:

```text
HOUSE STYLE FOR FORMAL EQUATIONS:
- All important equations must be presented in rendered LaTeX display math.
- Immediately below each equation, include a fenced `markdown` source block containing the exact raw syntax.
- Then include:
  - Symbol key
  - Structural reading
  - Optional annotated diagram description
- Prefer \[ ... \] over $$ ... $$.
```

The key distinction is:

* **display math block** = rendered formal equation
* **fenced code block** = literal source only

They are adjacent companions, not the same object. ([GitHub Docs][1])

A clean name for what you want is:

**Rendered Display Math + Raw Markdown Source**

Or more elegantly:

**Formal Equation Block Pattern**

I can also give you a one-paragraph master instruction you can paste into any LLM as your standing math-format preference.

[1]: https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions?utm_source=chatgpt.com "Writing mathematical expressions"
[2]: https://www.overleaf.com/learn/latex/Errors/Display_math_should_end_with_%24%24?utm_source=chatgpt.com "Display math should end with"
[3]: https://github.blog/changelog/2023-12-14-new-markdown-extension-alerts-provide-distinctive-styling-for-significant-content/
