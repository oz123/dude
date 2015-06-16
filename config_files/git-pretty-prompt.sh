##-ANSI-COLOR-CODES-##
Color_Off="\[\033[0m\]"
NO_COLOUR="\[\033[0m\]"
###-Regular-###
Red="\[\033[0;31m\]"
Green="\[\033[0;32m\]"
Purple="\[\033[0;35m\]"
####-Bold-####
BRed="\[\033[1;31m\]"
BPurple="\[\033[1;35m\]"
Cyan="\[\033[1;36m\]"
Blue="\[\033[1;34m\]"
Yellow="\[\033[0;33m\]"


# set up command prompt
function __prompt_command()
{
    # capture the exit status of the last command, ipython style
    EXIT="$?"
    if [ $EXIT -eq 0 ]; then 
       PS1="$Green[\#]$Color_Off "; 
    else 
       PS1="$Red[\#]$Color_Off "; 
    fi
 

    # if logged in via ssh shows the ip of the client
    if [ -n "$SSH_CLIENT" ]; then 
       PS1+="$Yellow ("${SSH_CLIENT%% *}") $Color_Off "; 
    fi
 
    # basic information (user@host:path)
    PS1+="$Blue\u$Color_Off@$Blue\h$Color_Off:$BPurple\w$Color_Off "
 
    # check if inside git repo
    local git_status
    git_status=$(git status -unormal 2>&1)
    EST=$?
    if [ $EST != 0 ]; then
       echo "not a repo $EST" > /tmp/foo.txt
    else
       echo "${EST}" >> /tmp/foo.txt
    fi
    #if ! [[ "$git_status" =~ "Not a git repo" ]]; then
    if [ $EST == 0 ]; then 
        # parse the porcelain output of git status
        if [[ "$git_status" =~ "nothing to commit" ]]; then
           local Color_On=$Green
        elif [[ "$git_status" =~ "nothing added to commit but untracked files present" ]]; then
           local Color_On="$Purple"
        else
           local Color_On="$Red"
        fi
     
	if [[ "$git_status" =~ "On branch ([^[:space:]]+)" ]]; then
        branch=${BASH_REMATCH[1]}
        else
            # Detached HEAD. (branch=HEAD is a faster alternative.)
            branch="$(git describe --all --contains --abbrev=4 HEAD 2> /dev/null || echo HEAD)"
        fi
        branch="["$branch"]"
        # add the result to prompt
        
        PS1+="$Color_On$branch$Color_Off "
    fi
    
    PS1+="\$ "

    # Prepend python virtualenv stuff 
    if [ ! -z $VIRTUAL_ENV  ]; then
       PS1="(`basename \"$VIRTUAL_ENV\"`)$PS1"
    fi 
}

PROMPT_COMMAND=__prompt_command
