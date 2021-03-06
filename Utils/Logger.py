from operator import itemgetter
"""
Logging class that handles formatting of Errors, Warnings, and Anomalies in a standard format.
Also handles ensuring that the logs are printed in the correct groupings per the expected formatting

Class should be used in the default design pattern, where the same instance is shared unless an object has a
specific reason for having its own instance. Class should be inputted through dependency injection to allow
for unit test ability.
"""


class Logger:
    """
    Inner data class to logger to represent an individual log entry
    This data class handles knowing how to sort itself and converting to a proper string format
    """

    class Log:
        level = ""
        collection = ""
        use_case = ""
        error_message = ""
        _use_case_label = "US"

        def __init__(self, level, collection, use_case, error_message):
            self.level = level
            self.collection = collection
            self.use_case = use_case
            self.error_message = error_message

        def __lt__(self, other):
            return self.collection < other.collection

        def __str__(self):
            return "{}: {}: {}{:02d}: {}".format(self.level,
                                                 self.collection,
                                                 self._use_case_label,
                                                 self.use_case,
                                                 self.error_message)

    # Defines for labels and collections for creating logs
    _error_label = "Error"
    _anomaly_label = "Anomaly"
    _warning_label = "Warning"
    _info_label = "Info"

    _individual_collection = "Individual"
    _family_collection = "Family"

    _outputMessages = []
    _backlog = [1, 7, 17, 18, 29, 23, 24, 32, 2, 3, 30, 31, 42, 33, 38, 11, 4, 5, 16,
                39, 21, 13, 12, 19, 6, 10, 14, 15, 35, 28, 34, 36]
    _catched = []

    def _log(self, level, collection, use_case, error_message):
        """
        Private log function to create the wrapper
        :param level: < Warning | Anomaly | Error >  The level of the warning
        :param collection: Which database collection the error derives from
        :param use_case: The user story which is validating this bounds, 0 if not a user story
        :param error_message: The custom formatted error message from the class
        :return: None
        """
        self._outputMessages.append((level, collection, use_case, error_message))
        self._catched.append(use_case)

    def team_use(self):
        for case in self._backlog:
            if case not in self._catched:
                print("US ", case, " unfinished")

    # Public Wrapper functions to increase readability from calling code

    def log_individual_error(self, use_case, error_message):
        self._log(self._error_label, self._individual_collection, use_case, error_message)

    def log_individual_anomaly(self, use_case, error_message):
        self._log(self._anomaly_label, self._individual_collection, use_case, error_message)

    def log_individual_warning(self, use_case, error_message):
        self._log(self._warning_label, self._individual_collection, use_case, error_message)

    def log_individual_info(self, use_case, error_message):
        self._log(self._info_label, self._individual_collection, use_case, error_message)

    def log_family_error(self, use_case, error_message):
        self._log(self._error_label, self._family_collection, use_case, error_message)

    def log_family_anomaly(self, use_case, error_message):
        self._log(self._anomaly_label, self._family_collection, use_case, error_message)

    def log_family_warning(self, use_case, error_message):
        self._log(self._warning_label, self._family_collection, use_case, error_message)

    def log_family_info(self, use_case, error_message):
        self._log(self._info_label, self._family_collection, use_case, error_message)

    def log_error(self, use_case, is_individual, error_message):
        self._log(self._error_label, self._individual_collection if is_individual else self._family_collection,
                  use_case, error_message)

    def print_log(self):
        self._outputMessages.sort(key=itemgetter(2, 0))
        for log_entry in self._outputMessages:
            print("{}".format(Logger.Log(log_entry[0], log_entry[1], log_entry[2], log_entry[3])))

    def get_logs(self):
        self._outputMessages.sort(key=itemgetter(2, 0))
        return self._outputMessages

    def clear_logs(self):
        self._outputMessages = []
