setlocal foldmethod=indent
setlocal tabstop=4 shiftwidth=4 expandtab

map <silent> <leader>b oimport pdb; pdb.set_trace()<esc>
map <silent> <leader>B Oimport pdb; pdb.set_trace()<esc>
let NERDTreeIgnore = ['\.pyc$']   

highlight ExtraWhitespace ctermbg=lightgreen guibg=lightgreen
autocmd ColorScheme * highlight ExtraWhitespace ctermbg=red guibg=red
match ExtraWhitespace /\s\+$/
