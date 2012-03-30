if v:lang =~ "utf8$" || v:lang =~ "UTF-8$"
   set fileencodings=utf-8,latin1
endif

set nocompatible	" Use Vim defaults (much better!)
set bs=indent,eol,start		" allow backspacing over everything in insert mode
set ai			" always set autoindenting on
"set backup		" keep a backup file
set viminfo='20,\"50	" read/write a .viminfo file, don't store more
			" than 50 lines of registers
set history=50		" keep 50 lines of command line history
set ruler		" show the cursor position all the time

" Only do this part when compiled with support for autocommands
if has("autocmd")
  augroup redhat
	" In text files, always limit the width of text to 78 characters
	autocmd BufRead *.txt set tw=78
	" When editing a file, always jump to the last cursor position
	autocmd BufReadPost *
	\ if line("'\"") > 0 && line ("'\"") <= line("$") |
	\	exe "normal! g'\"" |
	\ endif
  augroup END
endif

if has("cscope") && filereadable("/usr/bin/cscope")
   set csprg=/usr/bin/cscope
   set csto=0
   set cst
   set nocsverb
   " add any database in current directory
   if filereadable("cscope.out")
	  cs add cscope.out
   " else add database pointed to by environment
   elseif $CSCOPE_DB != ""
	  cs add $CSCOPE_DB
   endif
   set csverb
endif

" Switch syntax highlighting on, when the terminal has colors
" Also switch on highlighting the last used search pattern.
"if &t_Co > 2 || has("gui_running")
"  syntax on
"  set hlsearch
"endif

"if &term=="xterm"
"	  set t_Co=8
"	  set t_Sb=[4%dm
"	  set t_Sf=[3%dm
"endif

set shortmess=filnxtToOI 
set noea
set scs
set nu
set dict=/home/oznahum/.vim/allwords
set expandtab
set autoindent
set history=50
set ruler
set showcmd
set incsearch
set tabstop=4
"set sw=4
set scrolloff=6
" use 4 spaces for tabs
set tabstop=4 softtabstop=4 shiftwidth=4

" display indentation guides
"set list listchars=tab:\u2758-,trail:�,extends:�,precedes:�,nbsp:�

" convert spaces to tabs when reading file
autocmd! bufreadpost *.py set noexpandtab | retab! 4

" convert tabs to spaces before writing file
autocmd! bufwritepre *.py set expandtab | retab! 4

"set smartindent
"set tabstop=4
"set shiftwidth=4
"set expandtab
" make backspace work like most other apps
" even with ssh !

"highlight Comment ctermfg=Blue


""folding settings
"set foldmethod=indent	"fold based on indent
"set foldnestmax=10		"deepest fold is 10 levels
"set nofoldenable		"dont fold by default
"set foldlevel=10			"this is just what i use
"
""Then you can toggle folding with za. You can fold 
""everything with zM and unfold everything with zR.
""zm and zr can be used to get those folds just right.
""Always remember the almighty help file at 
"" "help :folding" if you get stuck.
"
"" Only do this when not done yet for this buffer
"if exists("b:did_ftplugin")
"finish
"endif
"let b:did_ftplugin = 1
"
"map <buffer> <S-e> :w<CR>:!/usr/bin/env python % <CR>
"map <buffer> gd /def <C-R><C-W><CR>
"
""set foldmethod=expr
"set foldexpr=PythonFoldExpr(v:lnum)
"set foldtext=PythonFoldText()
"
"map <buffer> f za
"map <buffer> F :call ToggleFold()<CR>
"let b:folded = 1
"
"function! ToggleFold()
"if( b:folded == 0 )
"exec "normal! zM"
"let b:folded = 1
"else
"exec "normal! zR"
"let b:folded = 0
"endif
"endfunction
"
"function! PythonFoldText()
"let size = 1 + v:foldend - v:foldstart
"if size < 10
"let size = " " . size
"endif
"if size < 100
"let size = " " . size
"endif
"if size < 1000
"let size = " " . size
"endif
"
"if match(getline(v:foldstart), '"""') >= 0
"let text = substitute(getline(v:foldstart), '"""', '', 'g' ) . ' '
"elseif match(getline(v:foldstart), "'''") >= 0
"let text = substitute(getline(v:foldstart), "'''", '', 'g' ) . ' '
"else
"let text = getline(v:foldstart)
"endif
"
"return size . ' lines:'. text . ' '
"endfunction
"
"function! PythonFoldExpr(lnum)
"if indent( nextnonblank(a:lnum) ) == 0
"return 0
"endif
"
"if getline(a:lnum-1) =~ '^\(class\|def\)\s'
"return 1
"endif
"
"if getline(a:lnum) =~ '^\s*$'
"return "="
"endif
"
"if indent(a:lnum) == 0
"return 0
"endif
"
"return '='
"endfunction
"
"" In case folding breaks down
"function! ReFold()
"set foldmethod=expr
"set foldexpr=0
"set foldnestmax=1
"set foldmethod=expr
"set foldexpr=PythonFoldExpr(v:lnum)
"set foldtext=PythonFoldText()
"echo
"endfunction 

"Toggle fold methods 

"#### no so nice method
"let g:FoldMethod = 0
"map <leader>fo :call ToggleFold()<cr>
"fun! ToggleFold()
"if g:FoldMethod == 0
"exe 'set foldmethod=indent'
"let g:FoldMethod = 1
"else
"exe 'set foldmethod=marker'
"let g:FoldMethod = 0
"endif
"endfun
""Add markers (trigger on class Foo line)
"nnoremap ,f2 ^wywO#<c-r>0 {{{2<esc>
"nnoremap ,f3 ^wywO#<c-r>0 {{{3<esc> 
"nnoremap ,f4 ^wywO#<c-r>0 {{{4<esc>
"nnoremap ,f1 ^wywO#<c-r>0 {{{1<esc>
"


filetype on 
syntax on
set term=xterm-256color
highlight Comment ctermbg=black ctermfg=cyan
set t_kb=
set backspace=2
autocmd BufRead *.py set tabstop=4
autocmd BufRead * set nowrap
autocmd BufRead * set go+=b


autocmd FileType python compiler pylint



"make nice spelling 
"setlocal spell spelllang=en_us
highlight clear SpellBad
highlight SpellBad term=standout ctermfg=1 term=undercurl cterm=undercurl
highlight clear SpellCap
highlight SpellCap term=undercurl cterm=undercurl
highlight clear SpellRare
highlight SpellRare term=undercurl cterm=undercurl
highlight clear SpellLocal
highlight SpellLocal term=undercurl cterm=undercurl

set pastetoggle=<F2>
"map <F12> :new \| r!pylint #<cr><cr>
"map <F12> :new \| r!pylint #<cr><cr>
map <F11> :set filetype=python <cr>
map <F10> :call Pylint(1)<cr>
map <F9> :!sci -T %<cr><cr>
