class ProductNotFoundError(Exception):
    pass


class InsufficientStockError(Exception):
    pass


class ProductHasOrdersError(Exception):
    pass


class NegativePriceError(Exception):
    pass


class NegativeStockError(Exception):
    pass


class InvalidQuantityError(Exception):
    pass
