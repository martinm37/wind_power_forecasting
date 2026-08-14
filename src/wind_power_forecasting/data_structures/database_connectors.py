from pydantic import BaseModel, ConfigDict


class MySQLConnectionData(BaseModel):
    """
    Data structure containing all of the data necessary
    to establish an connection with a MySQL database.
    """

    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    user: str
    password: str
    host: str
    port: int
    database: str
    datatable: str

