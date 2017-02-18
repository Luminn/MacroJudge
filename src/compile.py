# This file is part of MacroJudge.
#
# MacroJudge is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MacroJudge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MacroJudge.  If not, see <http://www.gnu.org/licenses/>.

import copy
import os
import random
import re
import subprocess
import sys
import threading
import time
from names import compiler_alias, fallback_compiler_names, all_compilers, standard_compilers, standard_interpreters, \
    file_extension_conv, special_compilers, mono_compilers

# Raised when trying to use a unsupported compiler
class NotSupportedCompilerError(BaseException):
    pass

# Raised when searching for compiler is PATH failed
class CompilerNotFoundError(BaseException):
    pass

# Raised when Compile failed
class CompileTimeError(BaseException):
    pass

# Reserved for future use. A none-zero exit code stands for error now
class RuntimeError(Exception):
    pass

# Raised when a process is killed.
class OutOfTimeError(Exception):
    pass

# a simple class to kill a process after a period of time
class ProcessKiller:
    elapse = 0.1
    def __init__(self, process, time):
        self.process = process
        self.timer = time
        self.abort_flag = False
        self.thread = threading.Thread(target=self._term_process)
    def start(self):
        self.thread.start()
    def abort(self):
        self.abort_flag = True
    def _term_process(self):
        while (self.timer > 0 and not self.abort_flag):
            time.sleep(0.1)
            self.timer -= 0.1
        if not self.abort_flag:
            self.process.terminate()

# a file stream to devnull
devnull = open(os.devnull, 'w')

# test if a command exists, easy way to test a compiler
def test_command(command):
    paths = os.getenv('PATH').split(':')
    for path in paths:
        if os.access(os.path.join(path, command), os.X_OK):
            return True
    return False

# generate a random name
def generate_rand_name():
    f_name =  '.test_' + str(random.randint(1000000, 10000000))
    while os.path.isdir(f_name):
        f_name = '.test_' + str(random.randint(1000000, 10000000))
    return f_name

# removing file extension
def remove_file_extension(src):
    if '.' in src:
        return src[:src.rfind('.')]
    else:
        return src

# compile with linker
def compile_with_linker(src, compiler, args, stdin=None):
    pass

# standard compile
def make(src, compiler):
    src_file = "test." + file_extension_conv[compiler]
    f = open(src_file, 'w')
    f.write(src)
    f.close()
    try:
        if compiler in standard_compilers:
            subprocess.check_call([compiler, src_file, '-o', 'test'], stdout=devnull, stderr=devnull)
        elif compiler in special_compilers:
            arglist = copy.copy(special_compilers[compiler])
            arglist[arglist.index('$SRC')] = src_file
            if '$TAR' in arglist:
                arglist[arglist.index('$OUT')] = 'test'
            subprocess.check_call(arglist, stdout=devnull, stderr=devnull)
    except Exception:
        raise CompileTimeError

# standard run
def run(filename="test", interpreter=None, input=None, timeout=None):
    if interpreter == None:
        proc = subprocess.Popen([os.path.abspath(filename)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        if file_extension_conv[interpreter] is not None:
            proc = subprocess.Popen([interpreter, filename + "." + file_extension_conv[interpreter]], stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            proc = subprocess.Popen([interpreter, filename], stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if timeout != None:
        k = ProcessKiller(proc, timeout)
        k.start()
    timer = int(round(time.time() * 1000))
    out, err = proc.communicate(input)
    timer = int(round(time.time() * 1000)) - timer
    if timeout != None:
        k.abort()
    return out, err, proc.returncode, timer

java_classname_finder = re.compile(r"public +class +(\w+)\s*\{")

# compile java source
def compile_java(src, stdin=None, timeout=None):
    try:
        src_file = re.findall(java_classname_finder, src)[0]
    except IndexError:
        raise CompileTimeError
    dir_name = generate_rand_name()
    os.mkdir(dir_name)
    os.chdir(dir_name)
    f = open(src_file + '.java', 'w')
    f.write(src)
    f.close()
    try:
        subprocess.check_call(['javac', src_file + '.java'], stdout=sys.stdout, stderr=sys.stdout)
    except Exception:
        os.chdir('..')
        os.system("rm -rf " + dir_name)
        raise CompileTimeError
    if isinstance(stdin, str):
        result = run(filename=src_file, interpreter="java", input=stdin, timeout=timeout)
    else:
        result = []
        for i in stdin:
            result.append(run(filename=src_file, interpreter="java", input=i, timeout=timeout))
    os.chdir('..')
    os.system("rm -rf " + dir_name)
    devnull.close()
    return result

# compile a .NET language using mono (with compile target *.exe)
def compile_mono(src, compiler, stdin=None, timeout=None):
    dir = generate_rand_name()
    os.mkdir(dir)
    os.chdir(dir)
    try:
        make(src, compiler)
    except CompileTimeError:
        os.chdir('..')
        subprocess.call(['rm', '-rf', dir], stderr=devnull)
        raise CompileTimeError
    if isinstance(stdin, str):
        result = run(interpreter="mono", input=stdin, timeout=timeout)
    else:
        result = []
        for i in stdin:
            result.append(run(interpreter="mono", input=i, timeout=timeout))
    os.chdir('..')
    subprocess.call(['rm', '-rf', dir], stderr=devnull)
    return result

# compile a source code string using gcc like syntax
def compile_source(src, compiler, stdin=None, timeout=None):
    dir = generate_rand_name()
    os.mkdir(dir)
    os.chdir(dir)
    try:
        make(src, compiler)
    except CompileTimeError:
        os.chdir('..')
        subprocess.call(['rm', '-rf', dir], stderr=devnull)
        raise CompileTimeError
    if isinstance(stdin, str):
        result = run(input=stdin, timeout=timeout)
    else:
        result = []
        for i in stdin:
            result.append(run(input=i, timeout=timeout))
    os.chdir('..')
    subprocess.call(['rm', '-rf', dir], stderr=devnull)
    return result

# interpret a source code string using python like syntax
def interprete_source(src, interpreter, stdin=None, timeout=None):
    dir = generate_rand_name()
    os.mkdir(dir)
    os.chdir(dir)
    src_file = "test." + file_extension_conv[interpreter]
    f = open(src_file, 'w')
    f.write(src)
    f.close()
    if isinstance(stdin, str):
        result = run(interpreter=interpreter, input=stdin, timeout=timeout)
    else:
        result = []
        for i in stdin:
            result.append(run(interpreter=interpreter, input=i, timeout=timeout))
    os.chdir('..')
    subprocess.call(['rm', '-rf', dir], stderr=devnull)
    return result

# compile or interpret a source string and get the output
def excecute_source(src, compiler, stdin=None, timeout=None):
    if compiler_alias.has_key(compiler):
        compiler = compiler_alias[compiler]
    if not test_command(compiler):
        if fallback_compiler_names.has_key(compiler):
            compiler = fallback_compiler_names[compiler]
            if not test_command(compiler):
                raise CompilerNotFoundError
        else:
            raise CompilerNotFoundError
    if compiler in all_compilers:
        return compile_source(src, compiler, stdin, timeout)
    elif compiler in standard_interpreters:
        return interprete_source(src, compiler, stdin, timeout)
    elif compiler == 'javac':
        return compile_java(src, stdin, timeout)
    elif compiler in mono_compilers:
        return compile_mono(src, compiler, stdin, timeout)
    else:
        raise NotSupportedCompilerError