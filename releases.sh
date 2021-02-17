#!/bin/sh

dodiff() {
    # Inputs: $1=pr, $2=first commit, $3=optional second commit
    # Output: $3.diffs
    rm -f $1.diff*

    git diff $2 $3 > $1.diff
    diff $1.patch $1.diff > $1.diffs

    rm -f $1.diff
}

getpatch() {
    # Inputs: $1=url, $2=PR
    # Output: $2.patch
    curl -L $1 > $2.diffpatch
    cat $2.diffpatch | perl -pe \
        's/index ([0-9a-f]{10})[0-9a-f]{2}\.\.([0-9a-f]{10})[0-9a-f]{2}/index \1..\2/' \
        > $2.patch

    rm -f $2.diffpatch
}

usage() {
    echo
    echo "Usage: `basename $0` <project-version> [<column-name>]"
    echo
    echo "where"
    echo "  <project-version> is the version of the GitHub project"
    echo "  <column-name>     is the name of the column whose cards are queried"
    echo "                       (default 'Done')"
    echo
    echo "For example, the following command extracts commit hashes from GitHub"
    echo "project cards for a Spack release whose name contains 'v0.16.1':"
    echo "$ sh releases.sh v0.16.1"
    echo
    echo "WARNING: This script is limited to the first 100 results for each"
    echo "query."
    echo
}

column="Done"
if [ $# -lt 1 ]; then
    echo "ERROR: The project version is required."
    usage
    exit 1
elif [ $# -gt 2 ]; then
    echo "ERROR: This script accepts at most two arguments."
    usage
    exit 1
fi

projects_url="https://api.github.com/repos/spack/spack/projects"
version="$1"

if [ $# -eq 2 ]; then
    column="$2"
fi

# Function to extract output to maximum supported per request (i.e., 100)
docurl() {
    curl \
        -u "tldahlgren:$(cat ~/.github/analysis-token)" \
        -H 'Accept: application/vnd.github.inertia-preview+json' \
        "$@"?per_page=100
}

# First pull all of the cards for the desired project column
columns_url=$(docurl $projects_url \
    | jq -r ".[] | select(.name | contains(\"$version\")) | .columns_url")
cards_url=$(docurl "$columns_url" | jq -r --arg cards "$column" \
    '.[] | select(.name==$cards) | .cards_url')

# Extract and process the associated PRs
content_urls=$(docurl $cards_url | jq -r ".[] | select(.content_url != null) \
    | .content_url")
pr_urls=$(docurl $content_urls \
    | jq -r "if (.pull_request != null) then .pull_request.url else empty end")

rm -f $version.$$ $version-$column.$$

for url in $pr_urls; do
    pr_info=($(docurl $url \
        | jq -r ".number, .diff_url, .merge_commit_sha, .commits"))
    pr=${pr_info[0]}
    url=${pr_info[1]}
    sha=${pr_info[2]}
    commits=${pr_info[3]}
    n="1"
    investigate=""
    echo; echo "PR $pr: $commits commit(s):"
    if [ "$commits" != "1" ]; then
        getpatch $url $pr

        # Can the differences be attributed to one commit?
        dodiff $pr $sha~1 $sha
        if [ -s $pr.diffs ]; then
            echo "Detected differences with previous for $pr"
            cat $pr.diffs

            # Differences detected with prior commit, try across all
            dodiff $pr $sha~$commits $sha
            if [ -s $pr.diffs ]; then
                echo "WARNING: Multi-commit diff detected differences for $pr"
                #cat $pr.diffs
                investigate="CheckPR"
            else
                n=$commits
            fi
        fi
        rm -f $pr.patch $pr.diffs $pr.tmp > /dev/null
    fi
    #prs=`git log -n $n --pretty="%ct %H" $sha`
    #prs=`git log -n $n --pretty="%cI %H" $sha`
    prs=`git log -n $n --pretty="%ci %H" $sha`
    echo "$prs" | while read -r line; do
        #abbrev=`echo $line | perl -pe 's/([0-9a-f]{10})[0-9a-f]{30}/\1/'`
        #abbrev=`echo $line | perl -pe 's/([0-9a-f]{20})[0-9a-f]{20}/\1/'`
        echo "$line $pr $investigate" >> $version.$$
    done
    echo ".. $n merge commit(s):"; echo "  $prs"
done

sort -o $version-$column.commits $version.$$ 
echo
echo "Sorted results are in $version-$column.commits"
rm -f $version.$$
