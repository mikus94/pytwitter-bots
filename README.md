Bot existence in Twitter conversations during Polish municipal election (Warsaw).
==
Polish Abstract.

W obecnych czasach wielu badaczy, dziennikarzy a także śledczych doszło do wniosku, że social media są ważnym narzędziem używanym do manipulacji opinią publiczną. Wiele badań wskazuje na masowe działania dezinformacyjnych w social mediach. W części tych kampanii wykorzystywano boty (tzw. social bots), które swoim zachowaniem miały przypominać ludzi. W mojej pracy chciałbym przeanalizować występowanie takich manipulacji podczas kampanii do ostatnich wyborów prezydentckich w Warszawie. W okresie ponad dwóch tygodnii poprzedzającym dzień elekcyjny (05/10/18 do 22/10/18) zbierałem tweety zawierające słowa kluczowe związane z wyborami w Warszawie. Wykorzystując technikę uczenia maszynowego udało mi się sklasyfikować część użytkowników będących potencjalnymi botami biorącymi udział w debacie publicznej.

---
Repository contain my Masters Degree Thesis work.
It includes few modules:
- <i>data-collection</i>
<br> This module takes care of data collection from Twitter. Data collection is 
executed by gathering only interesting tweets by given topic. This module saves 
downloaded tweets in files and also into database if needed.
- <i>machine-learning</i>
<br> This module handles recognition and extraction users and bots.
It is done with machine learning.
- <i>sql</i>
<br> SQL module that contains all the useful scripts used to maintain and manage 
data that are stored in database.

---
<h3>Technologies used in project.</h3>
Python 3.7.0 with libraries:
- numpy
- sklearn
- tweepy
- psycopg2
- other useful like:
  * os
  * time
  * datetime
  * json
  * getopts
  * csv
  * glob
  * matplotlib

TwitterAPI
<br>
PostgreSQL