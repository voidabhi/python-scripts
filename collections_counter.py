from collections import Counter
import re
import urllib  # for more pleasant http, use http://bit.ly/python-requests


def main(n=10):

    # Download the content
    content = urllib.urlopen('http://bit.ly/thewonderfulwizard').read()

    # Clean the content a little
    content = re.sub('\s+', ' ', content)  # condense all whitespace
    content = re.sub('[^A-Za-z ]+', '', content)  # remove non-alpha chars
    words = content.split()

    # Start counting
    word_count = Counter(words)

    # The Top-N words
    print("The Top {0} words".format(n))
    for word, count in word_count.most_common(n):
        print("{0}: {1}".format(word, count))


if __name__ == "__main__":
    main()
