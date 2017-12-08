CIS4930 Python Semester Project
Team Members: Andrew Berg, Mathew Tepley, William Wagner.



Description:
* We wanted to leverage Reddit’s popularity and openess in order to draw insights and analysis in how Redditor’s feel. We achieve this by indexing Reddit submissions as they come in, and performing sentiment analysis on them before storing them in a database. On the front-end, we provide a web application where one can search for specific terms and see all the submissions and their corresponding sentiments

* Python libraries we’re using:
    * # packages in environment at /Users/wcwagner/anaconda/envs/insight:
    * #
    * appnope                   0.1.0            py36hf537a9a_0
    * asn1crypto                0.22.0                   py36_0    conda-forge
    * blinker                   1.4                      py36_0    conda-forge
    * ca-certificates           2017.08.26           ha1e5d58_0
    * certifi                   2017.11.5        py36ha569be9_0
    * cffi                      1.11.2                   py36_0    conda-forge
    * chardet                   3.0.4                    py36_0    conda-forge
    * chardet                   3.0.4                     <pip>
    * click                     6.7              py36hec950be_0
    * cryptography              2.1.4                    py36_0    conda-forge
    * decorator                 4.1.2            py36h69a1b52_0
    * elasticsearch             5.4.0                    py36_0    conda-forge
    * elasticsearch-dsl         5.3.0                    py36_0    conda-forge
    * flask                     0.12.2           py36h5658096_0
    * idna                      2.6                      py36_1    conda-forge
    * idna                      2.6                       <pip>
    * ipython                   6.2.1            py36h3dda519_1
    * ipython_genutils          0.2.0            py36h241746c_0
    * itsdangerous              0.24             py36h49fbb8d_1
    * jedi                      0.11.0           py36h3aa571e_0
    * jinja2                    2.10             py36hd36f9c5_0
    * libcxx                    4.0.1                h579ed51_0
    * libcxxabi                 4.0.1                hebd6815_0
    * libedit                   3.1                  hb4e282d_0
    * libffi                    3.2.1                h475c297_4
    * libpq                     9.6.6                h77f6c7a_0    anaconda
    * markupsafe                1.0              py36h3a1e703_1
    * ncurses                   6.0                  hd04f020_2
    * nltk                      3.2.5            py36h1190bce_0
    * oauthlib                  2.0.6                      py_0    conda-forge
    * openssl                   1.0.2m               h86d3e6a_1
    * parso                     0.1.0            py36h71a4127_0
    * pexpect                   4.3.0            py36h427ab81_0
    * pickleshare               0.7.4            py36hf512f8e_0
    * pip                       9.0.1            py36h1555ced_4
    * praw                      5.2.0                     <pip>
    * prawcore                  0.12.0                    <pip>
    * prompt_toolkit            1.0.15           py36haeda067_0
    * psycopg2                  2.7.3.2          py36hfcdd239_0    anaconda
    * ptyprocess                0.5.2            py36he6521c3_0
    * pycparser                 2.18                     py36_0    conda-forge
    * pygments                  2.2.0            py36h240cd3f_0
    * pyjwt                     1.5.3                      py_0    conda-forge
    * pyopenssl                 17.4.0                   py36_0    conda-forge
    * pysocks                   1.6.7                    py36_0    conda-forge
    * python                    3.6.3                h5ce8c04_4
    * python-dateutil           2.6.1                    py36_0    conda-forge
    * readline                  7.0                  hc1231fa_4
    * redis-py                  2.10.6                     py_0    conda-forge
    * requests                  2.18.4                   py36_1    conda-forge
    * requests                  2.18.4                    <pip>
    * requests-oauthlib         0.8.0                    py36_1    conda-forge
    * rq                        0.8.1                    py36_0    conda-forge
    * setuptools                36.5.0           py36h2134326_0
    * simplegeneric             0.8.1            py36he5b5b09_0
    * six                       1.11.0           py36h0e22d5e_1
    * sqlite                    3.20.1               h7e4c145_2
    * tk                        8.6.7                h35a86e2_3
    * traitlets                 4.3.2            py36h65bd3ce_0
    * twython                   3.6.0                    py36_0    conda-forge
    * update-checker            0.16                      <pip>
    * urllib3                   1.22                      <pip>
    * urllib3                   1.22                     py36_0    conda-forge
    * wcwidth                   0.1.7            py36h8c6ec74_0
    * werkzeug                  0.12.2           py36h168efa1_0
    * wheel                     0.30.0           py36h5eb2c71_1
    * xz                        5.2.3                h0278029_2
    * zlib                      1.2.11               hf3cbc9b_2
* List of other resources
    * Reddit API
* Descriptions of any extra features
* Include a description  of separation of work
    * Matt Tepley - Front-end, Overall Design
    * William Wagner - Back-end,  Front-end
    * Andrew Berg - Sentiment analysis

