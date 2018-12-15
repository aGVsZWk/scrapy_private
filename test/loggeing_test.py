
import logging
# # 日志的五个等级，等级依次递增
# # 默认是WARNING等级
# logging.DEBUG
# logging.INFO
# logging.WARNING
# logging.ERROR
# logging.CRITICAL
# # 设置日志等级
logging.basicConfig(level=logging.INFO)
# # # 使用
logging.debug('DEBUG')
logging.info('INFO')
logging.warning('WARNING')
logging.error('ERROR')
logging.critical('CRITICAL')

# try:
#     raise Exception("python16")
# except Exception as e:
#     logging.exception(e)



