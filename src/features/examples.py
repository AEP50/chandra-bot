from chandra_bot import chandra_bot as cbot

# TODO reorg repo
# TODO make methods via notebook
# TODO make a notebook

cb = cbot.create_bot(
    paper_file = "../../data/processed/fake_paper_series.csv",
    review_file = "../../data/processed/fake_review_series.csv",
    human_file = "../../data/processed/fake_human.csv"
)

cb.assemble_paper_book()

# book_file = "../../data/processed/fake_serialized_paper_book.text"
#
# cb.write_paper_book(output_file = book_file)
