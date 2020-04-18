from __future__ import print_function
import chandra_bot_data_model_pb2 as dm
import numpy as np
import pandas as pd

class chandra_bot(object):
    """
    a class for data model
    """

    PAPER_DICT = {
        'paper_id': pd.StringDtype(), 'authors': pd.StringDtype(), 'author_ids': pd.StringDtype(),
        'title': pd.StringDtype(), 'year': np.int32, 'committee_publication_decision': pd.StringDtype(),
        'committee_presentation_decision': pd.StringDtype(), 'abstract': pd.StringDtype(),
        'body': pd.StringDtype()
    }

    REVIEW_DICT = {
        'paper_id': pd.StringDtype(), 'presentation_score': np.int32,
        'commentary_to_author': pd.StringDtype(), 'commentary_to_chair': pd.StringDtype(),
        'reviewer_human_hash_id': pd.StringDtype(), 'presentation_recommend': pd.StringDtype(),
        'publication_recommend': pd.StringDtype()
    }

    HUMAN_DICT = {
        'name': pd.StringDtype(), 'aliases': pd.StringDtype(), 'hash_id': pd.StringDtype(),
        'current_affiliation': pd.StringDtype(), 'previous_affiliation': pd.StringDtype(),
        'last_degree_affiliation': pd.StringDtype(), 'orcid_url': pd.StringDtype(),
        'orcid': pd.StringDtype(), 'author_id': pd.StringDtype(), 'verified': 'bool'
    }

    def __init__(
                self,
                paper_df: pd.DataFrame = None,
                review_df: pd.DataFrame = None,
                human_df: pd.DataFrame = None,
                input_paper_book: dm.PaperBook = None
    ):
        """
        constructor
        """
        if input_paper_book is None:
            self.paper_df: pd.DataFrame = paper_df
            self.review_df: pd.DataFrame = review_df
            self.human_df: pd.DataFrame = human_df

            self.paper_book = dm.PaperBook()
        else:
            self.paper_book = input_paper_book

    def _attribute_paper(self, paper: dm.Paper, row: list) -> None:

        paper.number = row['paper_id']
        paper.title = row['title']
        paper.year = int(row['year'])

        if row['committee_presentation_decision'] == 'Reject':
            paper.committee_presentation_decision = dm.PRESENTATION_REC_REJECT
        elif row['committee_presentation_decision'] == 'Accept':
            paper.committee_presentation_decision = dm.PRESENTATION_REC_ACCEPT
        else:
            paper.committee_presentation_decision = None

        if row['committee_publication_decision'] == 'Reject':
            paper.committee_publication_decision = dm.PUBLICATION_REC_REJECT
        elif row['committee_publication_decision'] == 'Accept':
            paper.committee_publication_decision = dm.PUBLICATION_REC_ACCEPT
        else:
            paper.committee_publication_decision = None

        paper.abstract.text = row['abstract']
        paper.body.text = str(row['body'])

    def _attribute_author(self, paper: dm.Paper, author: dm.Author, row: list):
        author.human.name = row['name'].values[0]

        try:
            for alias in row['aliases'].values[0].split(','):
                new_alias = author.human.aliases.add()
                new_alias = alias
        except:
            None

        author.human.hash_id = row['hash_id'].values[0]
        author.human.current_affiliation.name = row['current_affiliation'].values[0]
        author.human.last_degree_affiliation.name = str(row['last_degree_affiliation'].values[0])

        try:
            for affil_name in row['previous_affiliation'].values[0].split(','):
                affiliation = author.human.previous_affiliation.add()
                affiliation.name = row['previous_affiliation'].values[0]
        except:
            None

        author.human.orcid_url = str(row['orcid_url'].values[0])
        author.human.orcid = row['orcid'].values[0]

    def _attribute_review(self, review: dm.Review, row: list):
        review.presentation_score = row['presentation_score']
        review.commentary_to_author.text = row['commentary_to_author']
        review.commentary_to_chair.text = row['commentary_to_chair']

        if row['presentation_recommendation'] == 'Reject':
            review.presentation_recommend = dm.PRESENTATION_REC_REJECT
        elif row['presentation_recommendation'] == 'Accept':
            review.presentation_recommend = dm.PRESENTATION_REC_ACCEPT
        else:
            review.presentation_recommend = None

        if row['publication_recommendation'] == 'Reject':
            review.publication_recommend = dm.PUBLICATION_REC_REJECT
        elif row['publication_recommendation'] == 'Accept':
            review.publication_recommend = dm.PUBLICATION_REC_ACCEPT
        else:
            review.publication_recommend = None


    def _attribute_reviewer(self, review: dm.Review, row: list):
        review.reviewer.human.name = row['name'].values[0]

        try:
            for alias in row['aliases'].values[0].split(','):
                new_alias = review.reviewer.aliases.add()
                new_alias = alias
        except:
            None

        review.reviewer.human.hash_id = row['hash_id'].values[0]
        review.reviewer.human.current_affiliation.name = row['current_affiliation'].values[0]
        review.reviewer.human.last_degree_affiliation.name = str(row['last_degree_affiliation'].values[0])

        try:
            for affil_name in row['previous_affiliation'].values[0].split(','):
                affiliation = review.reviewer.human.previous_affiliation.add()
                affiliation.name = row['previous_affiliation'].values[0]
        except:
            None

        review.reviewer.human.orcid_url = str(row['orcid_url'].values[0])
        review.reviewer.human.orcid = row['orcid'].values[0]
        review.reviewer.verified = row['verified'].values[0]

    def assemble_paper_book(self):
        for paper_id in self.paper_df.index:
            paper = self.paper_book.paper.add()
            paper_row = self.paper_df.loc[paper_id]
            self._attribute_paper(paper, paper_row)

            for author_id in paper_row.author_ids.split(','):
                human_row = self.human_df.loc[self.human_df['author_id'] == author_id]
                self._attribute_author(paper, paper.authors.add(), human_row)

            paper_review_df = self.review_df.loc[self.review_df['paper_id'] == paper_id]
            paper_review_df.set_index('reviewer_human_hash_id')

            for hash_id in paper_review_df.index:
                review_row = paper_review_df.loc[hash_id]
                reviewer_hash = review_row['reviewer_human_hash_id']
                human_row = self.human_df.loc[self.human_df['hash_id'] == reviewer_hash]
                review = paper.reviews.add()
                self._attribute_review(review, review_row)
                self._attribute_reviewer(review, human_row)

    @staticmethod
    def create_bot(paper_file: str, review_file: str, human_file: str):

        paper_df = pd.read_csv(paper_file, dtype = chandra_bot.PAPER_DICT, index_col = 'paper_id')
        review_df = pd.read_csv(review_file, dtype = chandra_bot.REVIEW_DICT)
        human_df = pd.read_csv(human_file, dtype = chandra_bot.HUMAN_DICT)

        bot = chandra_bot(paper_df = paper_df, review_df = review_df, human_df = human_df)

        return bot

    @staticmethod
    def read_paper_book(input_file: str):
        paper_book = dm.PaperBook()
        try:
            with open(input_file, "rb") as f:
                paper_book.ParseFromString(f.read())
        except IOError:
            print(input_file + ": File not found.")

        bot = chandra_bot(input_paper_book = paper_book)

        return bot

    def write_paper_book(self, output_file: str):
        with open(output_file, "wb") as f:
            f.write(self.paper_book.SerializeToString())
