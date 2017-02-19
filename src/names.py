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

# can't use the dict below because it's not sorted in python2
COMPILERS_DISPLAY_NAMES = [
    "Default C Compiler",
    "GNU GCC Compiler",
    "LLVM Clang Compiler",
    "Tiny C Compiler",
    "GNU G++ Compiler",
    "LLVM Clang++ Compiler",
    "GNU Fortran Compiler",
    "Free Pascal Compiler",
    "Java Compiler",
    "Python 2.x",
    "Python 3.x",
    "Perl",
    "Ruby",
    "Bash (Shell)",
    "GNU Common Lisp",
    "GNU Guile (Scheme)",
    "Racket (Scheme)",
    "PHP",
    "Node.js",
    "Go",
    "GNU Octave (Matlab)",
    "Mono C# Compiler",
    "Mono VB.NET Compiler",
    "Mono F# Compiler"
]

#info about the displayed names the tuple contains compiler names in terminal and language names in lowercase
COMPILERS_INFO = {
    "Default C Compiler": ("cc", "c"),
    "GNU GCC Compiler": ("gcc", "c"),
    "LLVM Clang Compiler": ("clang", "c"),
    "Tiny C Compiler": ("tcc", "c"),
    "GNU G++ Compiler": ("g++", "c++"),
    "LLVM Clang++ Compiler": ("clang++", "c++"),
    "GNU Fortran Compiler": ("gfortran", "fortran"),
    "Free Pascal Compiler": ("fpc", "pascal"),
    "Java Compiler": ("javac", "java"),
    "Python 2.x": ("python2", "python2"),
    "Python 3.x": ("python3", "python3"),
    "Perl": ("perl", "perl"),
    "Ruby": ("ruby", "ruby"),
    "Bash (Shell)": ("bash", "shell"),
    "GNU Common Lisp": ("clisp", "lisp"),
    "GNU Guile (Scheme)": ("guile", "scheme"),
    "Racket (Scheme)": ("racket", "racket"),
    "PHP": ("php", "php"),
    "Node.js": ("node", "javascript"),
    "Go": ("go", "go"),
    "GNU Octave (Matlab)" : ("octave", "matlab"),
    "Mono C# Compiler" : ("mcs", "C#"),
    "Mono VB.NET Compiler" : ("vbnc", "VB.NET"),
    "Mono F# Compiler" : ("fsharpc", "F#")
}

# convert language names and other common alias to compiler names in terminal
compiler_alias = {
    'c' : 'gcc',
    'c++' : 'g++',
    'objective-c' : 'gobjc',
    'objective-c++' : 'gobjc++',
    'fortran' : 'gfortran',
    'pascal' : 'fpc',
    'free pascal' : 'fpc',
    'java' : 'javac',
    'llvm' : 'clang',
    'python' : 'python2',
    'javascript' : 'node',
    'js' : 'node',
    'node' : 'nodejs',
    'shell' : 'bash',
    'common lisp' : 'clisp',
    'lisp' : 'clisp',
    'scheme' : 'guile',
    'golang' : 'go',
    'matlab' : 'octave',
    "csharp" : "mcs",
    "dotnet" : "mcs",
    "c#" : "mcs",
    "visual basic": "vbnc",
    "vb.net" : "vbnc",
    "f#" : "fsharpc",
    "fsharpi" : "fsharpc",
    "fsharp" : "fsharpc"
}

# for compilers that has different names (node is called nodejs on many linux distros)
fallback_compiler_names = {
    'node' : 'nodejs'
}

# for all compilers that uses the compile_source function
all_compilers = [
    'cc', 'gcc', 'clang', 'tcc', 'g++', 'clang++', 'gfortran', 'fpc', 'go'
]

# compilers that supports "gcc src.c -o output" like syntax
standard_compilers = [
    'cc', 'gcc', 'clang', 'tcc', 'g++', 'clang++', 'gfortran'
]

# interpreters that supports "python src.py" like syntax
standard_interpreters = [
    'python2', 'python3', 'ruby', 'clisp', 'guile', 'racket', 'perl', 'bash', 'php', 'nodejs', 'node', 'octave'
]

# match file extensions and compiler names
file_extension_conv = {
    'cc' : 'c', 'gcc' : 'c', 'clang' : 'c', 'tcc' : 'c',
    'g++' : 'cpp', 'clang++' : 'cpp',
    'gobjc' : 'm', 'clang-objc' : 'm',
    'gobjc++' : 'mm', 'clang-objc++' : 'mm',
    'gfortran' : 'f95',
    'fpc' : 'pas',
    'python2' : 'py', 'python3' : 'py',
    'perl' : 'pl',
    'ruby' : 'rb',
    'clisp' : 'lisp',
    'guile' : 'scm',
    'racket' : 'scm',
    'php' : 'php',
    'nodejs' : 'js',
    'bash' : 'sh',
    'sh' : 'sh',
    'javac' : 'java',
    'go' : 'go',
    'lua' : 'lua',
    'octave' : 'm',
    'mcs' : 'cs',
    'vbnc' : 'vb',
    'fsharpc' : 'fs',
    'java' : None,   # the run function reqiures this
    'mono' : 'exe',  # the run function requires this
}

# use pattern matching for specific compilers that uses a different syntax
# $SRC for source code and $OUT for output
special_compilers = {
    "fpc" : ["fpc", "$SRC"],
    "mcs" : ["mcs", "$SRC"],
    "vbnc" : ["vbnc", "$SRC"],
    "fsharpc" : ["fsharpc", "$SRC"],
    "go" : ['go', 'build', '$SRC'],
    "gobjc" : ['gcc', '$SRC', '`gnustep-config --objc-flags`', '-lobjc', '-lgnustep-base', '-o', '$OUT']
}

# all compilers that has a target of an exe file
mono_compilers = [
    'mcs', 'vbnc', 'fsharpc'
]

compiled_compilers = [
    'cc', 'gcc', 'clang', 'tcc', 'g++', 'clang++', 'gfortran', 'fpc', 'go', 'fpc'
]

bytecode_compilers = [
    'javac', 'mcs', 'vbnc', 'fsharpc'
]