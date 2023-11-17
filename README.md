# GITS3.2

## Group30_Proj3

**For a limited time, this app is deployed in a AWS server. You can access it by [https://csc510.obear.io/start](https://csc510.obear.io/start).**

> You must accept Privacy Policy/EULA to continue.

[Setup - YouTube Link](https://www.youtube.com/watch?v=3JSH69fN-iU)  
[Tutorial - YouTube Link](https://www.youtube.com/watch?v=ESP3zT4LMaM)

### GITS3.2 - I.R.I.S (Ideal ReposItory for Software projects)

![GitHub](https://img.shields.io/github/license/psvkaushik/Group50_Proj2)
[![codecov](https://codecov.io/gh/psvkaushik/Group50_Proj2/graph/badge.svg?token=3QCL57IUZF)](https://codecov.io/gh/psvkaushik/Group50_Proj2)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10023548.svg)](https://doi.org/10.5281/zenodo.10023548)
[![GitHub issues](https://img.shields.io/github/issues/psvkaushik/Group50_Proj2)](https://github.com/psvkaushik/Group50_Proj2/issues?q=is%3Aopen+is%3Aissue)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/psvkaushik/Group50_Proj2)](https://github.com/psvkaushik/Group50_Proj2/issues?q=is%3Aissue+is%3Aclosed)
[![](https://tokei.rs/b1/github/psvkaushik/Group50_Proj2)](https://github.com/psvkaushik/Group50_Proj2).
![Github pull requests](https://img.shields.io/github/issues-pr/psvkaushik/Group50_Proj2)
[![GitHub stars](https://badgen.net/github/stars/psvkaushik/Group50_Proj2)](https://badgen.net/github/stars/psvkaushik/Group50_Proj2)
[![Respost - Write comment to new Issue event](https://github.com/psvkaushik/Group50_Proj2/actions/workflows/Respost.yml/badge.svg)](https://github.com/psvkaushik/Group50_Proj2/actions/workflows/Respost.yml)
![version](https://img.shields.io/badge/version-4.1-blue)
[![Greetings](https://github.com/psvkaushik/Group50_Proj2/actions/workflows/greetings.yml/badge.svg)](https://github.com/psvkaushik/Group50_Proj2/actions/workflows/greetings.yml)
[![Close as a feature](https://github.com/psvkaushik/Group50_Proj2/actions/workflows/close_as_a_feature.yml/badge.svg)](https://github.com/psvkaushik/Group50_Proj2/actions/workflows/close_as_a_feature.yml)
![GitHub contributors](https://img.shields.io/github/contributors/psvkaushik/Group50_Proj2)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/psvkaushik/Group50_Proj2)
[![Style Checker and Prettify Code](https://github.com/psvkaushik/Group50_Proj2/actions/workflows/Style_Checker_and_Prettify_Code.yml/badge.svg)](https://github.com/psvkaushik/Group50_Proj2/actions/workflows/Style_Checker_and_Prettify_Code.yml)
[![GitHub Actions](https://github.com/psvkaushik/Group50_Proj2/actions/workflows/build_test.yaml/badge.svg)](https://github.com/psvkaushik/Group50_Proj2/actions/workflows/build_test.yaml)
[![Running Code Coverage](https://github.com/psvkaushik/Group50_Proj2/actions/workflows/codecov.yml/badge.svg)](https://github.com/psvkaushik/Group50_Proj2/actions/workflows/codecov.yml)

<p align="center">
    <a href="https://github.com/Michaellzd/CSC510_Proj3/issues/new/choose">Report Bug</a>
</p>

# 🧐 About GITS3.2

"Your repo is your resume. But what is a good looking repo?"

So you want to start a Project on Github <br><br>
Do CLI commands scare you?? <br><br>
Do platform dependencies of softwares available annoy you?? <br><br>
Don't worry we got you! Introducing GITS3.2

GITS3.2 simplifies the organization of your repository according to Software Engineering Standards, ensuring it adheres to the required structure for a "Well-Structured Repository."

Think of GITS3.2 as a foundational repository that helps align your project repository with these standards.

Here are few motivation points to come up with this idea

1. When dealing with various files and branches, there often arises a need to update multiple commands in a particular sequence, which can become cumbersome. Employing a custom command that can execute multiple commands simultaneously in a predefined order is a time-saving and developer-friendly solution.
2. While tackling an assignment for the course, we discovered a shortage of project repositories that follow a standardized structure.
3. Developers might struggle to create projects that are easily transferable.

# 🛠️ Installation Setup

1. Install the pre-requisites Python 3.9 or above from [here](https://www.python.org/downloads/) and Git from [here](https://git-scm.com/downloads).
2. Open terminal and clone repository
   ```
   git clone https://github.com/psvkaushik/Group50_Proj2
   ```
3. Navigate to the directory and enter following command on terminal for linux or mac os
   ```
   bash setup.sh
   ```
   Navigate to the directory and enter following command on terminal for windows
   ```
   windows_setup
   ```

Detail about generating token is given [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

4. Navigate to the project directory and run the app.py file as follows
   ```bash
   python3 ./src/app.py
   ```
   Quick start guide can be found [here](https://github.com/psvkaushik/Group50_Proj2/blob/main/docs/Quick_start_guide.md)\
   Case studies can be found [here](https://github.com/psvkaushik/Group50_Proj2/blob/main/docs/case_study.md)  
   Troubleshooting steps can be found [here](https://github.com/psvkaushik/Group50_Proj2/blob/main/docs/Troubleshooting_guide.md)

## 📝 Project 3(Score card and video!) </a>

<span style="color:blue">[Project 3 Readme !](proj3/README.md)</span>

# 🗺️Roadmap

- [x] Initally , the software had separate implementaion for Linux, Windows or MAC . Now we have made sure the commands can be executed on all platforms without any dependancies
- [x] Also made an executable to setup the project on command line for ease of use for the user
- [x] Implemented a UI
- [x] Provided feature to add custom commands and included instaructions on using template to create corressponding code
- [x] GitHub token management
- [x] Website without refresh
- [ ] Host application on cloud
- [ ] Containerize the application

# Third Party Dependencies

1. Git [link](https://github.com/git-guides/install-git)
2. Python [link](https://www.python.org/downloads/)
3. Requests [link](https://pypi.org/project/requests/)
4. Flask [link](https://flask.palletsprojects.com/en/3.0.x/installation/#python-version)
5. PyYaml [linl](https://pypi.org/project/PyYAML/)

## 👥 Team Members <a name="TeamMember"></a>

Group 30:

Jack Hou

Zhendong Lu

Feng Wang

Enxi Zhang

# 📇Contact us

For any inquiries, you can reach out to us via email:

- [735955506@qq.com](mailto:1.735955506@qq.com)
- [fwang32@ncsu.edu](mailto:fwang32@ncsu.edu)
- [yhou8@ncsu.edu](mailto:yhou8@ncsu.edu)
- [1gabriel.zhang1@gmail.com](mailto:1gabriel.zhang1@gmail.com)

Made with ❤️ on GitHub.
