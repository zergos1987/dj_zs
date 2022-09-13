import os
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.translation import ngettext


def validator_file_size(value): # add this to some file where you can import it from
    megabytes = 2
    limit = megabytes * 1024 * 1024
    if value.size > limit:
        err_msg = _('File too large. Size should not exceed %(megabytes)d MB.') % {'megabytes': megabytes}
        raise ValidationError(err_msg)

def validator_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.txt', '.doc', '.docx']
    valid_extensions_name = _(' '.join(['Text file', 'MS Word']))
    err_msg = _('Unsupported file type. Only {valid_extensions_name} files are allowed.'.format(valid_extensions_name=valid_extensions_name))
    if not ext in valid_extensions:
        raise ValidationError(err_msg)
