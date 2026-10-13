from json import load, dump
import pathlib
from datetime import date as Date, datetime
from inspect import currentframe, getframeinfo


def get_line_number():
    """Gets the current line number and the filename of the caller.

    Returns:
        tuple: A tuple containing (line_number, filename).
    """
    cf = currentframe().f_back.f_back.f_back.f_back
    filename = getframeinfo(cf).filename
    return cf.f_lineno, filename


project_name = "MiGame"


class Loger:
    """A logger class for handling console and file logging.

    Attributes:
        path (pathlib.Path): The current working directory or the log file path.
        off_log_file (list[str]): A list of filenames to ignore in the logs.
        log_text (str): The accumulated log text for file logging.
        consol_loging (bool): Whether to log to the console.
        file_loging (bool): Whether to log to a file.
        len_string_number (int): Padding for the line number in logs.
        len_log_locate (int): Padding for the filename in logs.
        loging (bool): Whether logging is enabled.
        name (str): The name of the current log file.
    """

    def __init__(self, consol_loging=True, file_loging=True, loging=True):
        """Initializes the Loger instance.

        Args:
            consol_loging (bool): If True, logs will be printed to the console. Defaults to True.
            file_loging (bool): If True, logs will be written to a file. Defaults to True.
            loging (bool): If True, logging is enabled. Defaults to True.
        """
        self.path = pathlib.Path.cwd()

        self.off_log_file = [
            # r'\data\GameSession.py'
        ]
        self.log_text = f"Log file for {project_name}\n\n"

        self.consol_loging = consol_loging
        self.file_loging = file_loging
        self.len_string_number = 3
        self.len_log_locate = 15
        self.loging = loging

        if self.file_loging:
            self._load()

        self.status("Loger init complete")
        if self.off_log_file:
            self.status(f"Bunnet log from\n\t{'\n\t'.join(self.off_log_file)}")
        self.pass_line()

    def _load(self):
        """Loads log configuration and initializes the log file.

        Reads from `data/configs/logs_config.json` to determine the log file name
        based on the date and the number of logs for that day.
        """
        with self.path.joinpath("data/configs/logs_config.json").open("r") as file:
            data = load(file)

        if data["last_date"] == str(Date.today()):
            data['count'] += 1
        else:
            data['last_date'] = str(Date.today())
            data['count'] = 1
        self.name = f"log_{Date.today().strftime('%Y_%m_%d')}_{data['count']}.txt"

        with self.path.joinpath("data/configs/logs_config.json").open("w") as file:
            dump(data, file)

        self.path = self.path.joinpath("logs").joinpath(self.name)
        with self.path.open(mode="w+", encoding="utf-8") as f:
            pass

        self.status(f"Create log file to {self.path}")

    def set_loging(self, loging: bool):
        """Sets whether console logging is enabled.

        Args:
            loging (bool): True to enable console logging, False to disable it.
        """
        self.consol_loging = loging

    def _log_generate(self, *args, tp, time: bool, data: bool, sep: str, end: str):
        """Internal method to generate the formatted log message.

        Args:
            *args: Arguments to be included in the log message.
            tp (int): The type of log (1: Log, 2: Status, 3: Error, else: Unknown).
            time (bool): Whether to include the current timestamp.
            data (bool): Whether to include line number and filename.
            sep (str): Separator between log arguments.
            end (str): Ending characters for the log message.

        Returns:
            str: The formatted log message.
        """
        if tp == 1:
            st_tp = "[L]"
        elif tp == 2:
            st_tp = "[S]"
        elif tp == 3:
            st_tp = "[E]"
        else:
            st_tp = f"[?{tp}]"

        log = f"{sep.join(map(str, args))}{end}"

        if time:
            log_time = f"{datetime.now()} | "
        else:
            log_time = ""

        if data:
            number_str, nf = get_line_number()
            if "src" in nf:
                name_file = nf.split('src')[1]
            elif "libs" in nf:
                name_file = nf.split('libs')[1]
            else:
                name_file = nf
            if name_file in self.off_log_file:
                return
            log_data = f"{number_str: >{self.len_string_number}}, {name_file: <{self.len_log_locate}} | "
        else:
            log_data = ""

        log = f"{st_tp} {log_time}{log_data}>> {log}"
        return log

    def _save_log(self, log):
        """Writes the log message to the log file.

        Args:
            log (str): The formatted log message.
        """
        if self.file_loging:
            self.log_text += log
            with self.path.open(mode="w", encoding="utf-8") as f:
                f.write(self.log_text)

    def _log_data(self, *args, tp, time=True, data=True, sep=" ", end="\n"):
        """Internal method to handle the logging process.

        Args:
            *args: Arguments for the log message.
            tp: The type of log.
            time (bool): Include timestamp.
            data (bool): Include line info.
            sep (str): Separator.
            end (str): End character.
        """
        log = self._log_generate(*args, tp=tp, time=time, data=data, sep=sep, end=end)

        if log is not None:
            if self.consol_loging:
                print(log, end="")

            self._save_log(log)

    def log(self, *args, time=True, data=True, sep=" ", end="\n"):
        """Logs an informational message.

        Args:
            *args: Arguments for the log message.
            time (bool): Include timestamp.
            data (bool): Include line info.
            sep (str): Separator.
            end (str): End character.
        """
        if self.loging:
            self._log_data(*args, tp=1, time=time, data=data, sep=sep, end=end)

    def status(self, *args, time=True, data=False, sep=" ", end="\n"):
        """Logs a status message.

        Args:
            *args: Arguments for the status message.
            time (bool): Include timestamp.
            data (bool): Include line info.
            sep (str): Separator.
            end (str): End character.
        """
        self._log_data(*args, tp=2, time=time, data=data, sep=sep, end=end)

    def error(self, *args, time=True, data=True, sep=" ", end="\n"):
        """Logs an error message.

        Args:
            *args: Arguments for the error message.
            time (bool): Include timestamp.
            data (bool): Include line info.
            sep (str): Separator.
            end (str): End character.
        """
        self._log_data(*args, tp=3, time=time, data=data, sep=sep, end=end)

    def pass_line(self, n=1):
        """Prints and saves a few empty lines.

        Args:
            n (int): Number of lines to print. Defaults to 1.
        """
        log = "\n" * n
        print(log, end="")
        self._save_log(log)


loger = Loger(file_loging=False)

log = loger.log
log_step = loger.pass_line
