from django.forms.utils import ErrorList


class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ""
        return '<div class="ui list">%s</div>' % "".join(
            ['<div class="item">%s</div>' % e for e in self]
        )
