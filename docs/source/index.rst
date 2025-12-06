Czech_air_quality documentation
================================

.. toctree::
   :maxdepth: 2
   :caption: Table of contents:

   api/index

Quick Example
=============

.. code-block:: python

    from czech_air_quality import AirQuality
    
    # Create a client
    aq = AirQuality()
    
    # Get air quality report for a city
    report = aq.get_air_quality_report("Prague")
    print(report)

Useful Links
============

- `PyPi package page <https://pypi.org/project/czech-air-quality/>`_
- `GitHub Repository <https://github.com/chickendrop89/czech_air_quality>`_
