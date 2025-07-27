enum LogLevel { debug, info, warning, error }

class LOG {
  static void DEBUG(Object? message) => _log(LogLevel.debug, message);
  static void INFO(Object? message) => _log(LogLevel.info, message);
  static void WARNING(Object? message) => _log(LogLevel.warning, message);
  static void ERROR(Object? message) => _log(LogLevel.error, message);

  static void _log(LogLevel level, Object? message) {
    // ANSI color codes
    const reset = '\x1B[0m';
    const gray = '\x1B[97m';
    const blue = '\x1B[34m';
    const yellow = '\x1B[33m';
    const red = '\x1B[31m';
    final prefix = {
      LogLevel.debug: '[DEBUG]',
      LogLevel.info: '[INFO]',
      LogLevel.warning: '[WARNING]',
      LogLevel.error: '[ERROR]',
    }[level];
    final color = {
      LogLevel.debug: gray,
      LogLevel.info: blue,
      LogLevel.warning: yellow,
      LogLevel.error: red,
    }[level];
    // ignore: avoid_print
    print('$color$prefix $message$reset');
  }
}
