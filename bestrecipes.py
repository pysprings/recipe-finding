# -*- coding: utf-8 -*-
# Copyright 2015, Tim Flink <opensource@tirfa.com>
# License: BSD-3-Clause <http://spdx.org/licenses/BSD-3-Clause>
# See the LICENSE file for more details on Licensing

"""This is a simple example of an interface to find the n most highly ranked
recipes on food2fork and display those recipes on the command line. It's not
the best code ever (not much sanity checking or error handling, doesn't handle
spaces in search terms, etc.) but it's a decent example of what can be done
relatively quickly

This code was initially written as part of the PySprings Meetup on August 25,
2015

In order to use this code, you will need an API key from food2fork. At the time
this code was written, a free tier for API usage was available:

http://food2fork.com/about/api
"""

import argparse

import requests


api_base = 'http://food2fork.com/api/'

def get_recipe(api_key, recipe_id):
    """Get the contents of a recipe from the food2fork API"""

    get_url = '{}/get?key={}&rId={}'.format(api_base, api_key, recipe_id)
    r = requests.get(get_url)
    return r.json()['recipe']

def search_recipe(api_key, desired_recipe, ranking_type='r'):
    """Search for a desired recipe using the food2fork api and the specified
    ranking type.

    Spaces in desired_recipe are not handled here - make sure that any spaces
    in the search terms have been replaced with a +"""

    if ranking_type not in ['r','t']:
        raise Exception("ranking_type must be 'r' or 't'. " \
                        "got {}".format(ranking_type))
    search_url = '{}/search?key={}&q={}&sort={}'.format(api_base,
                                                        api_key,
                                                        desired_recipe,
                                                        ranking_type)
    r = requests.get(search_url)
    if not r.ok:
        raise Exception("error searching for {}: {}".format(desired_recipe,
                                                            r.test))
    return r.json()


def get_popular_recipes(api_key, desired_recipe, ranking_type='r',
                        num_results=1):
    """Find the num_results highest ranked recipes matching the desired_recipe
    term and print out the details to stdout"""

    print("Finding the {} best recipes for '{}' based "\
          "on {}".format(num_results, desired_recipe, ranking_type))
    search_results = search_recipe(api_key, desired_recipe, ranking_type)

    for i in xrange(num_results):
        recipe_id = search_results['recipes'][i]['recipe_id']
        recipe = get_recipe(api_key, recipe_id)
        print("\nRecipe #{}: {} ({})".format(i+1,
                                             recipe['title'],
                                             recipe['publisher']))
        print("  url: {}".format(recipe['source_url']))
        print("  ingredients:")
        for ingredient in recipe['ingredients']:
            print("    {}".format(ingredient))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("recipe", nargs=1,
                        help="recipe to search for (use + for spaces)")
    parser.add_argument("-r", "--ranking",
        choices=["r", "t"],
        default="r",
        help="Ranking algorithm to use - 'r'ating (default) or 't'rending")
    parser.add_argument("-a", "--apikey", help="food2fork API key")
    parser.add_argument("-n", "--numrecipes", default="1", type=int,
                        help="number of recipes to find")

    args = parser.parse_args()

    get_popular_recipes(args.apikey,
                        args.recipe[0],
                        args.ranking,
                        args.numrecipes)
