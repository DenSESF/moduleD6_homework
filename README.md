# Module D6, NewsPaper - newsletter and scheduler

* Added field to model Category
  * subscribers - ManytoMany to model User

* Authentication
  * Enable verify email for registration

* Added to app news
  * Refused to send news if the number of news was exceeded
  * Added category subscription button
  
* New app NoticesTasks
  * Added command runapscheduler
  * sheduler
    * Added blocking scheduler
      * Run job - notify last week new posts
    * Added background scheduler
      * Run job - notify creating new post
  * signals
    * m2m_change - notyfy change post category
    * post_save - sends a welcome email to new users

* Added use decouple

## Module D5, NewsPaper - Authentication and Authorization

* Added use allauth
  * Modified templates login, logout. signup (/templates/account)
  * Modified templates socialaccount login (/templates/socialaccount)
  * Added authentification our Google, modified templates

* New app accounts
  * New function join_authors in views.py
  * New class CustomLoginForm, CustomLoginForm in forms.py

* Added new custom filters
  * RegExError in whiteboard/templatetags/custom_filters.py

* Edit news/views.py
  * Added login requered in classes
    * NewsAddView
    * NewsEditView
    * NewsDeleteView
  * Added permission request in classes
    * NewsAddView
    * NewsEditView
    * NewsDeleteView
