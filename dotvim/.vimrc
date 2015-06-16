if has("gui_running")
   if has("gui_gtk2")
        set guioptions-=T  "remove toolbar
        let dsm=system('fc-list | grep -c Droid\ Sans\ Mono')
        let cons=system('fc-list | grep -c Inconsola')
        if ( dsm > 0)
           set gfn=Droid\ Sans\ Mono\ 10
        elseif ( cons > 0)
           set gfn=Inconsolata\ 12
        else 
           set gfn=Monospace\ 10
        endif
        set background=light
        set lines=35 columns=120
        " enable y and p from X11 clipboad
        " CTL+V on GTK application will paste stuff coppied with y
        set clipboard=unnamedplus
   endif
else
    set term=xterm-256color
    "set term=screen-256color
    set t_Co=256
endif

set nocompatible	" Use Vim defaults (much better!)
set bs=indent,eol,start " allow backspacing over everything in insert mode
set ai			" always set autoindenting on


call plug#begin('~/.vim/plugged')

" Make sure you use single quotes
Plug 'junegunn/seoul256.vim'
Plug 'junegunn/vim-easy-align'
"
" On-demand loading
Plug 'scrooloose/nerdtree', { 'on':  'NERDTreeToggle' }
Plug 'tpope/vim-fireplace', { 'for': 'clojure' }
"
Plug 'tpope/vim-fugitive'
Plug 'Lokaltog/vim-easymotion'
"Plug 'git://git.wincent.com/command-t.git'
Plug 'altercation/vim-colors-solarized'
" XML/HTML tags navigation
"Plug 'matchit.zip'
" Gvim colorscheme
"Plug 'Wombat'
" Python and PHP Debugger
"Plug 'fisadev/vim-debug.vim'
" " Better file browser
Plug 'scrooloose/nerdtree'
" Code commenter
"Plug 'scrooloose/nerdcommenter'
" Class/module browser
Plug 'majutsushi/tagbar'
" Code and files fuzzy finder
"Plug 'kien/ctrlp.vim'
" Zen coding
"Plug 'mattn/emmet-vim'
" Tab list panel
"Plug 'kien/tabman.vim'
" Powerline
"Plug 'Lokaltog/vim-powerline'
"Plug 'fisadev/fisa-vim-colorscheme'
" Consoles as buffers
"Plug 'rosenfeld/conque-term'
" Surround
"Plug 'tpope/vim-surround'
" Indent text object
"Plug 'michaeljsmith/vim-indent-object'
"Plug 'klen/python-mode' 
"Plug 'joonty/vdebug.git'
"Plug 'scrooloose/syntastic'
"Plug 'guns/xterm-color-table.vim'
"Plug 'Shougo/neocomplete.vim'
""Plug 'git://repo.or.cz/vcscommand.git'
Plug 'int3/vim-extradite'
Plug 'airblade/vim-gitgutter'
Plug 'buztard/vim-nomad'
Plug 't9md/vim-choosewin'
Plug 'yegappan/mru'
"Plug 'andviro/flake8-vim'
" SQLComplete 
"Plug 'vim-scripts/SQLComplete.vim'
Plug 'chrisbra/csv.vim'
"Plug 'SirVer/ultisnips'
"Plug 'honza/vim-snippets'
"Plug 'tpope/vim-eunuch'
"Plug 'python-rope/ropevim'
"Plug 'kien/rainbow_parentheses.vim'
Plug 'bling/vim-airline'
Plug 'luochen1990/rainbow'
"Plug 'junegunn/rainbow_parentheses.vim'
"
call plug#end()
"
" always show status bar
set ls=2
" incremental search
set incsearch
"
" highlighted search results
set hlsearch
"
" line numbers
set nu
"
" toggle Tagbar display
"map <F4> :TagbarToggle<CR>
" autofocus on Tagbar open
"let g:tagbar_autofocus = 1
"
" NERDTree (better file browser) toggle
"map <F3> :NERDTreeToggle<CR>
" Ignore files on NERDTree
"let NERDTreeIgnore = ['\.pyc$', '\.pyo$']
"
" tab navigation
"map tn :tabn<CR>
"map tp :tabp<CR>
"map tm :tabm 
"map tt :tabnew 
"
" to use fancy symbols for powerline, uncomment the following line and use a
" patched font (more info on the README.rst)
" based on https://github.com/fisadev/fisa-vim-config
"let g:pymode_lint_write = 1
"let g:syntastic_always_populate_loc_list=1
"let g:syntastic_auto_loc_list=1
"let g:syntastic_loc_list_height=4
"let g:syntastic_python_checkers=['flake8']
"let g:syntastic_python_flake8_args = "--ignore=E501 --max-complexity 10"
"let g:syntastic_warning_symbol = 'ww'
" to use fancy symbols for powerline, uncomment the following line and use a
" patched font (more info on the README.rst)
" let g:Powerline_symbols = 'fancy'
"
"
"" tablength exceptions
"autocmd FileType html setlocal shiftwidth=2 tabstop=2
"autocmd FileType htmldjango setlocal shiftwidth=2 tabstop=2
"autocmd FileType javascript setlocal shiftwidth=2 tabstop=2
""autocmd FileType c setlocal shiftwidth=2 tabstop=2 foldmethod=syntax
"
"set clipboard=unnamedplus
" hight background when lines are longer
let &colorcolumn=join(range(81,999),",")
"
" force spell when doing a git commit 
if  bufname("%")=="COMMIT_EDITMSG"
    set spell 
    set spelllang=en 
endif
"
"0 if you want to enable it later via :RainbowToggle
let g:rainbow_active = 1 
filetype plugin on

"Activation based on file type
"augroup rainbow_lisp
"  autocmd!
"  autocmd FileType * RainbowParentheses
"augroup END