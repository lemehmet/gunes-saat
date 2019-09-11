import logging

# TODO: There must be a better way to initialize common objects

logging.basicConfig(format='%(asctime)s %(funcName)s@%(threadName)s: %(message)s',
                    datefmt='%m-%d %H:%M:%S',
                    # filename='./saat.log', filemode='w',
                    level=logging.WARNING)
# console = logging.StreamHandler()
# console.setLevel(logging.DEBUG)
# logging.getLogger('').addHandler(console)

log_fw = logging.getLogger("framework")
log_fw.setLevel(logging.INFO)

log_paint = logging.getLogger("paint")
log_paint.setLevel(logging.INFO)

log_view = logging.getLogger("view")
log_view.setLevel(logging.DEBUG)
