import json
import praw

class CommentGetter:
    def __init__(self, keys_path):
        """
        Creates new CommentGetter instance, initializing a PRAW reddit client

        :param keys_path: Path to JSON file with OAuth keys
        """
        with open("keys.json") as keys:
            data = json.load(keys)
        
        self.reddit = praw.Reddit(
            client_id = data["clientId"],
            client_secret = data["clientSecret"],
            user_agent = data["userAgent"],
        )

    #TODO should i return the list (submission.comments.list) of comments instead of the submission class
    def get_comments(self, url, replace_more_runs = 50):
        """
        Gets comments for a specified post, loading for as many runs as specified

        :param url: Url of reddit post to get comments from\n
        :param replace_more_runs: Limit for the submission.comments.replace_more() method. Each run takes around 2 seconds longer and loads about 50-100 more comments.
        Increasing increases loaded comments for larger posts, but increases run time

        :returns: praw.submission with comments loaded
        """
        submission = self.reddit.submission(url=url) # Initially load submission
        submission.comments.replace_more(replace_more_runs) # Load more comments
        return submission