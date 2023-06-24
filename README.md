## Why and How Blocking Relations between Bugs are Breakable: An Empirical Study on Breakable Blocking Bugs
In this software repository, we present the source code and dataset in this study in the following two folders, respectively.
- code. This folder contains the source code for this study.
- datasets. This folder contains the datasets used in each of the research questions in this paper. These data sets contain the evaluation metrics proposed in RQ and the corresponding bug categories.

Next, the functions in the source code are introduced in detail.
- To calculate the breakable blocking bugs in the project, it is necessary to extract the basic bug information and bug activity information on Bugzilla in each project. Among them, the basic information of the bug can be obtained by searching the Bug ID on the Bugzilla of different projects. The Bugzilla link for each project is as follows, and users can search the Bug ID on these Bugzilla links.
    - eclipse: http://bugs.eclipse.org/bugs/
    - mozilla: https://bugzilla.mozilla.org
    - freedesktop: https://bugs.freedesktop.org
    - netbeans: https://netbeans.org/bugzilla/
    - openoffice: https://bz.apache.org/ooo/

- The basic bug information of the project and the activity information of the bug are also required when calculating the metrics of RQ1 and RQ2. The corresponding two functions in the code file need to input the file path where the bug information is stored. 

- When calculating the metrics of RQ3, since the calculation of these characteristics is based on the static analysis results of Understand, developers need to perform static analysis on the corresponding version of the project manually. The version information of these projects is saved to the versions file. In addition, the commit information in the project needs to be used when mapping bugs to source files, mainly including commit time, commit description information, and changed file information on commit. This information needs to be obtained by the developer from the version information of the project.

Next, the files in the datasets file are described.
- In the dataset folder, it mainly includes the dataset on RQ1, RQ2, and RQ3. These files mainly include: project name, bug id, bug type, and corresponding metrics. RQ3 calculates the metric value on the source file, so it also includes the source file information and the bugs corresponding to the source file.

- In addition, the datasets file also has the results of manual analysis of the reasons and measures of breaking the blocking relationship on bugs in RQ4 and RQ5. These two files ("review_result_1.txt" and "review_result_2.txt") are the results of manual analysis conducted by two authors respectively, and "final_review_result.txt" is the result of the final manual analysis.

- This file ("bug_distribution.csv") shows the overall distribution of different types of bugs and the distribution of different types of bugs that can be matched to commits.