﻿echo "# pages" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M master
git remote add origin git@github.com:dperov/pages.git
git push -u origin master