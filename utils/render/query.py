import sqlparse
import sqlalchemy
from sqlalchemy.dialects import postgresql


def render_query(statement: sqlalchemy.sql.expression.Selectable):
    return sqlparse.format(
        str(statement.compile(
            dialect=postgresql.dialect(),
            compile_kwargs={"literal_binds": True}
        )), reindent=True, keyword_case="lower",
    )
