import ply.lex as lex

key_words = {
	"auto":"AUTO",
	"break":"BREAK",
	"case":"CASE",
	"char":"CHAR",
	"const":"CONST",
	"continue":"CONTINUE",
	"default":"DEFAULT",
	"do":"DO",
	"double":"DOUBLE",
	"else":"ELSE",
	"enum":"ENUM",
	"extern":"EXTERN",
	"float":"FLOAT",
	"for":"FOR",
	"goto":"GOTO",
	"if":"IF",
	"int":"INT",
	"long":"LONG",
	"register":"REGISTER",
	"return":"RETURN",
	"short":"SHORT",
	"signed":"SIGNED",
	"sizeof":"SIZEOF",
	"struct":"STRUCT",
	"static":"STATIC",
	"switch":"SWITCH",
	"typedef":"TYPEDEF",
	"union":"UNION",
	"unsigned":"UNSIGNED",
	"void":"VOID",
	"volatile":"VOLATILE",
	"while":"WHILE",
}



class CLexer:

	tokens = [
		"ELLIPSIS",
		"RIGHT_ASSIGN",
		"LEFT_ASSIGN",
		"ADD_ASSIGN",
		"SUB_ASSIGN",
		"MUL_ASSIGN",
		"DIV_ASSIGN",
		"MOD_ASSIGN",
		"AND_ASSIGN",
		"XOR_ASSIGN",
		"OR_ASSIGN",
		"RIGHT_OP",
		"LEFT_OP",
		"INC_OP",
		"DEC_OP",
		"PTR_OP",
		"AND_OP",
		"OR_OP",
		"LE_OP",
		"GE_OP",
		"EQ_OP",
		"NE_OP",
		"LBRACE",
		"RBRACE",
		"LSQABRACK",
		"RSQABRACK",
		"WHITESPACE",
		"IDENTIFIER",
		"STRING_LITERAL",
		"CONSTANT",
		"COMMENT",
		'TYPE_NAME',
	] + list(key_words.values())

	literals = [
		";",",",":","=",
		"(",")",".","&",
		"!","~","-","+",
		"*","/","%","<",
		">","^","|","?",
	]

	def __init__(self):
		self.lexer = lex.lex(module=self)

	def input(self, in_str):
		return self.lexer.input(in_str)

	def token(self):
		return self.lexer.token()

	def t_IDENTIFIER(self, t):
		r'[_a-zA-Z][\d\w]*'
		t.type = key_words.get(t.value,'IDENTIFIER')
		return t

	def t_ELLIPSIS(self, t):
		r"\.\.\."
		t.type = "ELLIPSIS"
		return t

	def t_RIGHT_ASSIGN(self, t):
		r">>="
		t.type = "RIGHT_ASSIGN"
		return t
	
	def t_LEFT_ASSIGN(self, t):
		r"<<=" 
		t.type = "LEFT_ASSIGN" 
		return t
	
	def t_ADD_ASSIGN(self, t):
		r"\+=" 
		t.type = "ADD_ASSIGN"
		return t
	
	def t_SUB_ASSIGN(self, t):
		r"-="  
		t.type = "SUB_ASSIGN"  
		return t
	
	def t_MUL_ASSIGN(self, t):
		r"\*=" 
		t.type = "MUL_ASSIGN"  
		return t
	
	def t_DIV_ASSIGN(self, t):
		r"/="  
		t.type = "DIV_ASSIGN"  
		return t
	
	def t_MOD_ASSIGN(self, t):
		r"%="  
		t.type = "MOD_ASSIGN"  
		return t
	
	def t_AND_ASSIGN(self, t):
		r"&="  
		t.type = "AND_ASSIGN"  
		return t
	
	def t_XOR_ASSIGN(self, t):
		r"\^=" 
		t.type = "XOR_ASSIGN"  
		return t
	def t_OR_ASSIGN(self, t):
		r"\|=" 
		t.type = "OR_ASSIGN"   
		return t
	
	def t_RIGHT_OP(self, t):
		r">>"  
		t.type = "RIGHT_OP"    
		return t
	
	def t_LEFT_OP(self, t):
		r"<<"  
		t.type = "LEFT_OP"     
		return t
	
	def t_INC_OP(self, t):
		r"\+\+"
		t.type = "INC_OP"      
		return t
	def t_DEC_OP(self, t):
		r"--"  
		t.type = "DEC_OP"      
		return t
	
	def t_PTR_OP(self, t):
		r"->"  
		t.type = "PTR_OP"      
		return t
	
	def t_AND_OP(self, t):
		r"&&"  
		t.type = "AND_OP"      
		return t
	
	def t_OR_OP(self, t):
		r"\|\|" 
		t.type = "OR_OP"       
		return t
	
	def t_LE_OP(self, t):
		r"<="  
		t.type = "LE_OP"       
		return t
	
	def t_GE_OP(self, t):
		r">="  
		t.type = "GE_OP"       
		return t
	
	def t_EQ_OP(self, t):
		r"=="  
		t.type = "EQ_OP"       
		return t
	
	def t_NE_OP(self, t):
		r"!="  
		t.type = "NE_OP"       
		return t

	def t_LBRACE(self, t):
		r"{|<%"
		return t

	def t_RBRACE(self, t):
		r"}|%>"
		return t

	def t_LSQABRACK(self, t):
		r"\[|<:"
		return t

	def t_RSQABRACK(self, t):
		r"\]|:>"
		return t

	def t_WHITESPACE(self, t):
		r"[\s\t\n\v\f]"
		return t

	def t_hex(self, t):
		r"0[Xx][0-9a-fA-F]+([uU]?[lL]?[lL]?)"
		t.type = "CONSTANT"
		return t

	def t_oct(self, t):
		r"0\d+([uU]?[lL]?[lL]?)?"
		t.type = "CONSTANT"
		return t

	def t_float(self, t):
		r"\d+\.\d*([Ee][\+-]?\d+)?[FfLl]?|\d*\.\d+([Ee][\+-]?\d+)?[FfLl]?"
		t.type = "CONSTANT"
		return t

	def t_integer(self, t):
		r"\d+([Ee][\+-]?\d+)?[FfLl]?"
		t.type = "CONSTANT"
		return t

	def t_character(self, t):
		r"[a-zA-Z_]?'(\.|[^\\\']|\\\'|\\.)+'"
		t.type = "CONSTANT"
		return t

	def t_STRING(self, t):
		r"[a-zA-Z_]?\"(\.|[^\\\"]|\\\"|\\.)*\""
		t.type = "STRING_LITERAL"
		return t

	def t_ignore_COMMENT(self, t):
		r"\#.*"
		pass

	def t_error(self, t):
		print('C Language Lexer Error!')
		pass

lexer = CLexer()

def main():
	with open('.\\test.i') as input_file:
		input_text = input_file.read()
		lexer.input(input_text)
		while True:
			tok = lexer.token()
			if not tok: break
			print tok

if __name__ == '__main__':
	exit(main())

