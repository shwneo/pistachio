import ply.lex as lex

key_words = {
	'class':'CLASS',
	'def':'DEF',
	'del':'DEL',
	'if':'IF',
	'else':'ELSE',
	'elif':'ELIF',
	'for':'FOR',
	'in':'IN',
	'while':'WHILE',
	'break':'BREAK',
	'except':'EXCEPT',
	'raise':'RAISE',
	'import':'IMPORT',
	'from':'FROM',
	'as':'AS',
	'with':'WITH',
	'is':'IS',
	'return':'RETURN',
	'continue':'CONTINUE',
	'lambda':'LAMBDA',
	'try':'TRY',
	'and':'AND',
	'or':'OR',
	'not':'NOT',
	'assert':'ASSERT',
	'print':'PRINT',
	'pass':'PASS',
	'global','GLOBAL'
	'exec':'EXEC',
	'finally':'FINALLY',
}


tokens = [
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
  	'AUGASSIGN',
  	'EQUAL',
  	'NUMBER',
	'MINUS',
	'TIMES',
	'DIVIDE',
	'INTEGER',
	'HEX',
	'OCT',
	'FLOAT',
	'COMPLEX',
	'COMMENT',
	'SIGQUOT',
	'DOUBLEQUOT',
	'TRIPLEQUOT',
	'WHITESPACE',
	'NEWLINE',
	'COLON',
	'BASESTRING',
	'LONGSTRING',
	'LESSTHAN',
	'BIGGERTHAN',
	'LESSEQUAL',
	'BIGGEREQUAL',
	'NOTEQUAL',
	'BITOR',
	'BITAND',
	'BITXOR',
	'LSHIFT',
	'RSHIFT',
	'MOD',
	'COMPLEMENT',
	'POWER',
	'SQRT',
	'IDENTIFIER',
	'CLASSDEFINE',
	'SEMICO',
	'SKIM',
	'AT',
	'INDENT',
	'DEDENT',
] + list(key_words.values())

states = (
   ('basestring','exclusive'),
   ('longstring', 'exclusive'),
)

def t_IDENTIFIER(t):
	r'[_a-zA-Z][\d\w]*'
	t.type = key_words.get(t.value,'IDENTIFIER')
	return t

def t_OCT(t):
	r'0[1-7]+[0-7]*[Ll]?'
	return t

def t_COMPLEX(t):
	r'\d+j[$\s]'
	t.value = t.value.strip()
	return t

def start_string(t, long_str=False):
	t.lexer.quot_mark = t.value
	t.lexer.start_pos = t.lexer.lexpos
	t.lexer.long_str = long_str
	if not long_str:
		t.lexer.push_state('basestring')
	else:
		t.lexer.push_state('longstring')
	return t

def t_TRIPLEQUOT(t):
	r'[\'\"]{3}'
	return start_string(t, True)

def t_DOUBLEQUOT(t):
	r'\"'
	return start_string(t)

def t_SIGQUOT(t):
	r'\''
	return start_string(t)

def t_basestring_end(t):
	r'[\'\"]'
	if t.value == t.lexer.quot_mark:
		t.value = t.lexer.lexdata[t.lexer.start_pos:t.lexer.lexpos]
		t.type = 'BASESTRING'
		t.lexer.pop_state()
		return t

def t_longstring_end(t):
	r'(\'|\"){3}'
	if t.value == t.lexer.quot_mark:
		t.value = t.lexer.lexdata[t.lexer.start_pos:t.lexer.lexpos]
		t.type = 'LONGSTRING'
		t.lexer.pop_state()
		return t

def process_string(t):
	if t.value[0] == '\\':
		t.lexer.skip(2)
		return
	else:
		t.lexer.skip(1)
	if t.value[0] == '\n' and not t.lexer.long_str:
		raise Exception("Unexpected end of line at %d" % t.lexer.lexpos)

def t_basestring_error(t):
	process_string(t)

def t_longstring_error(t):
	process_string(t)

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
t_INTEGER = r'\d+([eE][+-]?\d+)?[Ll]?'
t_HEX = r'0x[0-9a-fA-F]+[Ll]?$'
t_FLOAT = r'([0-9]*\.[0-9]+|[0-9]+\.[0-9]*)([eE][+-]?[0-9]+)?'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_ignore_COMMENT = r'\#.*'
t_WHITESPACE = r'[ \t]+'
t_NEWLINE = r'\n'
t_ASSIGN = r'='
t_EQUAL = r'=='
t_COLON = r':'
t_LESSTHAN = r'<'
t_BIGGERTHAN = r'>'
t_LESSEQUAL = r'<='
t_BIGGEREQUAL = r'>='
t_NOTEQUAL = r'!='
t_BITOR = r'\|'
t_BITAND = r'\&'
t_BITXOR = r'\^'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'
t_MOD = r'%'
t_COMPLEMENT = r'~'
t_POWER = r'\*\*'
t_SQRT = r'\/\/'
t_SEMICO = r';'
t_AUGASSIGN = r'\+=|\-=|\*=|\/=|\^=|\&=|\%=|\|=|<<=|>>=|\*\*=|\/\/='
t_SKIM = r'\`'
t_AT = r'@'
t_INDENT = r'^\s'

def main():
	lexer = lex.lex()
	out_file = open('.\\lexer_out.txt', 'w')
	#with open('C:\\Python27\\Lib\\sha.py','r') as input_file:
	with open('C:\\Python27\\Lib\\lib2to3\\test.py') as input_file:
		input_text = input_file.read()
		input_text.decode('utf-8')
		lexer.input(input_text)
		while True:
			tok = lexer.token()
			if not tok: break
			print tok

if __name__ == '__main__':
	exit(main())
