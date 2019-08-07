# Rural Hospital Closures Since 2005

[Check it out!](https://alexklavens.github.io/hospital-closure-map)

## Background

While working as a news intern at WBUR during Summer 2017,
I [reported on a decision](https://alexklavens.github.io/radio#north-adams) by the Massachusetts Attorney General to not punish
the former leaders of a Western Massachusetts hospital that closed in 2014 with
less than a week's notice.

I decided to look into other hospital closures and create a visualization. I will be expanding the project further to include visualizations of what happened to hospital access after these facilities shut down.

## Data Gathering

This visualization uses data from [University of North Carolina](http://www.shepscenter.unc.edu/programs-projects/rural-health/rural-hospital-closures/).

The data was not available in a downloadable format, and their html tables do not contain information about many hospital closures that are mapped in a google maps iframe.

I had to 'View Frame Source' into the google map iframe, pull out some sort of JavaScript data structure holding all the information, and clean that information using python and regular expressions.

That code is not currently in this repository, but it produced a GeoJSON-formatted representation of the data. That data can be found in the `hospitals.json` file.


## Visualization

This is a D3.js-based front-end project hosted by [a GitHub Pages project site.](https://alexklavens.github.io/hospital-closure-map)
