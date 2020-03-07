from data_model import DataModel

# test reading from raw input and writing to pbf
datamodel = DataModel.create_datamodel(
    paper_file = "C:/Users/wangs1/Documents/cbot/data/processed/fake_paper_series.csv"
)
datamodel.write_pbf()


# test reading from existing pbf
datamodel = DataModel.create_datamodel(
    existing_paper_book_file = "C:/Users/wangs1/Documents/cbot/src/paper_book.txt"
)

for paper in datamodel.paper_book.paper[:10]:
    print("paper title: ", paper.title)
    for author in paper.authors:
        print("paper author name: ", author.human.name)
        print("paper author hash_id: ", author.human.hash_id)
