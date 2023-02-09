# Sustainable-Software-Project
## Project Description
This project defines, implements and tests a model for measuring power usage of a desktop app. 

The carbon footprint of apps can be significantly reduced. The carbon cost of network traffic is measurable. Our aim is to develop a solution to measure the energy use of a single app running on a desktop computer. 

## Git workflow
In order to submit your code, you should use a workflow like this. This makes sure that the right versions of the code are in the repo, and that we're all working off the same code. 

1. If you havent already, use `git pull` on the whatever branch your on. This is especially the case for backend, frontend and main branches. 
2. After pulling the branch, use `git checkout` to get on to your teams branch.
3. When you're adding code,(assuming you've just used git pull), you can use `git checkout -b <BRANCH_NAME>` eg `git checkout -b frontend-f-myfeature` The f in this case is for a feature branch.
4. Now in your feature branch you can add your code. 
5. When you're adding code, add it in small pieces, not all at once. 
6. When you've finished a small piece you can add it to staging with `git add myfile.js` You can also do this with vscode or some other editor. 
7. Then commit your code using `git commit -m"Some brief message telling us what the code is doing"`
8. When you've commit your code, then you can push your branch with `git push -u origin <BRANCH_NAME>` eg `git push -u origin frontend-f-myfeature`
9. Go the repository on github.com, and make a pull request to either the frontend, data-gathering or data-analysis BRANCH. 
10. Assign some other person to review the code, and then they will merge the code.
11. In your own feature branch you can start all over again by using `git pull`

## Backend Setup
1. pip install pythonnet OR py -m pip install pythonnet
2. download openhardwaretool from https://openhardwaremonitor.org/downloads/
3. extract the OpenHardwareMonitorLib.dll into the backend folder of the project
4. run your code editor as administrator 
