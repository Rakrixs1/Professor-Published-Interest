# Professor Published Interest - CS411 Final Project

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#design">Design</a></li>
    <li><a href="#design">Database Techniques</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
    <li><a href="#video">Video</a></li>
    <li><a href="#extra credit">Extra Credit</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Dashboard](images/2022-05-01-13-05-36.gif)

The purpose of the application is to provide students and staff information of most published keywords including:
- top published keyword in each state
- top keywords used in each university
- top citations for each keyword
- accumalated citations for each professor
- table demonstrating contact information 

### Built With

* [Dash.plotly](https://dash.plotly.com/)
* [Mongodb](https://www.mongodb.com/)
* [Neo4j](https://neo4j.com/)
* [MySQL](https://www.mysql.com/)
* [Pandas](https://pandas.pydata.org/docs/index.html)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

Install packages
   ```sh
   pip install pandas
   pip install mongodb
   pip install dash
   pip install plotly-express
  ```

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Clone the repo
   ```sh
   git clone https://github.com/Rakrixs1/Professor-Published-Interest.git
   ```
 2. Run app.py
   ```sh
   app.py
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

If the user is a student it can provide information when seeking out professors in the area of interest by filtering out keywords. The student will be able to use the US map to hover over information demonstrating the professor in the top spot for published keywords. The student can also use the tree map to filter out by state. The tree map will then demonstrate the top used keyword  for a university in that state, among other universities. When the student chooses a keyword from the tree map they can use the keyword dropdown to search for a specific keyword. This will display information in a bar chart of top citations among professors in the us. If the student will like more information regarding the specific professor of their choice they can use the faculty dropdown to view the accumulated citations for that professor. Once the professor of their choice is selected, the student will be able to contact them using the information on the data table on the bottom of the webpage. 

If the user is a professor it can provide information on their collegues and themselves. By using the keyword dropdown the professor can compare among other collegues. They will also be able to select their name to give visibility of accumulated number of citations they have. 

_For more examples, please refer to the [Video Demo](https://mediaspace.illinois.edu/media/t/1_1co0bp4m)_

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- DESIGN -->
## Design

 - app.py
    - mongodb
    - mysql
    - neo4j1
    - data
      - pf
      - prof_score
 - images
      - 2022-05-01-13-05-36

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- DATABASE TECHNIQUES -->
## Database Techniques

The following techniques where used in the creation of the dashboard
- Indexing
  - used pandas to reset index for mysql academic world table.
- View
  - When using academic world database mySQL Query, Neo4j query, mongodb database query to display the table
- Stored procedure
- Prepared Statement
  - The queries used to import the data. These where store in variables along the app.py file. 
    - Examples: faculty_mongo, keyword_search  

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Akrixs Radilla - radilla2@illinois.edu

Project Link: [https://github.com/Rakrixs1/](https://github.com/Rakrixs1)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Mongodb](https://www.mongodb.com/)
* [Neo4j](https://neo4j.com/)
* [MySQL](https://www.mysql.com/)
* [Pandas](https://pandas.pydata.org/docs/index.html)
* [Dash](https://dash.plotly.com/)
* [Serie A (football) — a simple dashboard with Plotly & Dash](https://towardsdatascience.com/create-a-simple-dashboard-with-plotly-dash-8f385ba1dd6d)
* [Creating an interactive dashboard with Dash Plotly using crime data](https://towardsdatascience.com/creating-an-interactive-dashboard-with-dash-plotly-using-crime-data-a217da841df3)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- VIDEO -->
## Video

* [ProfessorsPublishedInterest-FinalProject-CS411](https://mediaspace.illinois.edu/media/t/1_1co0bp4m)


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- EXTRA CREDIT -->
## Extra Credit

Additional US database was required to display professors in their perspective states in the US MAP Widget. Multiple hours went into datacleaning. New db was created with the merge or the mysql academic world db.


<p align="right">(<a href="#top">back to top</a>)</p>
