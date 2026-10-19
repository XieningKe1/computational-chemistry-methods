$ENV{'TEXINPUTS'} = "$ENV{HOME}/texmf-disabled/pgfplots-4.42//:" . ($ENV{'TEXINPUTS'} // '');
$pdf_mode = 5;
$xelatex = 'xelatex -interaction=nonstopmode -halt-on-error %O %S';
$bibtex_use = 2;
