from django.utils.translation import ugettext, ugettext_lazy as _

class City(object):
    SM = 'sm'
    GR = 'gr'

    CHOICES = (
        (SM, _("Saint-Martin-d'Hères")),
        (GR, _('Grenoble')),
    )


class FlatType(object):
    F = 'f'
    H = 'h'

    CHOICES = (
        (F, _('flat')),
        (H, _('house')),
    )


class GES(object):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'
    G = 'G'
    H = 'H'
    I = 'I'

    CHOICES = (
        (A, _('<5')),
        (B, _('6 to 10')),
        (C, _('11 to 20')),
        (D, _('21 to 35')),
        (E, _('36 to 55')),
        (F, _('56 to 80')),
        (G, _('81 to 110')),
        (H, _('110 to 145')),
        (I, _('>145')),
    )


class Energy(object):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'
    G = 'G'
    H = 'H'
    I = 'I'

    CHOICES = (
        (A, _('<50')),
        (B, _('51 to 90')),
        (C, _('91 to 150')),
        (D, _('151 to 230')),
        (E, _('231 to 330')),
        (F, _('331 to 450')),
        (G, _('451 to 590')),
        (H, _('591 to 750')),
        (I, _('>750')),
    )

