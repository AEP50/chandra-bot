from __future__ import print_function

import numpy as np
import pandas as pd
import itertools

from . import chandra_bot_data_model_pb2 as dm

class ChandraBot(object):
    """
    Add description
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

        if row['committee_presentation_decision'].lower() == 'reject':
            paper.committee_presentation_decision = dm.PRESENTATION_REC_REJECT
        elif row['committee_presentation_decision'].lower() == 'accept':
            paper.committee_presentation_decision = dm.PRESENTATION_REC_ACCEPT
        else:
            paper.committee_presentation_decision = dm.PRESENTATION_REC_NONE

        if row['committee_publication_decision'].lower() == 'reject':
            paper.committee_publication_decision = dm.PUBLICATION_REC_REJECT
        elif row['committee_publication_decision'].lower() == 'accept':
            paper.committee_publication_decision = dm.PUBLICATION_REC_ACCEPT
        elif row['committee_publication_decision'].lower() == 'accept_correct':
            paper.committee_publication_decision = dm.PUBLICATION_REC_ACCEPT_CORRECT
        else:
            paper.committee_publication_decision = dm.PUBLICATION_REC_NONE

        if 'abstract' in row:
            paper.abstract.text = row['abstract']
        else:
            paper.abstract.text = 'Missing'

        if 'body' in row:
            paper.body.text = str(row['body'])
        else:
            paper.body.text = 'Missing'

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

        try:
            review.commentary_to_author.text = row['commentary_to_author']
        except:
            review.commentary_to_author.text = ''

        try:
            review.commentary_to_chair.text = row['commentary_to_chair']
        except:
            review.commentary_to_chair.text = ''

        if row['presentation_recommendation'].lower() == 'reject':
            review.presentation_recommend = dm.PRESENTATION_REC_REJECT
        elif row['presentation_recommendation'].lower() == 'accept':
            review.presentation_recommend = dm.PRESENTATION_REC_ACCEPT
        else:
            review.presentation_recommend = dm.PRESENTATION_REC_NONE

        if row['publication_recommendation'].lower() == 'reject':
            review.publication_recommend = dm.PUBLICATION_REC_REJECT
        elif row['publication_recommendation'].lower() == 'accept':
            review.publication_recommend = dm.PUBLICATION_REC_ACCEPT
        else:
            review.publication_recommend = dm.PRESENTATION_REC_NONE


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
        review.reviewer.human.orcid = str(row['orcid'].values[0])
        review.reviewer.verified = bool(row['verified'].values[0])

    def assemble_paper_book(self):
        for paper_id in self.paper_df.index:
            paper = self.paper_book.paper.add()
            paper.number = paper_id
            paper_row = self.paper_df.loc[paper_id]
            self._attribute_paper(paper, paper_row)

            if 'author_ids' in self.paper_df.columns:
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

        paper_df = pd.read_csv(paper_file, dtype = ChandraBot.PAPER_DICT, index_col = 'paper_id')
        review_df = pd.read_csv(review_file, dtype = ChandraBot.REVIEW_DICT)
        human_df = pd.read_csv(human_file, dtype = ChandraBot.HUMAN_DICT)

        bot = ChandraBot(paper_df = paper_df, review_df = review_df, human_df = human_df)

        return bot

    @staticmethod
    def read_paper_book(input_file: str):
        paper_book = dm.PaperBook()
        try:
            with open(input_file, "rb") as f:
                paper_book.ParseFromString(f.read())
        except IOError:
            print(input_file + ": File not found.")

        bot = ChandraBot(input_paper_book = paper_book)
        bot.paper_df = bot.make_dataframe(dataframe_name = 'paper')
        bot.review_df = bot.make_dataframe(dataframe_name = 'review')
        bot.human_df = bot.make_dataframe(dataframe_name = 'human')

        return bot

    def write_paper_book(self, output_file: str):
        with open(output_file, "wb") as f:
            f.write(self.paper_book.SerializeToString())

    def _compute_normalized_scores(self, min_number_reviews: int):
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

                        if row['count'] >= min_number_reviews:
                            review.normalized_present_score = (review.presentation_score - row['mean']) / row['std']
                        else:
                            review.normalized_present_score = None
                    except:
                        None

    def compute_normalized_scores(self, min_number_reviews: int = 10, dataframe_only: bool = False):
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
            self._compute_normalized_scores(min_number_reviews)

    def make_dataframe(self, dataframe_name: str):
        output_df = pd.DataFrame()

        if dataframe_name == 'paper':
            author_id_df = self._make_author_id_df()

            for paper in self.paper_book.paper:
                authors = []
                author_ids = []
                for author in paper.authors:
                    authors.append(author.human.name)
                    author_ids.append(str(author_id_df.loc[author_id_df['hash_id'] == author.human.hash_id]['author_id'].values[0]))

                authors_string = ','.join(authors)
                authors_id_string = ','.join(author_ids)

                row_series = pd.Series({
                                'paper_id': paper.number,
                                'authors': authors_string,
                                'author_ids': authors_id_string,
                                'title': paper.title,
                                'year': paper.year,
                                'committee_presentation_decision': paper.committee_presentation_decision,
                                'committee_publication_decision': paper.committee_publication_decision,
                                'abstract': paper.abstract.text,
                                'body': paper.body.text
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
                                        'commentary_to_author': review.commentary_to_author.text,
                                        'commentary_to_chair': review.commentary_to_chair.text,
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

            output_df = output_df.drop_duplicates().groupby('hash_id').max().reset_index()

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

    def count_former_coauthors(self, dataframe_only: bool = False):
        if dataframe_only:
            df = self.paper_df[['paper_id', 'author_ids']]
            df = (pd.concat([df['paper_id'].reset_index(drop = True), df.author_ids.str.split(',', expand = True)], axis = 1)
                .set_index('paper_id')
                .stack()
                .reset_index(level=[0,1])
                .rename(columns = {0: 'author_id'})
                .drop(columns = ['level_1'])
                .set_index('paper_id')
                .join(self.paper_df[['paper_id', 'year']].set_index('paper_id')))

            h_df = self.human_df.reset_index()[['hash_id', 'author_id']].astype({'author_id': 'int64'})
            auth_df = df.astype({'author_id': 'int64'}).reset_index().merge(h_df, on = 'author_id', how = 'left')

            r_df = self.review_df[['paper_id', 'reviewer_human_hash_id']]
            a_r_pairs_df = auth_df.merge(r_df, on = 'paper_id', how = 'left').groupby(['hash_id', 'reviewer_human_hash_id']).size().reset_index(name = 'count')

            df = auth_df.merge(auth_df, how = 'outer', on = ['paper_id', 'year'], suffixes=('_01', '_02'))
            gb = df[['paper_id', 'year', 'hash_id_01', 'hash_id_02']].groupby(['hash_id_01', 'hash_id_02'])
            a_a_pairs_df = gb.size().to_frame(name = 'papers_written_with_authors').join(gb.agg({'year': 'min'}).rename(columns = {'year': 'year_of_first_collab'})).reset_index()

            conflict_r_df = a_r_pairs_df.merge(a_a_pairs_df, how = 'left', left_on = ['hash_id', 'reviewer_human_hash_id'], right_on = ['hash_id_01', 'hash_id_02']).dropna()

            df = auth_df.merge(r_df, how = 'left', on = 'paper_id')
            df_b = df.merge(conflict_r_df, how = 'left', on = ['hash_id', 'reviewer_human_hash_id']).dropna()
            df_c = df_b[df_b['year_of_first_collab'] <= df_b['year']]
            review_count_df = df_c[['paper_id', 'reviewer_human_hash_id', 'papers_written_with_authors']].reset_index(drop = True)

            self.review_df = self.review_df.merge(review_count_df, how = 'left', on = ['paper_id', 'reviewer_human_hash_id']).fillna(0)

        else:
            pairs_df = pd.DataFrame()
            for paper in self.paper_book.paper:
                a_list = []
                for author in paper.authors:
                    a_list.append(author.human.hash_id)
                pairs = [a_list, a_list]
                data = list(itertools.product(*pairs))
                idx = ['{}'.format(i) for i in range(1, len(data) + 1)]
                df = pd.DataFrame(data, index = idx, columns = list('ab'))
                df = df[df.a != df.b]
                df['year'] = paper.year
                pairs_df = pd.concat([pairs_df, df])

            count_df = pairs_df.groupby(['a','b']).size().reset_index(name = 'paper_count')
            first_df = pairs_df.groupby(['a','b']).min()[['year']].rename(columns = {'year': 'year_first_collab'})
            pairs_df = count_df.join(first_df, on = ['a','b'])

            for paper in self.paper_book.paper:
                a_list = []
                for author in paper.authors:
                    a_list.append(author.human.hash_id)
                for review in paper.reviews:
                    r_hash_id = review.reviewer.human.hash_id
                    df = pairs_df[pairs_df['a'] == r_hash_id]
                    for a in a_list:
                        a_df = df[(df.b == a) & df.year_first_collab <= paper.year]
                        review.papers_written_with_authors += sum(a_df['paper_count'])

    @staticmethod
    def _count_words_in_text(key_words, output_col_name, df, input_col_name):
        look_for = '|'.join(key_words)
        df[output_col_name] = df[input_col_name].str.count(look_for)
        return(df)

    def count_words_in_paper_abstract(self, key_words, column_name: str, dataframe_only: bool = True):
        if dataframe_only:
            self.paper_df = ChandraBot._count_words_in_text(key_words, column_name, self.paper_df, 'abstract')
        else:
            print("dataframe_only must be True")

    def count_words_in_review_commentary(self, key_words, column_name: str, dataframe_only: bool = True):
        if dataframe_only:
            self.review_df = ChandraBot._count_words_in_text(key_words, column_name, self.review_df, 'commentary_to_author')
        else:
            print("dataframe_only must be True")

    def append_verified_reviewer(self, min_count: int, dataframe_only: bool = False):
        if dataframe_only:
            df = pd.merge(self.review_df, self.human_df[['hash_id', 'verified']], how = 'left', left_on = ['reviewer_human_hash_id'], right_on = ['hash_id'])
            df = df.loc[df.verified][['paper_id', 'presentation_score']]
            df = df.groupby('paper_id').agg(n = ('presentation_score', 'size'), mean_verified_score = ('presentation_score', 'mean'))
            df = df.loc[df['n'] >= min_count].reset_index()
            self.review_df = pd.merge(self.review_df, df[['paper_id', 'mean_verified_score']], how = 'left', on = ['paper_id'])
        else:
            for paper in self.paper_book.paper:
                v_list = np.empty((0))
                for review in paper.reviews:
                    if review.reviewer.verified:
                        v_list = np.append(v_list, review.normalized_present_score)
                if len(v_list) > min_count:
                    paper.mean_verified_score = np.mean(v_list)
                else:
                    paper.mean_verified_score = np.nan
