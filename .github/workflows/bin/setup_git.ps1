# (c) 2022 Lawrence Livermore National Laboratory

git config --global user.email "spack@example.com"
git config --global user.name "Test User"
git config --global core.longpaths true

if ($(git branch --show-current) -ne "develop")
{
    git branch develop origin/develop
}
