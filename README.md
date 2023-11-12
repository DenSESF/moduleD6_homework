
# Module D5, NewsPaper

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
