from chandra_bot import chandra_bot as cbot

print('Creating bot')
bot = cbot.create_bot(
    paper_file = "../../data/processed/small_fake_paper_series.csv",
    review_file = "../../data/processed/small_fake_review_series.csv",
    human_file = "../../data/processed/small_fake_human.csv"
)
print('Assembling the paper book')
bot.assemble_paper_book()

print('Computing normalized scores')
bot.compute_normalized_scores()

print('Computing normalized scores (via dataframes)')
bot.compute_normalized_scores(dataframe_only = True)

print('Writing paper book to disk')
book_file = "../../data/processed/fake_serialized_paper_book.text"
bot.write_paper_book(output_file = book_file)

print('Read paper book from disk')
bot = cbot.read_paper_book(book_file)

print('Make a paper dataframe')
paper_out_df = bot.make_dataframe('paper')
review_out_df = bot.make_dataframe('review')
human_out_df = bot.make_dataframe('human')
