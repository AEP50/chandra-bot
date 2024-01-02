from typing import List
from pydantic import BaseModel, Field

class PresentationRecEnum(BaseModel):
    """Enum for presentation recommendation."""
    PRESENTATION_REC_REJECT: int = 0
    PRESENTATION_REC_ACCEPT: int = 1
    PRESENTATION_REC_NONE: int = 2

class PublicationRecEnum(BaseModel):
    """Enum for publication recommendation."""
    PUBLICATION_REC_REJECT: int = 0
    PUBLICATION_REC_ACCEPT: int = 1
    PUBLICATION_REC_ACCEPT_CORRECT: int = 2
    PUBLICATION_REC_NONE: int = 3

class Affiliation(BaseModel):
    """
    Represents an affiliation with a name and aliases.

    Variables:
    - name (str): The name of the affiliation.
    - aliases (List[str]): A list of alternative names or aliases for the affiliation.
    """
    name: str
    aliases: List[str]

class Human(BaseModel):
    """
    Represents a human with various attributes.

    Variables:
    - name (str): The name of the human.
    - aliases (List[str]): A list of alternative names or aliases for the human.
    - hash_id (str): The hash ID associated with the human.
    - current_affiliation (Affiliation): The current affiliation of the human.
    - previous_affiliation (List[Affiliation]): A list of previous affiliations of the human.
    - last_degree_affiliation (Affiliation): The last degree affiliation of the human.
    - orcid_url (str): The URL of the ORCID profile of the human.
    - orcid (str): The ORCID identifier of the human.
    """

    name: str
    aliases: List[str]
    hash_id: str
    current_affiliation: Affiliation
    previous_affiliation: List[Affiliation]
    last_degree_affiliation: Affiliation
    orcid_url: str
    orcid: str

class Author(BaseModel):
    """
    Represents an author with human information.

    Variables:
    - human (Human): The information about the author as a human.
    """
    human: Human

class Reviewer(BaseModel):
    """
    Represents a reviewer with specific review-related attributes.

    Variables:
    - human (Human): The information about the reviewer as a human.
    - verified (bool): Indicates whether the reviewer is verified.
    - mean_present_score (float): The mean presentation score given by the reviewer.
    - std_dev_present_score (float): The standard deviation of presentation scores given by the reviewer.
    - number_of_reviews (int): The total number of reviews conducted by the reviewer.
    - assigned_reviews_not_complete (int): The number of assigned reviews not yet completed by the reviewer.
    """
    human: Human
    verified: bool
    mean_present_score: float
    std_dev_present_score: float
    number_of_reviews: int
    assigned_reviews_not_complete: int

class Content(BaseModel):
    """
    Represents content with information about spelling, grammar, and text.

    Variables:
    - human (Human): The information about the individual who provided the content.
    - spelling_errors (int): The number of spelling errors in the content.
    - grammar_score (float): The grammar score of the content.
    - text (str): The text content.
    """
    human: Human
    spelling_errors: int
    grammar_score: float
    text: str

class Review(BaseModel):
    """
    Represents a review with reviewer information and review details.

    Variables:
    - reviewer (Reviewer): The information about the reviewer.
    - presentation_score (float): The presentation score given in the review.
    - normalized_present_score (float): The normalized presentation score.
    - commentary_to_author (Content): The commentary provided to the author.
    - commentary_to_chair (Content): The commentary provided to the chair.
    - papers_written_with_authors (int): The number of papers written with the authors of the reviewed paper.
    - presentation_recommend (PresentationRecEnum): The presentation recommendation from the committee.
    - publication_recommend (PublicationRecEnum): The publication recommendation from the committee.
    """
    reviewer: Reviewer
    presentation_score: float
    normalized_present_score: float
    commentary_to_author: Content
    commentary_to_chair: Content
    papers_written_with_authors: int
    presentation_recommend: PresentationRecEnum
    publication_recommend: PublicationRecEnum

class Paper(BaseModel):
    """
    Represents a paper with details like title, authors, reviews, etc.

    Variables:
    - number (str): The identification number of the paper.
    - authors (List[Author]): The list of authors associated with the paper.
    - reviews (List[Review]): The list of reviews received by the paper.
    - title (str): The title of the paper.
    - year (int): The year of publication.
    - committee_presentation_decision (PresentationRecEnum): The presentation decision made by the committee.
    - committee_publication_decision (PublicationRecEnum): The publication decision made by the committee.
    - abstract (Content): The content representing the abstract of the paper.
    - body (Content): The content representing the body of the paper.
    - mean_verified_score (float): The mean verified score of the paper.
    """
    number: str
    authors: List[Author]
    reviews: List[Review]
    title: str
    year: int
    committee_presentation_decision: PresentationRecEnum
    committee_publication_decision: PublicationRecEnum
    abstract: Content
    body: Content
    mean_verified_score: float

class PaperBook(BaseModel):
    """
    Represents a collection of papers.

    Variables:
    - paper (List[Paper]): The list of papers in the paper book.
    """
    paper: List[Paper]
