### You can see the app [Here](centralabs.streamlit.app)
# Back Story 

I made this app when I was the Teacher Assistant (TA) in [Ironhack Portugal](https://www.ironhack.com/) Data Analytics course. 


At Ironhack Portugal, students are responsible for completing a certain number of [labs](https://github.com/gladysmawarni/ironhack-labs) as part of their coursework. There are a total of 42 labs and the minimum requirement is to submit 80% of them. The labs can be found on GitHub and to complete them, students must fork the repository, answer the problems, push the changes to their repository, and create a pull request for the TA to review and correct.

However, I noticed as a student that each person kept their own record of how many labs they had submitted, which ones they still needed to complete from each week, and how many more they needed to meet the minimum requirement. This was a burden for students, who already had a weekly project and a lot of new material to process. Additionally, there were often cases where students thought they had already submitted the labs but had forgotten to create a pull request on GitHub.

When I became a TA, I realized that the TA side was also inefficient as I had to manually go through each student's repository to check for new pull requests, and update their progress in an Excel sheet every day. 

There is no way I am willing to do such a boring task every day when I know how to use Python, so I automated the whole process. 

I created a script that connects to the GitHub API to check for new pull requests from students, updates the Excel sheet, and sends a weekly email to students with their progress (including which labs have been delivered and which ones have not yet been submitted).

Later, my Lead Teacher suggested that I create a platform for students to track their progress themselves, rather than just receiving a weekly email. 

That's why I built this Streamlit app, which uses [Cloud Firestore](https://firebase.google.com/docs/firestore), [GitHub API](https://docs.github.com/en/rest), and [Plotly](https://plotly.com/). 

**This app has two sides - one for students and one for me as the admin.**


# Students Side
The `overview 👀` page of the app allows students to view their overall progress (as a percentage of labs completed) and a detailed view by week. They can also see their submission behavior, including the number of labs submitted per day and their most productive day and time.

In the `comments 💡` page, students can view all the comments that I have posted in one place rather than having to go to GitHub and check pull request comments individually.

In the `hello 👋` page, students have the option to share their daily feelings and song recommendations with their classmates. The `status 💭` page is refreshed daily and allows students to see what their peers have shared. 


# Admin Side
I created the admin page to make my job as a TA easier. It is only accessible to me and allows me to easily track the progress of all students. In the `students progress 📊` page I can see the overall progress of each student and quickly identify anyone who is falling behind or has already met the minimum requirement.
I can also view a detailed view of all students' progress by week, which helps me keep track of which labs I have already reviewed and which ones I need to review.

In addition, I also have access to the `status 💭` page, which allows me to see how students are feeling and share my own song recommendations :) 
