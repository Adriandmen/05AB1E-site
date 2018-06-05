import subprocess
import random
import hashlib
import os
import signal

# Windows process creation flags
CREATE_NO_WINDOW = 0x08000000
MAX_BYTE_SIZE = 2 ** 16


class Command(object):

    @staticmethod
    def run(timeout, code_file, input_file) -> (str, bool, bool):
        """
        Runs the program where the source code is located in the 'code_file' file and the input
        in the 'input file' file. The timeout specifies the number of seconds the process gives
        for the program to run before it terminates.
        :param timeout: The number of seconds before the program times out.
        :param code_file: The file name where the source code is located at.
        :param input_file: The file name where the input is located at
        :return:
        """

        # Check for cross operating system
        if os.name == "posix":
            cmd = "python3 lib/05AB1E/osabie.py --safe {} < {}".format(code_file, input_file)
            process = subprocess.Popen(cmd, shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       preexec_fn=os.setsid)
            terminated = None

            # Try to run the script within the timeout frame.
            try:
                output, _ = process.communicate(timeout=timeout)
                terminated = False
            except subprocess.TimeoutExpired:

                # If the timeout has expired, kill the subprocess.
                print("Timeout reached, terminating subprocess")
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                output, _ = process.communicate()
                terminated = True
                print("Terminated")
        else:

            # Construct the command with the unique files and create a process with that command.
            cmd = "py -3 lib/05AB1E/osabie.py --safe {} < {}".format(code_file, input_file)
            process = subprocess.Popen(cmd, shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       creationflags=CREATE_NO_WINDOW)  # type: subprocess.Popen
            terminated = None

            # Try to run the script within the timeout frame.
            try:
                output, _ = process.communicate(timeout=timeout)
                terminated = False
            except subprocess.TimeoutExpired:

                # If the timeout has expired, kill the subprocess.
                print("Timeout reached, terminating subprocess")
                subprocess.call(["taskkill", "/F", "/T", "/PID", str(process.pid)])
                output, _ = process.communicate()
                terminated = True
                print("Terminated")

        # Remove the files that were used.
        os.remove(code_file)
        os.remove(input_file)

        # Return the first MAX_BYTE_SIZE bytes of the output.
        is_truncated = False
        if output:
            if len(output) > MAX_BYTE_SIZE:
                is_truncated = True
            return output[:MAX_BYTE_SIZE].decode("UTF-8"), terminated, is_truncated
        else:
            return "", terminated, is_truncated


class OsabieRunner:

    @staticmethod
    def generate_random_files() -> (str, str, str):
        """
        Generates the input, output and code files with a random process ID.
        :return: A triple containing the file names.
        """

        # Assign a random ID to the current process.
        m = hashlib.sha256()
        m.update(str(random.random()).encode("UTF-8"))
        process_id = m.hexdigest()

        # Generate the file names for that process.
        code_file_name = "config/osabie.code-{}".format(process_id)
        input_file_name = "config/osabie.input-{}".format(process_id)

        return code_file_name, input_file_name

    @staticmethod
    def run_code(code: str, inputs: str) -> str:
        """
        Run the code from the given osabie source code and the corresponding inputs.
        :param code: The code that will be run with the osabie interpreter.
        :param inputs: The input(s) for the program.
        :return: The result after running the program.
        """

        # Get the files with a random ID.
        code_file_name, input_file_name = OsabieRunner.generate_random_files()

        # Write the code into the code file.
        code_file = open(code_file_name, "wb+")
        code_file.write(code.encode("UTF-8"))
        code_file.close()

        # Write the input into the input file.
        input_file = open(input_file_name, "w+")
        input_file.write(inputs)
        input_file.close()

        # Retrieve the output from the command and return that.
        content = Command.run(timeout=3, code_file=code_file_name, input_file=input_file_name)
        return content
