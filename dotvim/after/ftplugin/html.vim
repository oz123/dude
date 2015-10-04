setlocal shiftwidth=2 
setlocal tabstop=2 
setlocal softtabstop=2
setlocal foldmethod=syntax
set foldlevel=1
set foldlevelstart=1
nmap <F5> :w <Bar>silent !xdg-open %:p &<CR>
