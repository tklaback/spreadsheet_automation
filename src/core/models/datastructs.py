from dataclasses import dataclass

@dataclass
class ReviewApiInfo:
    account_id: str
    location_id: str
    access_token: str

@dataclass
class Review:
    id: str
    author: str
    rating: int
    time: str
    comment: str

    def convert_to_list(self) -> list:
        return [self.id, self.author, self.rating, self.time, self.comment]

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

@dataclass
class SpreadsheetInfo:
    spreadsheet_id: str
    value_input_option: str