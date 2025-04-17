# Name: Yolanda Meng
# CSE 160
# Homework 5

import utils  # noqa: F401, do not remove if using a Mac
import networkx as nx
import matplotlib.pyplot as plt


###
#  Problem 1a
###

def get_practice_graph():
    """Builds and returns the practice graph
    """
    practice_graph = nx.Graph()
    practice_graph.add_edges_from([
        ("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"),
        ("C", "D"), ("C", "F"), ("D", "E"), ("D", "F")
    ])
    return practice_graph


def draw_practice_graph(graph):
    """Draw practice_graph to the screen.
    """
    nx.draw_networkx(graph)
    plt.show()


###
#  Problem 1b
###

def get_romeo_and_juliet_graph():
    """Builds and returns the romeo and juliet graph
    """
    rj = nx.Graph()
    edges = [
        ("Nurse", "Juliet"), ("Juliet", "Tybalt"),
        ("Juliet", "Friar Laurence"), ("Juliet", "Romeo"),
        ("Juliet", "Capulet"), ("Tybalt", "Capulet"),
        ("Capulet", "Escalus"), ("Capulet", "Paris"),
        ("Friar Laurence", "Romeo"), ("Romeo", "Benvolio"),
        ("Romeo", "Montague"), ("Romeo", "Mercutio"),
        ("Benvolio", "Montague"), ("Montague", "Escalus"),
        ("Escalus", "Mercutio"), ("Escalus", "Paris"),
        ("Paris", "Mercutio")
    ]
    rj.add_edges_from(edges)
    return rj


def draw_rj(graph):
    """Draw the rj graph to the screen and to a file.
    """
    nx.draw_networkx(graph)
    plt.savefig("romeo-and-juliet.pdf")
    plt.show()


###
#  Problem 2
###

def friends(graph, user):
    """Returns a set of the friends of the given user, in the given graph.
    """
    # This function has already been implemented for you.
    # You do not need to add any more code to this (short!) function.
    return set(graph.neighbors(user))


def friends_of_friends(graph, user):
    """Find and return the friends of friends of the given user.

    Arguments:
        graph: the graph object that contains the user and others
        user: unique identifier

    Returns: a set containing the names of all of the friends of
    friends of the user. The set should not contain the user itself
    or their immediate friends.
    """
    fof_set = set()
    user_friends = friends(graph, user)

    for friend in user_friends:
        fof_set.update(friends(graph, friend))

    if user in fof_set:
        fof_set.remove(user)

    fof_set -= user_friends

    return fof_set
    pass


def common_friends(graph, user1, user2):
    """
    Finds and returns the set of friends that user1
    and user2 have in common.

    Arguments:
        graph:  the graph object that contains the users
        user1: a unique identifier representing one user
        user2: a unique identifier representing another user

    Returns: a set containing the friends user1 and user2 have in common
    """
    return set(graph.neighbors(user1)) & set(graph.neighbors(user2))
    pass


def common_friends_map(graph, user):
    """Returns a map (a dictionary), mapping a person to the number of friends
    that person has in common with the given user. The map keys are the
    people who have at least one friend in common with the given user,
    and are neither the given user nor one of the given user's friends.
    Example: a graph called my_graph and user "X"
    Here is what is relevant about my_graph:
        - "X" and "Y" have two friends in common
        - "X" and "Z" have one friend in common
        - "X" and "W" have one friend in common
        - "X" and "V" have no friends in common
        - "X" is friends with "W" (but not with "Y" or "Z")
    Here is what should be returned:
      common_friends_map(my_graph, "X")  =>   { 'Y':2, 'Z':1 }

    Arguments:
        graph: the graph object that contains the user and others
        user: unique identifier

    Returns: a dictionary mapping each person to the number of (non-zero)
    friends they have in common with the user
    """
    common_map = {}

    for person in friends_of_friends(graph, user):
        common_map[person] = len(common_friends(graph, user, person))

    return common_map
    pass


def num_map_to_sorted_list(map_with_number_vals):
    """Given a dictionary, return a list of the keys in the dictionary.
    The keys are sorted by the number value they map to, from greatest
    number down to smallest number.
    When two keys map to the same number value, the keys are sorted by their
    natural sort order for whatever type the key is, from least to greatest.

    Arguments:
        map_with_number_vals: a dictionary whose values are numbers

    Returns: a list of keys, sorted by the values in map_with_number_vals
    """
    items = list(map_with_number_vals.items())

    def custom_sort(item):
        return (-item[1], item[0])

    items.sort(key=custom_sort)

    sorted_keys = []
    for item in items:
        sorted_keys.append(item[0])

    return sorted_keys
    pass


def recs_by_common_friends(graph, user):
    """
    Returns a list of friend recommendations for the user, sorted
    by number of friends in common.

    Arguments:
        graph: the graph object that contains the user and others
        user: a unique identifier

    Returns: A list of friend recommendations for the given user.
    The friend recommendation list consists of names/IDs of people in
    the graph who are not yet a friend of the given user.  The order
    of the list is determined by the number of common friends (people
    with the most common friends are listed first).  In the
    case of a tie in number of common friends, the names/IDs are
    sorted by their natural sort order, from least to greatest.
    """
    return num_map_to_sorted_list(common_friends_map(graph, user))
    pass


###
#  Problem 3
###

def influence_map(graph, user):
    """Returns a map (a dictionary) mapping from each person to their
    influence score, with respect to the given user. The map only
    contains people who have at least one friend in common with the given
    user and are neither the user nor one of the users's friends.
    See the assignment writeup for the definition of influence scores.
    """
    scores = {}
    user_friends = friends(graph, user)

    for friend in user_friends:
        friend_friends = friends(graph, friend)
        influence = 1 / len(friend_friends)

        for person in friend_friends:
            if person != user and person not in user_friends:
                scores[person] = scores.get(person, 0) + influence

    return scores
    pass


def recs_by_influence(graph, user):
    """Return a list of friend recommendations for the given user.
    The friend recommendation list consists of names/IDs of people in
    the graph who are not yet a friend of the given user.  The order
    of the list is determined by the influence score (people
    with the biggest influence score are listed first).  In the
    case of a tie in influence score, the names/IDs are sorted
    by their natural sort order, from least to greatest.
    """
    scores = influence_map(graph, user)
    items = list(scores.items())

    def custom_sort(item):
        return (-item[1], item[0])

    items.sort(key=custom_sort)

    sorted_keys = []
    for item in items:
        sorted_keys.append(item[0])

    return sorted_keys
    pass


###
#  Problem 5
###


def get_facebook_graph(filename="facebook-links-small.txt"):
    """Creates an undirected Facebook graph from the file."""
    facebook = nx.Graph()

    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 2:
                user1 = int(parts[0])
                user2 = int(parts[1])
                facebook.add_edge(user1, user2)

    return facebook


def test_get_facebook_graph(facebook, filename):
    if (filename == "facebook-links-small.txt"):
        pass
    else:
        assert len(facebook.nodes()) == 63731
        assert len(facebook.edges()) == 817090


def main():
    # practice_graph = get_practice_graph()
    # Make sure to comment out this line after you have visually verified
    # your practice graph. Otherwise, the picture will pop up every time
    # that you run your program.
    # draw_practice_graph(practice_graph)

    # rj = get_romeo_and_juliet_graph()
    # Make sure to comment out this line after you have visually verified
    # your rj graph and created your PDF file. Otherwise, the picture will
    # pop up every time that you run your program.
    # draw_rj(rj)
    fb_filename = "facebook-links-small.txt"
    facebook = get_facebook_graph(fb_filename)

    ###
    #  Problem 4
    ###
    rj = get_romeo_and_juliet_graph()

    same_recommendations = []
    different_recommendations = []

    for person in rj.nodes():
        recs_common = recs_by_common_friends(rj, person)
        recs_influence = recs_by_influence(rj, person)

        if recs_common == recs_influence:
            same_recommendations.append(person)
        else:
            different_recommendations.append(person)

    same_recommendations.sort()
    different_recommendations.sort()
    print("Problem 4:")
    print()
    print("Unchanged Recommendations:", sorted(same_recommendations))
    print("Changed Recommendations:", sorted(different_recommendations))

    ###
    #  Problem 5
    ###
    facebook = get_facebook_graph(fb_filename)
    test_get_facebook_graph(facebook, fb_filename)

    ###
    #  Problem 6
    ###
    fb_filename = "facebook-links-small.txt"
    facebook = get_facebook_graph(fb_filename)
    print()
    print("Problem 6:")
    print()
    recommend_by_common_friends(facebook)

    ###
    #  Problem 7
    ###
    print()
    print("Problem 7:")
    print()
    recommend_by_influence_score(facebook)

    ###
    #  Problem 8
    ###
    print()
    print("Problem 8:")
    print()
    compare_recommendation_algorithms(facebook)

    ###
    #  Problem 5
    ###

    # (replace this filename with "facebook-links-small.txt" for testing)
    # fb_filename = "facebook-links.txt"

    # (Make sure to call get_facebook_graph)

    fb_filename = "facebook-links-small.txt"
    facebook = get_facebook_graph(fb_filename)

    # Test the Facebook graph
    test_get_facebook_graph(facebook, fb_filename)

    ###
    #  Problem 6
    ###


def recommend_by_common_friends(facebook):
    for user in sorted(facebook.nodes()):
        if user % 1000 == 0:
            recommendations = recs_by_common_friends(facebook, user)[:10]
            print(f"{user} (by num_common_friends): {recommendations}")

    ###
    #  Problem 7
    ###


def recommend_by_influence_score(facebook):
    for user in sorted(facebook.nodes()):
        if user % 1000 == 0:
            recommendations = recs_by_influence(facebook, user)[:10]
            print(f"{user} (by influence): {recommendations}")

    ###
    #  Problem 8
    ###


def compare_recommendation_algorithms(facebook):
    same_count = 0
    different_count = 0

    for user in sorted(facebook.nodes()):
        if user % 1000 == 0:
            common_recs = recs_by_common_friends(facebook, user)[:10]
            influence_recs = recs_by_influence(facebook, user)[:10]
            if common_recs == influence_recs:
                same_count += 1
            else:
                different_count += 1

    print(f"Same: {same_count}")
    print(f"Different: {different_count}")


if __name__ == "__main__":
    main()


###
#  Collaboration
#  no one

# ... Write your answer here, as a comment (on lines starting with "#").
