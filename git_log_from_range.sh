start="v0.22.1"
end="${start}-BSK"

GIT_PAGER=cat \
    git log ${start}..${end}


git log ${start}..${end} --format=format:%H | cat

echo "To port:"
echo -n "git cherry-pick"

for commit in $(git log ${start}..${end} --format=format:%H | tac && echo); do
    echo " \\"
    echo -n "  ${commit}"
done
