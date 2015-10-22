from django.db.models import DateField, Func


class JustTheDate(Func):
    """
    Converts a datetime to a date
    """
    function = 'DATE'  # MySQL and SQLite
    output_field = DateField()

    def as_postgresql(self, compiler, connection):
        self.template = '(%(expression)s)::DATE'
        return super().as_sql(compiler, connection)

    def as_oracle(self, compiler, connection):
        self.function = 'TRUNC'
        return super().as_sql(compiler, connection)
