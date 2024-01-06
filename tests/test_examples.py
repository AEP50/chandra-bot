import os

import pytest

from chandra_bot import ChandraBot as cbot

example_dir = os.path.join(os.getcwd(), "examples")


@pytest.mark.travis
def test():
    print("Creating bot")
    bot = cbot.create_bot(
        paper_file=os.path.join(example_dir, "small_fake_paper_series.csv"),
        review_file=os.path.join(example_dir, "small_fake_review_series.csv"),
        human_file=os.path.join(example_dir, "small_fake_human.csv"),
    )
    print("Assembling the paper book")
    bot.assemble_paper_book()

    print("Computing normalized scores")
    bot.compute_normalized_scores()

    print("Computing normalized scores (via dataframes)")
    bot.compute_normalized_scores(dataframe_only=True)

    print("Writing paper book to disk")
    book_file = os.path.join(example_dir, "fake_serialized_paper_book.text")
    bot.write_paper_book(output_file=book_file)

    print("Read paper book from disk")
    bot = cbot.read_paper_book(book_file)

    # this test is redundant as the read_paper_book above calls make_dataframe()
    # print("Make dataframes")
    # paper_out_df = bot.make_dataframe("paper")
    # review_out_df = bot.make_dataframe("review")
    # human_out_df = bot.make_dataframe("human")

    print("Count former co-authors")
    bot.count_former_coauthors()

    print("Count former co-authors (via dataframes)")
    bot.count_former_coauthors(dataframe_only=True)

    print("Mean verified review score")
    bot.append_verified_reviewer(min_count=2, dataframe_only=False)

    print("Mean verified review score (via dataframes)")
    bot.append_verified_reviewer(min_count=2, dataframe_only=True)


if __name__ == "__main__":
    test()