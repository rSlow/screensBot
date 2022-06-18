import logging


async def on_startup(_):
    try:
        import handlers
    except ImportError as ex:
        logging.warning("Error with importing handlers!")
        raise ex
