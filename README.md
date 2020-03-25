# Skillstract
A program to scrape indeed job listings to rank given skills in order of most needed. In addition, we are working on using machine learning clustering algorithms to cluster the data (i.e. communication skills, technical skills, etc.). We are also learning SQL to save the data because that will be more convenient than saving the data locally in text files.

Check out the Roman branch for latest, unstable version.

# Performance
Currently takes about 1 minute per 10 job listings 

# Further explanation of the approach
<br>This is an example of what the first job listings page for software
<br>engineering in MA looks like: https://www.indeed.com/jobs?q=software+engineer&l=MA&sort=date
<br>Now, if we look at a single job: https://www.indeed.com/jobs?q=software+engineer&l=MA&sort=date&vjk=3916106ade6d80b3
<br>Note that this is the same URL as the one before, with only vjk=3916106ade6d80b3, the unique job id, added to it.
<br>Overall, this means we can replace the text after q= to get results for a different job (with spaces converted to +),
<br>and replace text after l= with state abbreviation

# Requirements
<br>Have pip ready: https://stackoverflow.com/questions/4750806/how-do-i-install-pip-on-windows?rq=1
<br> *Note, you may already have pip, so check by going to cmd, typing python, and then import pip and you should get no errors, if you have it
<br> Have selenium ready: https://pypi.org/project/selenium/
<br> use: 'pip install selenium' without quotes in cmd

# Nice to have the following to get visual results
<br>Have easygui ready: https://pypi.org/project/easygui/
<br>use: 'pip install easygui' without quotes in cmd
<br>Have matplotlib ready (this is quite heavy): https://pypi.org/project/matplotlib/
<br>use: 'pip install matplotlib' without quotes in cmd
<br>
<br><br><h6>Logo: https://www.flaticon.com/authors/eucalyp</h6>