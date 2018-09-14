# Project configs
BRIEF  := report

TARGETS := $(BRIEF).pdf

# Compiler configs
ifndef LATEX
	LATEX  := xelatex
endif
BIBTEX := bibtex

# Etc.
OBJS   := $(wildcard **/*.tex) $(wildcard *.tex)

# Rules
.PHONY: clean clean-pdf all

all: $(TARGETS)

$(BRIEF).pdf:  $(BRIEF).tex

%.pdf: %.tex
	$(LATEX) --shell-escape $(basename $@)
ifdef BIBREF
	$(BIBTEX) $(basename $@)
	$(LATEX) --shell-escape $(basename $@)
	$(LATEX) --shell-escape $(basename $@)
endif
	$(LATEX) --shell-escape $(basename $@)

clean:
	rm -f *.{aux,bbl,blg,log,nav,snm,out,toc}
	rm -rf _minted-*

clean-pdf:
	rm $(BRIEF).pdf
