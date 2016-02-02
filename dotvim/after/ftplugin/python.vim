setlocal foldmethod=indent
setlocal tabstop=4 shiftwidth=4 expandtab
au BufWritePre,BufRead,BufNewFile *.py,*.pyw,*.c,*.h match BadWhitespace /\s\+$/
map <silent> <leader>b oimport pdb; pdb.set_trace()<esc>
map <silent> <leader>B Oimport pdb; pdb.set_trace()<esc>
let NERDTreeIgnore = ['\.pyc$']
