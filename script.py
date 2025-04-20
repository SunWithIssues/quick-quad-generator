## License Under GPLv3, Author: SunWithIssues

import sys
from argparse import ArgumentParser
import pandas as pd
from random import shuffle
from bs4 import BeautifulSoup as soup
import pdfkit 

## Class / Functions

class HtmlPrinter:
	def __init__(self):
		html = """<!DOCTYPE html>
			<html>
			<head>
			<title>Quad Pairing Sheets</title>

			<style>
			@media {
				body { 
					background: white; 
				} 
				div {
					margin-left: 5%;
				}
				table {
				  font-family: arial, sans-serif;
				  border-collapse: collapse !important;
				  border-width:1px 0 0 1px !important;

				}
				th {
				    border-bottom: 2px solid #000 !important; 
				    padding: 8px;
				    font-size: 1.2em;
				    border-width:0 1px 1px 0 !important;
				    background-color:#e0e0e0; 
				    text-align: left;
				    min-width: 20px;
				}


				td{
				  border: 1px solid #dddddd !important;
				  text-align: left;
				  padding: 8px;
				  border-width:0 1px 1px 0 !important;
				}


				/* White Player Name, right align */
				tr td:nth-child(2) { 
					text-align: right; 
					min-width: 300px;

				}	

				th:nth-child(2), tr td:nth-child(1) {
					text-align: right; 
				}

				/* Black Player Name, left align */
				tr td:nth-child(6) { 
					text-align: left; 
					min-width: 300px;

				}

				tr:nth-child(even) { 
					background-color:#e0e0e0; 
				}

			}




			</style>
			</head>
			<body>


			</body>
			</html> 
		"""
		self.bs4_html = soup(html, "html.parser")

	def appendSection(self, html_page, section_name=""):

		pg_tag = self.bs4_html.new_tag("div", id=section_name,style='break-after:page')
		h1_tag = self.bs4_html.new_tag("h1")
		h1_tag.string = section_name + "\n"

		pg = soup(html_page, "html.parser")

		pg_tag.append(h1_tag)
		pg_tag.append(pg)

		self.bs4_html.body.append(pg_tag)



	def append(self, html):
		self.bs4_html.body.append(html)

	def saveAsHtml(self, path):
		with open(path, "w") as file:
			file.write(str(self.bs4_html))

	def saveAsPdf(self, path):
		pdfkit.from_string(str(self.bs4_html), path) 




class QuadTournament:
	def __init__(self, players_dataframe, first_board_num=1, show_rating=True, must_sort=True):
		self.hp = HtmlPrinter()
		self.board_num = first_board_num 
		self.df = players_dataframe
		self.path = "quads"

		self.must_sort = must_sort
		self.show_rating = show_rating
		self.print_pdf = print_pdf


	def make_pairing_sheets(self, print_choice=0):
		
		# sort by ratings
		if self.must_sort:
			self.df.sort_values(by=['rating'], inplace=True, ascending=False)
			self.df.reset_index(drop=True, inplace=True)

		# count number of rows/players
		row_count = self.df.shape[0] 

		if row_count % 4 != 0: # create bottom swiss + top quads
			n = row_count % 4 + 4
			self._quadPrint(0, row_count - n)
			self._swissPrintRound1(row_count - n, row_count)
		else:                  # create quads for all
			self._quadPrint(0, df.shape[0])

		# create + save quads pdf / html file
		if print_choice == 0:
			self.hp.saveAsPdf(self.path + ".pdf")
			self.hp.saveAsHtml(self.path + ".html")
		elif print_choice == 1:
			self.hp.saveAsHtml(self.path + ".html")
		else:
			self.hp.saveAsPdf(self.path + ".pdf")


	def save_as_pdf(self, path):
		self.hp.saveAsPdf(path)

	def save_as_html(self, path):
		self.hp.saveAsHtml(path)


	def _name_format(self, row):
		s = self.df.loc[row, "name"] 

		if self.show_rating:
			s += "( "+ str(self.df.loc[row, "rating"]) + " )"

		return s

	def _layoutDf(self, size=0):
		# board_num, W_name (W_rating), W_Res, [blank space], B_Res, B_name (B_rating) 
		l = pd.DataFrame(columns=['Board','White','W_Res','-','B_Res','Black'])
		for i in range(size):
			l = l._append(pd.Series(), ignore_index = True)
		return l

	def _quadPrint(self, start_idx, end_idx):

		
		quad_num = 1

		# print(self._layoutDf(2))
		for i in range(start_idx, end_idx, 4): # For every 4 players
			qOrder = list(range(i, i+4))
			shuffle(qOrder)
			rounds = [self._layoutDf(2) for i in range(3)]


			## Pairing All 3 Rounds
			rounds[0].loc[0, "White"] = self._name_format(qOrder[0])
			rounds[0].loc[0, "Black"] = self._name_format(qOrder[3])

			rounds[0].loc[1, "White"] = self._name_format(qOrder[1])
			rounds[0].loc[1, "Black"] = self._name_format(qOrder[2])

			rounds[1].loc[0, "White"] = self._name_format(qOrder[2])
			rounds[1].loc[0, "Black"] = self._name_format(qOrder[0])

			rounds[1].loc[1, "White"] = self._name_format(qOrder[3])
			rounds[1].loc[1, "Black"] = self._name_format(qOrder[1])


			toss = [[0,1], [2,3]] # Last round colors are a toss up
			shuffle(toss[0])
			shuffle(toss[1])

			rounds[2].loc[0, "White"] = self._name_format(qOrder[toss[0][0]])  
			rounds[2].loc[0, "Black"] = self._name_format(qOrder[toss[0][1]]) 

			rounds[2].loc[1, "White"] = self._name_format(qOrder[toss[1][0]]) 
			rounds[2].loc[1, "Black"] = self._name_format(qOrder[toss[1][1]]) 


			
			h = ""
			for i in range(3):
				## Setting up board number
				rounds[i]["Board"] = [self.board_num, self.board_num+1]
				rounds[i]['-'] = ['-','-']


				## Creating html page
				h += f"<h2>Round {i+1}</h2>" + rounds[i].to_html(index=False, na_rep="")

			self.hp.appendSection(h, f"Quad {quad_num}")

			quad_num  += 1
			self.board_num += 2

	


	def _swissPrintRound1(self, start_idx, end_idx):
		# count number of rows/players
		row_count = start_idx + end_idx

		round1 = self._layoutDf(4)

		offset = row_count//2
		j = 0
		for i in range(start_idx, offset):
			round1.loc[j, "White"]  = self._name_format(i)
			round1.loc[j, "Black"]  = self._name_format(offset+j)

			round1.loc[j, "Board"] = self.board_num
			round1.loc[j, '-'] = '-'

			self.board_num += 1
			j += 1

		if(row_count % 2 == 1):

			round1.loc[j, "White"]    = self._name_format(end_idx-1)
			round1.loc[j, "Board"] = self.board_num
			round1.loc[j, "W_Res"]     = "1-bye"
			round1.loc[j, '-'] = '-'

			self.board_num += 1

		h = "" + f"<h2>Round 1</h2>" + round1.to_html(index=False, na_rep="")

		self.hp.appendSection(h, f"Swiss")




def main():

	parser = ArgumentParser()

	parser.add_argument("path", help="Path to the csv which will be used for generating the pairings.",
                    type=str)
	parser.add_argument("-nr", "--no_rating", help="Do not show rating information.",
                    action="store_false")
	parser.add_argument("-ns", "--no_sort", help="Do not sort table before pairing.", action="store_false")
	parser.add_argument("-b", "--board_num", help="Starting board number of first pairing.", type=int, default=1)
	parser.add_argument("--html_only", help="Creates only the html file component", action="store_true")
	parser.add_argument("--pdf_only", help="Creates only the pdf file component", action="store_true")

	args = parser.parse_args()

	try:
		df = pd.read_csv(args.path)
	except Exception as e:
		raise
		sys.exit(1)



	quads = QuadTournament(df, first_board_num=args.board_num, show_rating=args.no_rating, must_sort=args.no_sort)

	if(args.html_only == args.pdf_only ):
		quads.make_pairing_sheets()
	elif(args.html_only):
		quads.make_pairing_sheets(1)
	else:
		quads.make_pairing_sheets(2)

	# TODO::LATER:: check ids and pull ratings from uscf database



	

if __name__ == '__main__':
	main()