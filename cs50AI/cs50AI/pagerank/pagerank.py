import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    # print(corpus)
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    pd = {}
    links = corpus[page]

    if len(links) > 0:
        # If there are links on the current page, distribute
        # PageRank among them based on the transition model.
        pd[page] += (1 - damping_factor) / len(corpus)
        for link in links:
            pd[link] = (damping_factor / len(links)) + (
                (1 - damping_factor) / len(corpus)
            )
    else:
        # If there are no links on the current page, distribute
        # PageRank uniformly among all pages in the corpus.
        for page in corpus:
            pd[page] = 1 / len(corpus)

    return pd


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {}

    # Initialize PageRank values for all pages to zero.
    for page in corpus.keys():
        page_rank[page] = 0

    current_page = random.choice(list(corpus.keys()))

    for i in range(n):
        # Randomly choose a new page based on the transition model.
        rand = random.random()
        if rand < damping_factor and len(corpus[current_page]) != 0:
            current_page = random.choice(list(corpus[current_page]))
        else:
            current_page = random.choice(list(corpus.keys()))
        page_rank[current_page] += 1

    # Normalize PageRank values to sum to 1.
    for page in page_rank:
        page_rank[page] /= n

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    iteratePR = {}

    # Initialize PageRank values for all pages uniformly.
    for page in corpus:
        iteratePR[page] = 1 / N

    change = float("inf")

    # Iterate until the PageRank values converge (change is small).
    while change > 0.001:
        NewPR = {}
        for page in corpus:
            sum = 0
            for possible_page in corpus:
                if page in corpus[possible_page]:
                    sum += iteratePR[possible_page] / len(corpus[possible_page])

            # Calculate the new PageRank value for the current page.
            NewPR[page] = (1 - damping_factor) / N + damping_factor * sum

        # Calculate the change in PageRank values.
        change = 0
        for page in corpus:
            change += abs(iteratePR[page] - NewPR[page])

        # Update the PageRank values for the next iteration.
        iteratePR = NewPR.copy()

    return iteratePR


if __name__ == "__main__":
    main()
