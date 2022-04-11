1. Coding style

    - Some approachs

        - Avoid abbreviating variable names.
        - Write out your function argument names.
        - Document your classes and methods.
        - Comment your code.
        - Refactor repeated lines of code into reusable functions or methods.
        - Keep functions and methods short. A good rule of thumb is that scrolling should not be necessary 
        to read an entire function or method.

    - The import order in a Django project is:

        1 Standard library imports.
        2 Imports from core Django.
        3 Imports from third-party apps including those unrelated to Django.
        4 Imports from the apps that you created as part of your Django project.

    - Table 1.1: Imports: Absolute vs. Explicit Relative

        ---------------------------------------------------------------------------------------------------------------------------
        |            Code                     |     Import Type        |               Usage                                       |
        ---------------------------------------------------------------------------------------------------------------------------
        | from core.views import FoodMixin    |    absolute import     | Use when importing from outside the current app           |
        | from .models import WaffleCone      |    explicit relative   | Use when importing from another module in the current app |
        ---------------------------------------------------------------------------------------------------------------------------

    - Use Underscores("_") in URL Pattern Names Rather Than Dashes


2. The optimal django environment setup

    - This chapter covered using the same database in development as in production, pip, virtualenv,
      venv, conda, poetry, pipenv, version control, and Docker. These are good to have
      in your tool chest, since they are commonly used not just in Django, but in the majority of
      Python software development.


3. How to Lay Out Django Projects

    - example layouts

        icecreamratings_project                 # repository_root/
        ├── config/                             # configuration_root/
        │ ├── settings/
        │ ├── __init__.py
        │ ├── asgi.py
        │ ├── urls.py
        │ └── wsgi.py
        ├── docs/
        ├── icecreamratings/                    # django_project_root/
        │ ├── media/ # Development only!
        │ ├── products/
        │ ├── profiles/
        │ ├── ratings/
        │ ├── static/
        │ └── templates/
        ├── .gitignore
        ├── Makefile
        ├── README.md
        ├── manage.py
        └── requirements.txt

    - We like to put all our environments in one directory and all our projects in another.

    `~/projects/icecreamratings_project/`

    `~/.envs/icecreamratings/`


4. Fundamentals of Django App Design

    - Vocabulary
        Django project:
            is a web application powered by the Django web framework.
        Django apps:
            are small libraries designed to represent a single aspect of a project. (A Django
            project is made up of many Django apps.)
        Installed apps: 
            is the list of Django apps used by a given project available in its
            INSTALLED_APPS setting.
        Third-party Django packages:
            are simply pluggable, reusable Django apps that have been
            packaged with the Python packaging tools

    - Each Django app should be tightly-focused on its own task and possess a simple, easy-to-remember name. If an app
      seems too complex, it should be broken up into smaller apps.


5. Settings and Requirements Files

    - Best Practices

        - All settings files need to be version-controlled. This is especially true in production
          environments, where dates, times, and explanations for settings changes absolutely
          must be tracked.

        - Don’t Repeat Yourself. You should inherit from a base settings file rather than
          cutting-and-pasting from one file to another(base.py, local.py, prod.py, stg.py).

            icecreamratings_project/         
            └── config/           
                ├── settings/
                └── ├── __init__.py
                    ├── base.py
                    ├── local_audreyr.py
                    ├── local_pydanny.py
                    ├── local.py
                    ├── staging.py
                    ├── test.py
                    └── production.py

            `python manage.py shell --settings=config.settings.local`
            `python manage.py runserver --settings=config.settings.local`

        - Keep secret keys safe. They should be kept out of version control.

            `export SOME_SECRET_KEY=1c3-cr3am-15-yummy`

            >>> # Top of settings/production.py
            >>> import os
            >>> SOME_SECRET_KEY = os.environ['SOME_SECRET_KEY']

        - Installing From Multiple Requirements Files

            requirements/
            ├── base.txt
            ├── local.txt
            ├── staging.txt
            └── production.txt

            `pip install -r requirements/local.txt`

        - Handling File Paths in Settings

            - XXXX Never Hardcode File Paths XXXX

                >>> # settings/base.py
                >>> # DON’T DO THIS! Hardcoded to just one user's preferences
                >>> MEDIA_ROOT = '/Users/pydanny/twoscoops_project/media'

            - Instead set a BASE_DIR-like setting with Pathlib

                >>> # settings/base.py
                >>> from pathlib import Path
                >>> BASE_DIR = Path(__file__).resolve().parent.parent.parent

                >>> MEDIA_ROOT = BASE_DIR / 'media'
                >>> STATIC_ROOT = BASE_DIR / 'static_root'
                >>> STATICFILES_DIRS = [BASE_DIR / 'static']


6. Model Best Practices

    - Break Up Apps With Too Many Models to no more than five to ten models per app.

    - Be Careful With Model Inheritance
        
        - No model inheritance: If models have a common field, give both models that field.
        - Abstract base classes: Tables are only created for derived models.
        - Multi-Table Inheritance: tables are created for both parent and child. An implied OneToOneField links parent and child.

        - Rules for knowing which type of inheritance to use and when:

            If the overlap between models is minimal (e.g. you only have a couple of models
            that share one or two identically named fields), there might not be a need for model
            inheritance. Just add the fields to both models.

            Instead of multi-table inheritance, use explicit OneToOneFields and ForeignKeys between 
            models so you can control when joins are traversed. In our combined 20+ years of doing 
            Django we’ve never seen multi-table inheritance cause anything but trouble.

            If there is enough overlap between models that maintenance of models’ repeated fields
            cause confusion and inadvertent mistakes, then in most cases the code should be
            refactored so that the common fields are in an abstract base model.


                ``` core/models.py
                from django.db import models
                
                class TimeStampedModel(models.Model):
                    """
                    An abstract base class model that provides selfupdating
                    ``created`` and ``modified`` fields.
                    """
                    created = models.DateTimeField(auto_now_add=True)
                    modified = models.DateTimeField(auto_now=True)

                    class Meta:
                        abstract = true
                ```

                By defining TimeStampedModel as an abstract base class when we define a new class that
                inherits from it, Django doesn’t create a core_timestampedmodel table when migrate
                is run.

                ``` flavors/models.py
                from django.db import models
                from core.models import TimeStampedModel

                class Flavor(TimeStampedModel):
                    title = models.CharField(max_length=200)
                ```

    - Database Migrations

        - Tips for Creating Migrations

            - As soon as a new app or model is created, create the initial migrations `python manage.py makemigrations.`
            - Examine the generated migration and SQL code `sqlmigrate` before you run it, especially when complex changes are involved.
            - Always back up your data before running a migration.
