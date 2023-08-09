from enum import Enum

class HttpErrorsEnum(Enum):
    # USER ERRORS
    USER_NOT_FOUND = 'user-not-found'
    USER_ALREADY_EXIST = 'user-already-exist'
    USER_CREATION_FAILED = 'user-creation-failed'
    USER_LICENCE_TYPE_ERROR = 'user-licence-type-error'

    # ORDER ERRORS
    ORDER_NOT_FOUND = 'order-not-found'
    YOU_DO_NOT_OWN_THIS_ORDER = 'you-do-not-own-this-order'

    # LICENCE ERRORS
    LICENCE_NOT_FOUND = 'licence-not-found'
    LICENCE_ALREADY_USED = 'licence-already-used'
    LICENCE_NOT_AVAILABLE = 'licence-not-available'
    ERROR_WHILE_GENERATING_SERIAL_NUMBER = 'error-while-generating-serial-number'

    # TICKET ERRORS
    TICKET_NOT_FOUND = 'ticket-not-found'
    TICKET_ALREADY_CLOSED = 'ticket-already-closed'
    YOU_DO_NOT_OWN_THIS_TICKET = 'you-do-not-own-this-ticket'

    # SELLER ERRORS
    SELLER_NOT_FOUND = 'seller-not-found'

    # FILE UPLOAD
    ERROR_WHILE_UPLOADING_FILE = 'error-while-uploading-file'
