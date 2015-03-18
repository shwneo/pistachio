import ply.lex as lex

_g_indent = []
_g_lcontinue = False

_g_barrier_scope = { 'in_scope':False,
					 'character':None,
					 'count':0,
					 'barrier_couple':{
					 	')':'(',
					 	']':'[',
					 	'}':'{'}
					}

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
	'global':'GLOBAL',
	'exec':'EXEC',
	'finally':'FINALLY',
	'yield':'YIELD',
}


tokens = [
	'LPAREN',
  	'RPAREN',
  	'COMMA',
  	'DOT',
  	'DOTS',
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
	'RUBSIGQUOT',
	'RUBDOUBLEQUOT',
	'RUBTRIPLEQUOT',
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
	'NOTEQUAL2',
	'BITOR',
	'BITAND',
	'BITXOR',
	'LSHIFT',
	'RSHIFT',
	'MOD',
	'COMPLEMENT',
	'POWER',
	'IDENTIFIER',
	'CLASSDEFINE',
	'SEMICO',
	'SKIM',
	'AT',
	'INDENT',
	'DEDENT',
	'EOF',
	'STRMODIF',
] + list(key_words.values())

states = (
   ('basestring','exclusive'),
   ('longstring', 'exclusive'),
   ('indent', 'exclusive')
)

def t_RUBTRIPLEQUOT(t):
	r'([rR]?|[uU]?|[bB]?)(\'{3}|\"{3})'
	t.type = 'TRIPLEQUOT'
	if t.value[-1] == '\'':
		t.value = '\'\'\''
	else:
		t.value = '\"\"\"'
	return start_string(t, True)

def t_RUBDOUBLEQUOT(t):
	r'([rR]?|[uU]?|[bB]?)\"'
	t.type = 'DOUBLEQUOT'
	t.value = '\"'
	return start_string(t)

def t_RUBSIGQUOT(t):
	r'([rR]?|[uU]?|[bB]?)\''
	t.type = 'SIGQUOT'
	t.value = '\''
	return start_string(t)

def t_IDENTIFIER(t):
	r'[_a-zA-Z][\d\w]*'
	t.type = key_words.get(t.value,'IDENTIFIER')
	return t

def t_OCT(t):
	r'0o[1-7]+[0-7]*[Ll]?'
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

def t_basestring_end(t):
	r'[\'\"]'
	if t.value == t.lexer.quot_mark:
		t.value = t.lexer.lexdata[t.lexer.start_pos:t.lexer.lexpos]
		t.type = 'BASESTRING'
		t.lexer.pop_state()
		return t

def t_longstring_end(t):
	r'\'{3}|\"{3}'
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

def t_NEWLINE(t):
	r'\n'
	global _g_lcontinue
	global _g_barrier_scope
	if _g_lcontinue:
		_g_lcontinue = False
		return
	if _g_barrier_scope['in_scope']:
		t.type = 'WHITESPACE'
		t.value = None
		return t
	t.lexer.push_state('indent')
	t.type = 'NEWLINE'
	return t

def t_indent_blankline(t):
	r'[ \t]*\n'
	t.type = 'WHITESPACE'
	t.value = None
	# DONT pop_state!
	# because of the '\n'
	# we're still in the 'indent' mode
	return t

def t_indent_comment(t):
	r'''[ \t]*\#.*\n'''
	pass

def t_indent_end(t):
	r'[ \t]+'

	strip_str = t.value
	indent_num = len(strip_str)
	global _g_indent
	if len(_g_indent) > 0:
		if _g_indent[-1] == indent_num:
			# just a newline within the scope
			# return no more NEWLINE token
			t.lexer.pop_state()
			return
		if _g_indent[-1] < indent_num:
			# new scope starts with a bigger indent
			t.type = 'INDENT'
			_g_indent.append(indent_num)
			t.lexer.pop_state()
			return t
		if _g_indent[-1] > indent_num:
			# go through the indent stack, try to find the right indent level
			# if can't, raise a exception
			while len(_g_indent) > 0:
				if _g_indent[-1] == indent_num:
					t.type = 'DEDENT'
					t.lexer.pop_state()
					return t
				else:
					_g_indent.pop(-1)
					if len(_g_indent) == 0:
						raise Exception('IndentationError: unindent does not match any outer indentation level')
					t.type = 'DEDENT'
					t.value = None
					t.lexer.lexpos -= len(strip_str)
					return t
	else:
		# Without any indent yet, mybe a new file, or a fresh top scope
		# Lexer parser cannot realize an 'Unexpected indent' exception
		# hoping yacc part could do that
		_g_indent.append(indent_num)
		t.type = 'INDENT'
		t.lexer.pop_state()
		return t

def t_indent_pass(t):
	# A newline without any indent
	r'\S+'
	global _g_indent
	if len(_g_indent) > 0:
		# Clean all indents
		# Accroding to Python grammar,
		# we should return every 'DEDENT' token
		# of scopes this statement closed
		_g_indent.pop(-1)
		t.lexer.lexpos -= len(t.value)
		t.type = 'DEDENT'
		t.value = None
		return t
	else:
		t.lexer.pop_state()
		# rollback to the beging of this token
		# to prevent swallowing it
		t.lexer.lexpos -= len(t.value)

def t_BACKSLASH(t):
	r'\\'
	global _g_lcontinue
	_g_lcontinue = True

def t_WHITESPACE(t):
	r'[ \t]+'
	global _g_lcontinue
	_g_lcontinue = False

def left_barrier_scope(character):
	global _g_barrier_scope
	if _g_barrier_scope['in_scope']:
		if _g_barrier_scope['character'] == character:
			_g_barrier_scope['count'] += 1
		else:
			return
	else:
		_g_barrier_scope['in_scope'] = True
		_g_barrier_scope['character'] = character
		_g_barrier_scope['count'] = 1

def right_barrier_scope(character):
	global _g_barrier_scope
	if _g_barrier_scope['in_scope']:
		if _g_barrier_scope['character'] ==\
				_g_barrier_scope['barrier_couple'].get(character):
			_g_barrier_scope['count'] -= 1
			if _g_barrier_scope['count'] == 0:
				_g_barrier_scope['character'] = None
				_g_barrier_scope['in_scope'] = False
	else:
		raise Exception('Unexpected '+ character)

def t_LPAREN(t):
	r'\('
	left_barrier_scope(t.value)
	return t

def t_RPAREN(t):
	r'\)'
	right_barrier_scope(t.value)
	return t

def t_LSQABRACK(t):
	r'\['
	left_barrier_scope(t.value)
	return t

def t_RSQABRACK(t):
	r'\]'
	right_barrier_scope(t.value)
	return t

def t_LBRACE(t):
	r'\{'
	left_barrier_scope(t.value)
	return t

def t_RBRACE(t):
	r'\}'
	right_barrier_scope(t.value)
	return t

t_COMMA = r','
t_DOT = r'\.'
t_DOTS = r'\.{2,}'
t_SLASH = r'\/'
#t_BACKSLASH = r'\\'
t_INTEGER = r'\d+([eE][+-]?\d+)?[Ll]?'
t_HEX = r'0x[0-9a-fA-F]+[Ll]?$'
t_FLOAT = r'([0-9]*\.[0-9]+|[0-9]+\.[0-9]*)([eE][+-]?[0-9]+)?'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/|\/\/'
t_ignore_COMMENT = r'\#.*'
t_ASSIGN = r'='
t_EQUAL = r'=='
t_COLON = r':'
t_LESSTHAN = r'<'
t_BIGGERTHAN = r'>'
t_LESSEQUAL = r'<='
t_BIGGEREQUAL = r'>='
t_NOTEQUAL = r'!='
t_NOTEQUAL2 = r'<>'
t_BITOR = r'\|'
t_BITAND = r'\&'
t_BITXOR = r'\^'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'
t_MOD = r'%'
t_COMPLEMENT = r'~'
t_POWER = r'\*\*'
t_SEMICO = r';'
t_AUGASSIGN = r'\+=|\-=|\*=|\/=|\^=|\&=|\%=|\|=|<<=|>>=|\*\*=|\/\/='
t_SKIM = r'\`'
t_AT = r'@'

lexer = lex.lex()

def main():
	lexer = lex.lex()
	#with open('C:\\Python27\\Lib\\sha.py','r') as input_file:
	with open('.\\test.py') as input_file:
		input_text = input_file.read()
		lexer.input(input_text)
		while True:
			tok = lexer.token()
			if not tok: break
			print tok

if __name__ == '__main__':
	exit(main())
