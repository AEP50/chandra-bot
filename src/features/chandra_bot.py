from __future__ import print_function
import chandra_bot_data_model_pb2 as dm
import numpy as np
import pandas as pd

class chandra_bot(object):
    """
    a class for data model
    """

    PAPER_DICT = {
        'paper_id': pd.StringDtype(),
        'authors': pd.StringDtype(),
        'author_ids': pd.StringDtype(),
        'title': pd.StringDtype(),
        'year': np.int32,
        'committee_publication_decision': pd.StringDtype(),
        'committee_presentation_decision': pd.StringDtype(),
        'abstract': pd.StringDtype(),
        'body': pd.StringDtype()
    }

    REVIEW_DICT = {
        'paper_id': pd.StringDtype(),
        'presentation_score': np.int32,
        'commentary_to_author': pd.StringDtype(),
        'commentary_to_chair': pd.StringDtype(),
        'reviewer_human_hash_id': pd.StringDtype(),
        'presentation_recommend': pd.StringDtype(),
        'publication_recommend': pd.StringDtype()
    }

    HUMAN_DICT = {
        'name': pd.StringDtype(),
        'aliases': pd.StringDtype(),
        'hash_id': pd.StringDtype(),
        'current_affiliation': pd.StringDtype(),
        'previous_affiliation': pd.StringDtype(),
        'last_degree_affiliation': pd.StringDtype(),
        'orcid_url': pd.StringDtype(),
        'orcid': pd.StringDtype(),
        'author_id': pd.StringDtype(),
        'verified': 'bool'
    }

    NORMALIZE_SCORE_MIN_REVIEWS = 10

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
            self.paper_book: dm.PaperBook = input_paper_book

            # self.paper_df = self.make_dataframe(dataframe_name = 'paper')
            # self.review_df = self.make_dataframe('review')
            # self.human_df = self.make_dataframe('human')

    def _attribute_paper(self, paper: dm.Paper, row: list) -> None:

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
        review.reviewer.verified = bool(row['verified'].values[0])

    def assemble_paper_book(self):
        for paper_id in self.paper_df.index:
            paper = self.paper_book.paper.add()
            paper.number = paper_id
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
        bot.paper_df = bot.make_dataframe(dataframe_name = 'paper')

        return bot

    def write_paper_book(self, output_file: str):
        with open(output_file, "wb") as f:
            f.write(self.paper_book.SerializeToString())

    def _compute_normalized_scores(self):
        scores_df = pd.DataFrame()
        for paper in self.paper_book.paper:
            for review in paper.reviews:
                row_series = pd.Series({
                                    "paper_id": paper.number,
                                    "reviewer_id": review.reviewer.human.hash_id,
                                    "score": review.presentation_score
                })
                row_df = pd.DataFrame([row_series])
                scores_df = pd.concat([scores_df, row_df], ignore_index = True)

        mean_df = scores_df.groupby('reviewer_id').mean()[['score']].rename(columns = {'score': 'mean'})
        std_df = scores_df.groupby('reviewer_id').std()[['score']].rename(columns = {'score': 'std'})
        count_df = scores_df.groupby('reviewer_id').count()[['score']].rename(columns = {'score': 'count'})
        normalized_df = mean_df.join(std_df, on = 'reviewer_id').join(count_df, on = 'reviewer_id')

        matched_reviewer = []
        for paper in self.paper_book.paper:
            for review in paper.reviews:
                hash_id = review.reviewer.human.hash_id
                if hash_id in matched_reviewer:
                    None
                else:
                    matched_reviewer.append(hash_id)
                    try:
                        row = normalized_df.loc[hash_id]
                        review.reviewer.mean_present_score = row['mean']
                        review.reviewer.std_dev_present_score = row['std']
                        review.reviewer.number_of_reviews = int(row['count'])

                        if row['count'] >= self.NORMALIZE_SCORE_MIN_REVIEWS:
                            review.normalized_present_score = (review.presentation_score - row['mean']) / row['std']
                        else:
                            review.normalized_present_score = None
                    except:
                        None

    def compute_normalized_scores(self, dataframe_only: bool = False):
        if dataframe_only:
            df = self.review_df
            mean_df = df.groupby('reviewer_human_hash_id').mean()[['presentation_score']].rename(columns = {'presentation_score': 'mean'})
            std_df = df.groupby('reviewer_human_hash_id').std()[['presentation_score']].rename(columns = {'presentation_score': 'std'})
            count_df = df.groupby('reviewer_human_hash_id').count()[['presentation_score']].rename(columns = {'presentation_score': 'count'})
            normalized_df = mean_df.join(std_df, on = 'reviewer_human_hash_id').join(count_df, on = 'reviewer_human_hash_id')

            df = df.join(normalized_df, on = 'reviewer_human_hash_id')
            df['normalized_present_score'] = (df['presentation_score'] - df['mean'])/df['std']
            df = df.rename(columns = {'mean': 'mean_present_score', 'std': 'std_dev_present_score', 'count': 'number_of_reviews'})
            self.review_df = df
        else:
            self._compute_normalized_scores()

    def make_dataframe(self, dataframe_name: str):
        output_df = pd.DataFrame()

        if dataframe_name == 'paper':
            author_id_df = self._make_author_id_df()

            for paper in self.paper_book.paper:
                authors = []
                author_ids = []
                for author in paper.authors:
                    authors.append(author.human.name)
                    author_ids.append(author_id_df.loc[author_id_df['hash_id'] == author.human.hash_id]['author_id'].values[0])

                authors_string = ','.join(authors)
                authors_id_string = ','.join(str(author_ids))

                row_series = pd.Series({
                                'paper_id': paper.number,
                                'authors': authors_string,
                                'author_ids': authors_id_string,
                                'title': paper.title,
                                'year': paper.year,
                                'committee_presentation_decision': paper.committee_presentation_decision,
                                'committee_publication_decision': paper.committee_publication_decision,
                                'abstract': paper.abstract,
                                'body': paper.body
                })
                row_df = pd.DataFrame([row_series])
                output_df = pd.concat([output_df, row_df], ignore_index = True)

        elif dataframe_name == 'review':
            for paper in self.paper_book.paper:
                for review in paper.reviews:
                    reviewer = review.reviewer
                    row_series = pd.Series({
                                        'paper_id': paper.number,
                                        'presentation_score': review.presentation_score,
                                        'commentary_to_author': review.commentary_to_author,
                                        'commentary_to_chair': review.commentary_to_chair,
                                        'reviewer_human_hash_id': review.reviewer.human.hash_id,
                                        'presentation_recommendation': review.presentation_recommend,
                                        'publication_recommendation': review.publication_recommend,
                                        'normalized_present_score': review.normalized_present_score
                    })
                    row_df = pd.DataFrame([row_series])
                    output_df = pd.concat([output_df, row_df], ignore_index = True)
        elif dataframe_name == 'human':
            author_id_df = self._make_author_id_df()
            for paper in self.paper_book.paper:
                authors_df = pd.DataFrame()
                for author in paper.authors:
                    author_id = author_id_df.loc[author_id_df['hash_id'] == author.human.hash_id]['author_id'].values[0]
                    alias_str = ','.join(author.human.aliases)
                    affil_list = []
                    for affil in author.human.previous_affiliation:
                        affil_list.append(affil)
                    row_series = pd.Series({
                                        'name': author.human.name,
                                        'aliases': alias_str,
                                        'hash_id': author.human.hash_id,
                                        'current_affiliation': author.human.current_affiliation.name,
                                        'previous_affiliation': ','.join(affil_list),
                                        'last_degree_affiliation': author.human.last_degree_affiliation.name,
                                        'orcid_url': author.human.orcid_url,
                                        'orcid': author.human.orcid,
                                        'author_id': author_id
                    })
                    row_df = pd.DataFrame([row_series])
                    authors_df = pd.concat([authors_df, row_df], ignore_index = True)

                reviewers_df = pd.DataFrame()
                for review in paper.reviews:
                    reviewer = review.reviewer
                    alias_str = ','.join(reviewer.human.aliases)
                    affil_list = []
                    for affil in reviewer.human.previous_affiliation:
                        affil_list.append(affil.name)
                    row_series = pd.Series({
                                        'name': reviewer.human.name,
                                        'aliases': alias_str,
                                        'hash_id': reviewer.human.hash_id,
                                        'current_affiliation': reviewer.human.current_affiliation.name,
                                        'previous_affiliation': ','.join(affil_list),
                                        'last_degree_affiliation': reviewer.human.last_degree_affiliation.name,
                                        'orcid_url': reviewer.human.orcid_url,
                                        'orcid': reviewer.human.orcid,
                                        'verified': reviewer.verified
                    })
                    row_df = pd.DataFrame([row_series])
                    reviewers_df = pd.concat([reviewers_df, row_df], ignore_index = True)

                r_join_df = reviewers_df[['hash_id', 'verified']].set_index('hash_id')
                a_df = authors_df.set_index('hash_id').join(r_join_df, on = 'hash_id')

                a_join_df = authors_df[['hash_id', 'author_id']].set_index('hash_id')
                b_df = reviewers_df.set_index('hash_id').join(a_join_df, on = 'hash_id')

                a_b_df = pd.concat([a_df, b_df])
                output_df = pd.concat([output_df, a_b_df])

            output_df.drop_duplicates().groupby('hash_id').max()

        else:
            print("dataframe_name must be 'paper', 'review', or 'human'")

        return output_df

    def _make_author_id_df(self):
        list = []
        for paper in self.paper_book.paper:
            for author in paper.authors:
                if author.human.hash_id not in list:
                    list.append(author.human.hash_id)
        df = pd.DataFrame({'hash_id': list})
        df['author_id'] = np.arange(len(df)) + 1

        return(df)
