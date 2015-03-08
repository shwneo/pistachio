import ply.lex as lex

tokens = (
	'CLASS',
	'DEF',
	'IF',
	'ELSE',
	'ELIF',
	'FOR',
	'IN',
	'WHILE',
	'BREAK',
	'EXCEPT',
	'RAISE',
	'IMPORT',
	'FROM',
	'AS',
	'WITH',
	'IS',
	'RETURN',
	'CONTINUE',
	'LAMBDA',
	'TRY',
	'AND',
	'OR',
	'NOT',
	'ASSERT',
	'LPAREN',
  	'RPAREN',
  	'COMMA',
  	'DOT',
  	'LSQABRACK',
  	'RSQABRACK',
  	'LBRACE',
  	'RBRACE',
  	'SLASH',
  	'BACKSLASH',
  	'PLUS',
  	'ASSIGN',
  	'EQUAL',
  	'NUMBER',
	'MINUS',
	'TIMES',
	'DIVIDE',
	'INTEGER',
	#'FLOAT',
	'COMMENT',
	'SIGQUOT',
	'DOUBLEQUOT',
	'TRIPLEQUOT',
	'WHITESPACE',
	'NEWLINE',
	'PERCENT',
	'COLON',
	'IDENTIFIER',
)

def t_IMPORT(t):
	r'import$'
	return t

def t_CLASS(t):
	r'class$'
	return t

def t_DEF(t):
	r'def$'
	return t

def t_IF(t):
	r'if$'
	return t

def t_ELSE(t):
	r'else$'
	return t

def t_ELIF(t):
	r'elif$'
	return t

def t_FOR(t):
	r'for$'
	return t

def t_IN(t):
	r'in$'
	return t

def t_WHILE(t):
	r'while$'
	return t

def t_BREAK(t):
	r'break$'
	return t

def t_EXCEPT(t):
	r'except$'
	return t

def t_RAISE(t):
	r'raise$'
	return t

def t_FROM(t):
	r'from$'
	return t

def t_AS(t):
	r'as$'
	return t

def t_WITH(t):
	r'with$'
	return t

def t_IS(t):
	r'is$'
	return t

def t_RETURN(t):
	r'return$'
	return t

def t_CONTINUE(t):
	r'continue$'
	return t

def t_LAMBDA(t):
	r'lambda'
	return t

def t_TRY(t):
	r'try$'
	return t

def t_AND(t):
	r'and$'
	return t

def t_OR(t):
	r'or$'
	return t

def t_NOT(t):
	r'not$'
	return t

def t_ASSERT(t):
	r'assert'
	return

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_DOT = r'\.'
t_LSQABRACK = r'\[' 
t_RSQABRACK = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SLASH = r'\/'
t_BACKSLASH = r'\\'
t_INTEGER = r'\d+([eE]\d+)?'
#t_FLOAT = r'[(\.\d+)(\d+\.\d+)](eE\d+)?'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_ignore_COMMENT = r'\#.*'
t_SIGQUOT = r'\''
t_DOUBLEQUOT = r'\"'
t_TRIPLEQUOT = r'[\'\"]{3}'
t_IDENTIFIER = r'[_a-zA-Z][\d\w]*'
t_WHITESPACE = r'[ \t]+'
t_NEWLINE = r'\n'
t_ASSIGN = '='
t_EQUAL = '=='
t_PERCENT = '\%'
t_COLON = ':'

lexer = lex.lex()
out_file = open('.\\lexer_out.txt', 'w')
with open('C:\\Python27\\Lib\\lib2to3\\fixer_base.py','r') as input_file:
	input_text = input_file.read()
	lexer.input(input_text)
	while True:
		tok = lexer.token()
		if not tok: break
		print tok
