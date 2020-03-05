from __future__ import print_function
import chandra_bot_pb2
import sys
import pandas as pd
from typing import Optional

class DataModel(object):
    """
    a class for data model
    """

    def __init__(
        self,
        paper_book : None,
        human_book : None,
        university_book : None,
        author_book : None,
        reviewer_book : None,
        review_book : None,
        content_book : None
    ):
        """
        constructor
        """

        self.paper_book = paper_book
        self.human_book = human_book
        self.university_book = university_book
        self.author_book = author_book
        self.reviewer_book = reviewer_book
        self.review_book = review_book
        self.content_book = content_book


    @staticmethod
    def create_datamodel(
        existing_paper_book_file: Optional[str] = None,
        paper_file: Optional[str] = None,
        review_file: Optional[str] = None,
    ):

        paper_book = chandra_bot_pb2.PaperBook()
        human_book = chandra_bot_pb2.HumanBook()
        university_book = chandra_bot_pb2.UniversityBook()
        author_book = chandra_bot_pb2.AuthorBook()
        reviewer_book = chandra_bot_pb2.ReviewerBook()
        review_book = chandra_bot_pb2.ReviewBook()
        content_book = chandra_bot_pb2.ContentBook()

        if paper_file:
            input_df = pd.read_csv(paper_file)
        elif review_file:
            input_df = pd.read_csv(review_file)
        elif existing_paper_book_file:
            paper_book = DataModel.read_pdf(existing_paper_book_file)
            input_df = pd.DataFrame()
        else:
            print("!!no input specified!!")
            input_df = None

        if len(input_df) > 0:
            # move to parameter.py
            raw_to_model_df = pd.read_csv("C:/Users/wangs1/Documents/cbot/references/raw_to_model.csv")
            raw_to_model_dict = dict(zip(raw_to_model_df.raw, raw_to_model_df.model))

            for c in input_df.columns:
                if c in list(raw_to_model_dict.keys()):
                    input_df.rename(
                        columns = {c: raw_to_model_dict[c]},
                        inplace = True
                    )

            for i in input_df.index:
                DataModel.generate_paper(
                    paper_book.paper.add(),
                    input_df.loc[i]
                )

        datamodel = DataModel(
            paper_book = paper_book,
            human_book = human_book,
            university_book = university_book,
            author_book = author_book,
            reviewer_book = reviewer_book,
            review_book = review_book,
            content_book = content_book
        )

        return datamodel


    @staticmethod
    def generate_paper(
        paper,
        row
        ):
        paper.title = row.title
        paper.year = row.year

        author = paper.authors.add()
        author.human.name = row.firstname + " " + row.lastname
        author.human.hash_id = row.hash_id


    def write_pbf(self):
        """
        write out books to pbf

        file paths should be moved to parameter.py
        """

        """
        paper_book_file = self.parameter.DEFAULT_PAPER_BOOK_FILE
        human_book_file = self.parameter.DEFAULT_HUMAN_BOOK_FILE
        university_book_file = self.parameter.DEFAULT_UNIVERSITY_BOOK_FILE
        author_book_file = self.parameter.DEFAULT_AUTHOR_BOOK_FILE
        reviewer_book_file = self.parameter.DEFAULT_REVIEWER_BOOK_FILE
        review_book_file = self.parameter.DEFAULT_REVIEW_BOOK_FILE
        content_book_file = self.parameter.DEFAULT_CONTENT_BOOK_FILE
        """

        paper_book_file = "C:/Users/wangs1/Documents/cbot/src/paper_book.txt"

        with open(paper_book_file, "wb") as f:
            f.write(self.paper_book.SerializeToString())


    @staticmethod
    def read_pdf(path):
        """
        read existing pbf

        """

        """
        paper_book_file = self.parameter.DEFAULT_PAPER_BOOK_FILE
        human_book_file = self.parameter.DEFAULT_HUMAN_BOOK_FILE
        university_book_file = self.parameter.DEFAULT_UNIVERSITY_BOOK_FILE
        author_book_file = self.parameter.DEFAULT_AUTHOR_BOOK_FILE
        reviewer_book_file = self.parameter.DEFAULT_REVIEWER_BOOK_FILE
        review_book_file = self.parameter.DEFAULT_REVIEW_BOOK_FILE
        content_book_file = self.parameter.DEFAULT_CONTENT_BOOK_FILE
        """
        paper_book = chandra_bot_pb2.PaperBook()

        paper_book_file = "C:/Users/wangs1/Documents/cbot/src/paper_book.txt"

        try:
          with open(paper_book_file, "rb") as f:
            paper_book.ParseFromString(f.read())
        except IOError:
          print(paper_book_file + ": File not found.  Creating a new file.")

        return paper_book
